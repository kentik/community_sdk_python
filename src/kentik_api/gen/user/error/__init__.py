# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class UserError(HTTPException):
    """Base service-local error for the user API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "UserError":
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
    ) -> "UserError":
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


class CreateError(UserError):
    """Operation-local error for client.user.create()."""

    response_error_map: dict[str, type[UserError]] = {}


class CreateUnexpectedError(CreateError):
    """Operation-local response error for create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateError.response_error_map = {
    "default": CreateUnexpectedError,
}


class DeleteError(UserError):
    """Operation-local error for client.user.delete()."""

    response_error_map: dict[str, type[UserError]] = {}


class DeleteUnexpectedError(DeleteError):
    """Operation-local response error for delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteError.response_error_map = {
    "default": DeleteUnexpectedError,
}


class GetError(UserError):
    """Operation-local error for client.user.get()."""

    response_error_map: dict[str, type[UserError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class ListError(UserError):
    """Operation-local error for client.user.list()."""

    response_error_map: dict[str, type[UserError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class ResetActiveSessionsError(UserError):
    """Operation-local error for client.user.reset_active_sessions()."""

    response_error_map: dict[str, type[UserError]] = {}


class ResetActiveSessionsUnexpectedError(ResetActiveSessionsError):
    """Operation-local response error for reset_active_sessions (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ResetActiveSessionsError.response_error_map = {
    "default": ResetActiveSessionsUnexpectedError,
}


class ResetApiTokenError(UserError):
    """Operation-local error for client.user.reset_api_token()."""

    response_error_map: dict[str, type[UserError]] = {}


class ResetApiTokenUnexpectedError(ResetApiTokenError):
    """Operation-local response error for reset_api_token (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ResetApiTokenError.response_error_map = {
    "default": ResetApiTokenUnexpectedError,
}


class UpdateError(UserError):
    """Operation-local error for client.user.update()."""

    response_error_map: dict[str, type[UserError]] = {}


class UpdateUnexpectedError(UpdateError):
    """Operation-local response error for update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateError.response_error_map = {
    "default": UpdateUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[UserError]] = {
    "create": CreateError,
    "delete": DeleteError,
    "get": GetError,
    "list": ListError,
    "reset_active_sessions": ResetActiveSessionsError,
    "reset_api_token": ResetApiTokenError,
    "update": UpdateError,
}

__all__ = [
    "UserError",
    "CreateUnexpectedError",
    "DeleteUnexpectedError",
    "GetUnexpectedError",
    "ListUnexpectedError",
    "ResetActiveSessionsUnexpectedError",
    "ResetApiTokenUnexpectedError",
    "UpdateUnexpectedError",
    "CreateError",
    "DeleteError",
    "GetError",
    "ListError",
    "ResetActiveSessionsError",
    "ResetApiTokenError",
    "UpdateError",
    "ERROR_BY_METHOD",
]
