# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import json
import time
from enum import Enum
from typing import Any
from urllib.parse import quote, urlencode

import httpx
from pydantic import BaseModel, ValidationError

from kentik_api.auth.credentials import auth_headers
from kentik_api.core.api_config import DEADLINE_EXTENSION, APIConfig, _check_deadline
from kentik_api.core.rate_limit import RateLimit, attach_rate_limit, rate_limit_of
from kentik_api.errors import (
    AuthenticationError,
    ConfigurationError,
    HTTPException,
    KentikError,
    TransportError,
)

# RFC 3986 pchar minus the unreserved set, which quote() never encodes. Leaving
# these raw matters: grpc-gateway does not decode reserved characters in a path
# parameter, so an encoded ":" in a timestamp would reach the server as "%3A".
_PATH_SEGMENT_SAFE = "!$&'()*+,;=:@"


def _wire_scalar(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def _wire_query_value(value: Any) -> Any:
    value = _wire_scalar(value)
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_wire_query_value(item) for item in value if item is not None]
    return value


def _normalize_credential(
    field_name: str, value: str | None, *, operation_name: str
) -> str:
    if value is None:
        raise ConfigurationError(
            f"{operation_name}: missing required credential field {field_name}."
        )

    normalized = value.strip()
    if not normalized:
        raise ConfigurationError(
            f"{operation_name}: credential field {field_name} is empty after trimming whitespace."
        )

    if any(ord(ch) < 32 or ord(ch) == 127 for ch in normalized):
        raise ConfigurationError(
            f"{operation_name}: credential field {field_name} contains control characters."
        )

    try:
        normalized.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ConfigurationError(
            f"{operation_name}: credential field {field_name} must be ASCII."
        ) from exc

    return normalized


def _payload_preview(payload: Any, *, max_chars: int = 200) -> str:
    try:
        rendered = json.dumps(payload, default=str)
    except Exception:  # noqa: BLE001 - a preview must never replace the real error
        rendered = repr(payload)
    if len(rendered) <= max_chars:
        return rendered
    return f"{rendered[:max_chars]}..."


def _unusable_body(
    operation_name: str, method: str, path: str, problem: str, preview: str
) -> HTTPException:
    """A success status whose body the SDK cannot use: the 502 a gateway would give."""
    return HTTPException(
        status_code=502,
        message=f"{operation_name} returned {problem}",
        method=method.upper(),
        path=path,
        details={"response_preview": preview},
    )


def parse_response_model[ModelT: BaseModel](
    model_cls: type[ModelT],
    body: Any,
    *,
    operation_name: str,
    method: str,
    path: str,
) -> ModelT:
    if body is None:
        raise _unusable_body(operation_name, method, path, "a null body", "null")

    try:
        parsed = model_cls.model_validate(body)
    except ValidationError as exc:
        error = HTTPException(
            status_code=502,
            message=(
                f"{operation_name} returned data that does not match "
                f"{model_cls.__name__}"
            ),
            method=method.upper(),
            path=path,
            details={
                "model": model_cls.__name__,
                "validation_error": str(exc).splitlines()[0],
                "response_preview": _payload_preview(body),
            },
        )
        error.rate_limit = rate_limit_of(body)
        raise error from exc

    return attach_rate_limit(parsed, rate_limit_of(body))


def parse_response_model_list[ModelT: BaseModel](
    item_cls: type[ModelT],
    body: Any,
    *,
    operation_name: str,
    method: str,
    path: str,
) -> list[ModelT]:
    if body is None:
        raise _unusable_body(operation_name, method, path, "a null body", "null")

    if not isinstance(body, list):
        raise HTTPException(
            status_code=502,
            message=(
                f"{operation_name} returned data that does not match "
                "the expected list response"
            ),
            method=method.upper(),
            path=path,
            details={"response_preview": _payload_preview(body)},
        )

    parsed: list[ModelT] = []
    for index, item in enumerate(body):
        try:
            parsed.append(item_cls.model_validate(item))
        except ValidationError as exc:
            raise HTTPException(
                status_code=502,
                message=(
                    f"{operation_name} returned an invalid item at index {index} "
                    f"for {item_cls.__name__}"
                ),
                method=method.upper(),
                path=path,
                details={
                    "model": item_cls.__name__,
                    "index": index,
                    "validation_error": str(exc).splitlines()[0],
                    "item_preview": _payload_preview(item),
                },
            ) from exc

    return parsed


def path_segment(value: Any) -> str:
    """Encodes one path parameter so its value cannot leave its own segment.

    "/", "?" and "#" are percent-encoded, and the dot segments, which encoding
    cannot neutralize, are refused: `device.delete(deviceid="../../user/7")`
    must not delete a user.
    """
    segment = format(_wire_scalar(value))
    if segment in ("", ".", ".."):
        raise ValueError(f"{segment!r} is not a valid path parameter value")
    return quote(segment, safe=_PATH_SEGMENT_SAFE)


def request_json(
    method: str,
    path: str,
    *,
    path_template: str | None = None,
    api_config_override: APIConfig | None = None,
    query_params: dict[str, Any] | None = None,
    json_body: Any = None,
    header_params: dict[str, Any] | None = None,
    expected_status: int = 200,
    operation_name: str = "request",
    error_cls: type[HTTPException] = HTTPException,
) -> Any:
    """Shared REST request execution for generated service methods.

    `path_template` is the schema path, such as `/device/v1/device/{device.id}`.
    It keys the quota, so one endpoint keeps one entry whatever IDs it is called with.
    """
    api_config = api_config_override if api_config_override else APIConfig()
    if not api_config.auth_email or not api_config.auth_token:
        raise ConfigurationError(
            f"{operation_name}: the APIConfig for this call has no credentials. An "
            "api_config_override replaces the client's config entirely; build it "
            "with client.api_config.with_timeout(...) or pass auth_email and auth_token."
        )

    auth_email = _normalize_credential(
        "auth_email", api_config.auth_email, operation_name=operation_name
    )
    auth_token = _normalize_credential(
        "auth_token", api_config.auth_token, operation_name=operation_name
    )

    headers: dict[str, Any] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **auth_headers(auth_email, auth_token),
    }
    if header_params:
        headers.update(
            {
                header_name: header_value
                for (header_name, header_value) in header_params.items()
                if header_value is not None
            }
        )

    clean_query_params = {
        key: _wire_query_value(value)
        for (key, value) in (query_params or {}).items()
        if value is not None
    }
    # httpx writes a space as "+", which Envoy's transcoder does not decode by
    # default; "%20" means a space to every server. httpx still renders the values.
    query = urlencode(
        httpx.QueryParams(clean_query_params).multi_items(), quote_via=quote
    )

    started_at = time.monotonic()
    try:
        url = httpx.URL(path, query=query.encode()) if query else httpx.URL(path)
        client = api_config.client
        rest_timeout, deadline = api_config._rest_request_limits(started_at)
        extensions = {} if deadline is None else {DEADLINE_EXTENSION: deadline}
        response = client.request(
            method.lower(),
            url,
            headers=headers,
            json=json_body,
            timeout=rest_timeout,
            extensions=extensions,
        )
    except httpx.RequestError as exc:
        error = TransportError(
            f"{operation_name} transport failed ({type(exc).__name__}).",
        )
        if isinstance(
            exc,
            (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout),
        ):
            error.may_have_reached_server = False
        raise error from exc

    rate_limit = RateLimit.from_headers(response.headers)
    if rate_limit is not None:
        api_config.rate_limits[f"{method.upper()} {path_template or path}"] = rate_limit

    try:
        body = _handle_response(
            response,
            method=method,
            path=path,
            expected_status=expected_status,
            operation_name=operation_name,
            error_cls=error_cls,
        )
    except KentikError as exc:
        exc.rate_limit = rate_limit
        raise
    if deadline is not None:
        try:
            _check_deadline(deadline)
        except httpx.ReadTimeout as exc:
            raise TransportError(
                f"{operation_name} transport failed ({type(exc).__name__}).",
            ) from exc
    # A plain dict cannot hold an attribute; a subclass can, and the generated
    # function hands the quota on to the model it builds from this body.
    if isinstance(body, dict):
        body = attach_rate_limit(_ResponseBody(body), rate_limit)
    return body


class _ResponseBody(dict):
    """A parsed JSON object that can also carry the call's quota."""


def _handle_response(
    response: httpx.Response,
    *,
    method: str,
    path: str,
    expected_status: int,
    operation_name: str,
    error_cls: type[HTTPException],
) -> Any:
    def _raise_http_error(message: str, *, details: dict[str, Any]) -> None:
        error_factory = getattr(error_cls, "from_response", None)
        if callable(error_factory):
            built_error = error_factory(
                response,
                operation_name=operation_name,
                method=method.upper(),
                path=path,
            )
            if isinstance(built_error, BaseException):
                raise built_error

        raise error_cls(
            response.status_code,
            message,
            method=method.upper(),
            path=path,
            details=details,
        )

    if response.status_code != expected_status:
        preview = response.text[:200].replace("\n", " ")
        content_type = response.headers.get("content-type", "unknown")
        details: dict[str, Any] = {
            "method": method.upper(),
            "path": path,
            "content_type": content_type,
            "preview": preview,
        }
        message = (
            f"{operation_name} failed with status code: {response.status_code} "
            f"(method={method.upper()}, path={path}, content-type={content_type}, preview={preview!r})"
        )

        try:
            payload = response.json()
        except ValueError:
            payload = None

        if isinstance(payload, dict):
            details["response_json"] = payload
            if payload.get("code") is not None:
                details["code"] = payload.get("code")
            if payload.get("message"):
                message = str(payload.get("message"))
            elif isinstance(payload.get("error"), str) and payload["error"]:
                message = (
                    f"{operation_name} failed with status code: "
                    f"{response.status_code}: {payload['error']}"
                )
            if payload.get("details") is not None:
                details["details"] = payload.get("details")
        elif payload is not None:
            details["response_json"] = payload

        # Handled here, ahead of the generated error_cls, so REST raises the
        # same type gRPC does for UNAUTHENTICATED without regenerating errors.
        if response.status_code == 401:
            raise AuthenticationError(message)

        _raise_http_error(message, details=details)

    if expected_status == 204:
        return None

    try:
        return response.json()
    except ValueError:
        preview = response.text[:200].replace("\n", " ")
        content_type = response.headers.get("content-type", "unknown")
        raise _unusable_body(
            operation_name,
            method,
            path,
            f"a non-JSON body (content-type={content_type})",
            preview,
        ) from None
