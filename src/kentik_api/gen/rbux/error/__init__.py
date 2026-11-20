# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class RbuxError(HTTPException):
    """Base service-local error for the rbux API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "RbuxError":
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
    ) -> "RbuxError":
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


class CreateScopeError(RbuxError):
    """Operation-local error for client.rbux.create_scope()."""

    response_error_map: dict[str, type[RbuxError]] = {}


class CreateScopeUnexpectedError(CreateScopeError):
    """Operation-local response error for create_scope (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateScopeError.response_error_map = {
    "default": CreateScopeUnexpectedError,
}


class DeleteScopeError(RbuxError):
    """Operation-local error for client.rbux.delete_scope()."""

    response_error_map: dict[str, type[RbuxError]] = {}


class DeleteScopeUnexpectedError(DeleteScopeError):
    """Operation-local response error for delete_scope (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteScopeError.response_error_map = {
    "default": DeleteScopeUnexpectedError,
}


class GetScopeError(RbuxError):
    """Operation-local error for client.rbux.get_scope()."""

    response_error_map: dict[str, type[RbuxError]] = {}


class GetScopeUnexpectedError(GetScopeError):
    """Operation-local response error for get_scope (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetScopeError.response_error_map = {
    "default": GetScopeUnexpectedError,
}


class ListScopesError(RbuxError):
    """Operation-local error for client.rbux.list_scopes()."""

    response_error_map: dict[str, type[RbuxError]] = {}


class ListScopesUnexpectedError(ListScopesError):
    """Operation-local response error for list_scopes (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListScopesError.response_error_map = {
    "default": ListScopesUnexpectedError,
}


class UpdateScopeError(RbuxError):
    """Operation-local error for client.rbux.update_scope()."""

    response_error_map: dict[str, type[RbuxError]] = {}


class UpdateScopeUnexpectedError(UpdateScopeError):
    """Operation-local response error for update_scope (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateScopeError.response_error_map = {
    "default": UpdateScopeUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[RbuxError]] = {
    "create_scope": CreateScopeError,
    "delete_scope": DeleteScopeError,
    "get_scope": GetScopeError,
    "list_scopes": ListScopesError,
    "update_scope": UpdateScopeError,
}

__all__ = [
    "RbuxError",
    "CreateScopeUnexpectedError",
    "DeleteScopeUnexpectedError",
    "GetScopeUnexpectedError",
    "ListScopesUnexpectedError",
    "UpdateScopeUnexpectedError",
    "CreateScopeError",
    "DeleteScopeError",
    "GetScopeError",
    "ListScopesError",
    "UpdateScopeError",
    "ERROR_BY_METHOD",
]
