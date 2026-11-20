# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class EnrichmentsError(HTTPException):
    """Base service-local error for the enrichments API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "EnrichmentsError":
        preview = getattr(response, "text", "")[:200].replace("\n", " ")
        headers = getattr(response, "headers", {})
        content_type = (
            headers.get("content-type", "unknown")
            if hasattr(headers, "get")
            else "unknown"
        )
        details: dict[str, Any] = {
            "content_type": content_type,
            "preview": preview,
        }
        message = f"{operation_name} failed with status code: {getattr(response, 'status_code', 'unknown')}"
        try:
            payload = response.json()
        except Exception:
            payload = None
        if isinstance(payload, dict):
            details["response_json"] = payload
            if isinstance(payload.get("error"), str) and payload["error"]:
                message = f"{message}: {payload['error']}"
            try:
                status = rpcStatus.model_validate(payload)
            except Exception:
                status = None
            if status is not None:
                details["rpc_status"] = payload
                if status.code is not None:
                    details["rpc_status_code"] = status.code
                if status.message:
                    message = status.message
                else:
                    message = payload.get("message") or message
            else:
                message = payload.get("message") or message
        elif payload is not None:
            details["response_json"] = payload
        return cls(
            getattr(response, "status_code", 500),
            message,
            method=method,
            path=path,
            details=details,
        )

    @classmethod
    def from_response(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "EnrichmentsError":
        status_key = str(getattr(response, "status_code", ""))
        response_error_map = getattr(cls, "response_error_map", {})
        target_cls = (
            response_error_map.get(status_key)
            or response_error_map.get("default")
            or cls
        )
        return target_cls._build_error(
            response,
            operation_name=operation_name,
            method=method,
            path=path,
        )


class FetchValuesByIdsError(EnrichmentsError):
    """Operation-local error for client.enrichments.fetch_values_by_ids()."""

    response_error_map: dict[str, type[EnrichmentsError]] = {}


class FetchValuesByIdsUnexpectedError(FetchValuesByIdsError):
    """Operation-local response error for fetch_values_by_ids (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


FetchValuesByIdsError.response_error_map = {
    "default": FetchValuesByIdsUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[EnrichmentsError]] = {
    "fetch_values_by_ids": FetchValuesByIdsError,
}

__all__ = [
    "EnrichmentsError",
    "FetchValuesByIdsUnexpectedError",
    "FetchValuesByIdsError",
    "ERROR_BY_METHOD",
]
