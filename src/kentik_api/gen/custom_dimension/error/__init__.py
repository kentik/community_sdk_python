# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class CustomDimensionError(HTTPException):
    """Base service-local error for the custom_dimension API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "CustomDimensionError":
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
    ) -> "CustomDimensionError":
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


class CreateError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.create()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class CreateUnexpectedError(CreateError):
    """Operation-local response error for create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateError.response_error_map = {
    "default": CreateUnexpectedError,
}


class CreatePopulatorError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.create_populator()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class CreatePopulatorUnexpectedError(CreatePopulatorError):
    """Operation-local response error for create_populator (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreatePopulatorError.response_error_map = {
    "default": CreatePopulatorUnexpectedError,
}


class DeleteError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.delete()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class DeleteUnexpectedError(DeleteError):
    """Operation-local response error for delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteError.response_error_map = {
    "default": DeleteUnexpectedError,
}


class DeletePopulatorError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.delete_populator()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class DeletePopulatorUnexpectedError(DeletePopulatorError):
    """Operation-local response error for delete_populator (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeletePopulatorError.response_error_map = {
    "default": DeletePopulatorUnexpectedError,
}


class GetInfoError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.get_info()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class GetInfoUnexpectedError(GetInfoError):
    """Operation-local response error for get_info (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetInfoError.response_error_map = {
    "default": GetInfoUnexpectedError,
}


class GetPopulatorError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.get_populator()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class GetPopulatorUnexpectedError(GetPopulatorError):
    """Operation-local response error for get_populator (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetPopulatorError.response_error_map = {
    "default": GetPopulatorUnexpectedError,
}


class GetPopulatorFieldError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.get_populator_field()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class GetPopulatorFieldUnexpectedError(GetPopulatorFieldError):
    """Operation-local response error for get_populator_field (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetPopulatorFieldError.response_error_map = {
    "default": GetPopulatorFieldUnexpectedError,
}


class ListError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.list()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class UpdateError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.update()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class UpdateUnexpectedError(UpdateError):
    """Operation-local response error for update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateError.response_error_map = {
    "default": UpdateUnexpectedError,
}


class UpdatePopulatorError(CustomDimensionError):
    """Operation-local error for client.custom_dimension.update_populator()."""

    response_error_map: dict[str, type[CustomDimensionError]] = {}


class UpdatePopulatorUnexpectedError(UpdatePopulatorError):
    """Operation-local response error for update_populator (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdatePopulatorError.response_error_map = {
    "default": UpdatePopulatorUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[CustomDimensionError]] = {
    "create": CreateError,
    "create_populator": CreatePopulatorError,
    "delete": DeleteError,
    "delete_populator": DeletePopulatorError,
    "get_info": GetInfoError,
    "get_populator": GetPopulatorError,
    "get_populator_field": GetPopulatorFieldError,
    "list": ListError,
    "update": UpdateError,
    "update_populator": UpdatePopulatorError,
}

__all__ = [
    "CustomDimensionError",
    "CreateUnexpectedError",
    "CreatePopulatorUnexpectedError",
    "DeleteUnexpectedError",
    "DeletePopulatorUnexpectedError",
    "GetInfoUnexpectedError",
    "GetPopulatorUnexpectedError",
    "GetPopulatorFieldUnexpectedError",
    "ListUnexpectedError",
    "UpdateUnexpectedError",
    "UpdatePopulatorUnexpectedError",
    "CreateError",
    "CreatePopulatorError",
    "DeleteError",
    "DeletePopulatorError",
    "GetInfoError",
    "GetPopulatorError",
    "GetPopulatorFieldError",
    "ListError",
    "UpdateError",
    "UpdatePopulatorError",
    "ERROR_BY_METHOD",
]
