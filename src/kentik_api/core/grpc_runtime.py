# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Shared gRPC call helper: the gRPC analogue of rest_runtime.request_json.

Every generated gRPC wrapper method routes through call_grpc so error
handling, status-code mapping, and transport failures stay in one place.
"""

from collections.abc import Iterable
from typing import Any, cast

import grpc
from google.protobuf.json_format import MessageToDict, ParseDict, ParseError
from google.protobuf.message import DecodeError
from google.rpc import (
    error_details_pb2 as _error_details_pb2,  # noqa: F401  registers the standard detail types
)
from google.rpc import status_pb2
from pydantic import BaseModel

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rate_limit import RateLimit, attach_rate_limit, rate_limit_of_rpc
from kentik_api.core.rest_runtime import parse_response_model
from kentik_api.errors import (
    AuthenticationError,
    ConfigurationError,
    HTTPException,
    TransportError,
)

_GRPC_STATUS_TO_HTTP: dict[grpc.StatusCode, int] = {
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.FAILED_PRECONDITION: 400,
    grpc.StatusCode.OUT_OF_RANGE: 400,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.ABORTED: 409,
    grpc.StatusCode.RESOURCE_EXHAUSTED: 429,
    grpc.StatusCode.UNKNOWN: 500,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.DATA_LOSS: 500,
    grpc.StatusCode.UNIMPLEMENTED: 501,
}

_NO_RESPONSE_CODES: frozenset[grpc.StatusCode] = frozenset(
    {
        grpc.StatusCode.CANCELLED,
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.UNAVAILABLE,
    }
)

_STATUS_DETAILS_KEY = "grpc-status-details-bin"


def _rpc_status(exc: grpc.RpcError) -> dict[str, Any] | None:
    """The google.rpc.Status a server sent, in the JSON form REST's error body has."""
    try:
        trailers = cast(
            Iterable[tuple[str, Any]],
            exc.trailing_metadata() or (),  # ty: ignore[missing-attribute]
        )
        raw = next((v for k, v in trailers if k == _STATUS_DETAILS_KEY), None)
        if not isinstance(raw, bytes):
            return None
        status = status_pb2.Status.FromString(raw)
    except (AttributeError, DecodeError, TypeError, ValueError):
        return None
    details = []
    for detail in status.details:
        try:
            details.append(MessageToDict(detail))
        except (KeyError, TypeError):
            details.append({"@type": detail.type_url})
    return {"code": status.code, "message": status.message, "details": details}


def map_grpc_error(
    exc: grpc.RpcError,
    *,
    method: str = "gRPC",
    path: str = "unknown",
) -> AuthenticationError | HTTPException | TransportError:
    """Maps a gRPC RpcError to the SDK exception hierarchy.

    Pure function: no I/O, no side effects. Testable without a gRPC channel.
    """
    code = exc.code()  # ty: ignore[missing-attribute]  # grpcio ships no stubs
    details = exc.details() or ""  # ty: ignore[missing-attribute]
    code_name = getattr(code, "name", repr(code))

    if code == grpc.StatusCode.UNAUTHENTICATED:
        return AuthenticationError(details)
    if code == grpc.StatusCode.RESOURCE_EXHAUSTED and "larger than max" in details:
        # Raised by the client when a response exceeds the receive limit. It is
        # not Kentik's quota, so it must not read as a 429 that callers back off on.
        return TransportError(
            f"{method} {path} response exceeded the gRPC receive limit: {details}. "
            "Pass grpc_options=[('grpc.max_receive_message_length', N)] to KentikAPI, "
            "or use protocol='rest'."
        )
    if code in _NO_RESPONSE_CODES:
        return TransportError(f"{method} {path} failed with {code_name}: {details}")

    http_status = _GRPC_STATUS_TO_HTTP.get(code)
    if http_status is None:
        return TransportError(
            f"{method} {path} failed with unrecognized gRPC status {code_name}: {details}"
        )
    status = _rpc_status(exc)
    return HTTPException(
        status_code=http_status,
        message=details,
        method=method,
        path=path,
        details=None
        if status is None
        else {"rpc_status": status, "rpc_status_code": status["code"]},
        grpc_status_code=code_name,
    )


def _mask_paths(message: Any, sent: dict[str, Any], prefix: str = "") -> list[str]:
    """The field paths a JSON body sets, as grpc-gateway's FieldMaskFromRequestBody."""
    fields = message.DESCRIPTOR.fields_by_name
    by_json = {field.json_name: field for field in fields.values()}
    paths: list[str] = []
    for key, value in sent.items():
        field = by_json.get(key) or fields.get(key)
        if field is None:
            continue
        path = f"{prefix}{field.name}"
        nested = field.message_type
        if (
            isinstance(value, dict)
            and value
            and nested is not None
            and not nested.GetOptions().map_entry
            and not nested.full_name.startswith("google.protobuf.")
        ):
            paths += _mask_paths(getattr(message, field.name), value, f"{path}.")
        else:
            paths.append(path)
    return paths


def build_grpc_request(
    message_cls,
    body: dict[str, Any] | None,
    fields: dict[str, Any],
    update_mask_from: str | None = None,
) -> Any:
    """Builds a request message the way grpc-gateway transcodes the REST call.

    `body` is the REST request body, already nested under the field the RPC's
    HTTP rule names. `fields` maps each path and query parameter's dotted field
    path (for example "device.id") to its value; None means unset. Both must
    resolve: an unknown body key or enum name would otherwise be dropped, and a
    full-replace update would then blank the field it was meant to set.

    `update_mask_from` names the body field of a PATCH whose request has an
    `update_mask`. grpc-gateway fills an unset mask from the keys sent there,
    and an empty mask on gRPC would replace every field instead.
    """
    nested: dict[str, Any] = {}
    for field_path, value in fields.items():
        if value is None:
            continue
        *parents, leaf = field_path.split(".")
        node = nested
        for parent in parents:
            node = node.setdefault(parent, {})
        node[leaf] = value
    try:
        request = ParseDict(body or {}, message_cls())
        request = ParseDict(nested, request)
    except ParseError as exc:
        raise ConfigurationError(
            f"Invalid argument for {message_cls.DESCRIPTOR.name}: {exc}"
        ) from exc
    if update_mask_from:
        sent = (body or {}).get(update_mask_from)
        if isinstance(sent, dict) and not request.update_mask.paths:
            request.update_mask.paths.extend(
                _mask_paths(getattr(request, update_mask_from), sent)
            )
    return request


def _method_label(stub_method) -> str:
    # Best effort: `_method` is a grpcio implementation detail, and failing to
    # read it must never cost the caller the RpcError it was meant to describe.
    try:
        label = stub_method._method
    except Exception:  # noqa: BLE001 - see the comment above
        return "unknown"
    if isinstance(label, bytes):
        return label.decode("utf-8", errors="replace")
    return str(label)


def _validate_grpc_override(api_config: APIConfig) -> None:
    if not api_config.is_timeout_copy:
        raise ConfigurationError(
            "gRPC api_config_override must come from client.api_config.with_timeout(...). "
            "Per-call credential, host, or verify overrides are not supported on gRPC."
        )


def _as_operation_error(
    error: HTTPException, error_cls: type[HTTPException]
) -> HTTPException:
    """Re-types a mapped gRPC error as the operation's own class, as REST does.

    REST picks the response class from the HTTP status, so an `except
    ListError` clause catches the same error on either transport.
    """
    by_status = getattr(error_cls, "response_error_map", {})
    target = by_status.get(str(error.status_code)) or by_status.get("default")
    return (target or error_cls)(
        error.status_code,
        error.message,
        method=error.method,
        path=error.path,
        details=error.details,
        grpc_status_code=error.grpc_status_code,
    )


def grpc_response_body(response: Any) -> dict[str, Any]:
    """The proto3 JSON a REST call returns for the same message."""
    return MessageToDict(response, always_print_fields_with_no_presence=True)


def parse_grpc_response[T: BaseModel](
    model_cls: type[T],
    response: Any,
    rate_limit: RateLimit | None,
    *,
    stub_method: Any,
    operation_name: str,
) -> T:
    """Validates a gRPC response into the REST model, as REST validates its body.

    A response the model rejects, such as an enum value newer than this SDK,
    raises the same HTTPException 502 on both transports.
    """
    # Without always_print_fields_with_no_presence, a scalar at its zero value
    # is omitted and then fails a model that marks the field required.
    body = grpc_response_body(response)
    try:
        parsed = parse_response_model(
            model_cls,
            body,
            operation_name=operation_name,
            method="gRPC",
            path=_method_label(stub_method),
        )
    except HTTPException as exc:
        exc.rate_limit = rate_limit
        raise
    return attach_rate_limit(parsed, rate_limit)


def call_grpc(
    stub_method,
    proto_request,
    *,
    api_config: APIConfig | None = None,
    error_cls: type[HTTPException] | None = None,
) -> tuple[Any, RateLimit | None]:
    """Calls one unary gRPC method; returns the response and the quota it reported.

    Only grpc.RpcError is a transport outcome. Anything else the stub raises,
    such as a malformed request, propagates unchanged rather than being
    misreported as a network failure.

    `api_config` is a per-call override: its grpc_deadline bounds this call,
    ahead of the channel's default. An override that with_timeout() did not
    build raises ConfigurationError, because the channel binds its credentials
    and host once.
    """
    path = _method_label(stub_method)
    if api_config is not None:
        _validate_grpc_override(api_config)

    kwargs: dict[str, Any] = (
        {} if api_config is None else {"timeout": api_config.grpc_deadline}
    )
    try:
        # A future, unlike with_call, lets the channel end a call that it sends
        # without a deadline (grpc_client._NO_SERVER_DEADLINE). It also exposes
        # the call's initial metadata, where the quota is.
        if isinstance(stub_method, grpc.UnaryUnaryMultiCallable):
            call = stub_method.future(proto_request, **kwargs)
            return call.result(), rate_limit_of_rpc(call)
        return stub_method(proto_request, **kwargs), None
    except grpc.FutureCancelledError as exc:
        raise TransportError(
            f"gRPC {path} failed with DEADLINE_EXCEEDED: no response within the deadline"
        ) from exc
    except grpc.RpcError as exc:
        error = map_grpc_error(exc, method="gRPC", path=path)
        if error_cls is not None and isinstance(error, HTTPException):
            error = _as_operation_error(error, error_cls)
        error.rate_limit = rate_limit_of_rpc(exc)
        raise error from exc
