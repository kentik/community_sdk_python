# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class DeviceError(HTTPException):
    """Base service-local error for the device API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "DeviceError":
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
    ) -> "DeviceError":
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


class CreateError(DeviceError):
    """Operation-local error for client.device.create()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class CreateUnexpectedError(CreateError):
    """Operation-local response error for create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateError.response_error_map = {
    "default": CreateUnexpectedError,
}


class CreateBulkError(DeviceError):
    """Operation-local error for client.device.create_bulk()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class CreateBulkUnexpectedError(CreateBulkError):
    """Operation-local response error for create_bulk (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateBulkError.response_error_map = {
    "default": CreateBulkUnexpectedError,
}


class DeleteError(DeviceError):
    """Operation-local error for client.device.delete()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class DeleteUnexpectedError(DeleteError):
    """Operation-local response error for delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteError.response_error_map = {
    "default": DeleteUnexpectedError,
}


class DeleteBulkError(DeviceError):
    """Operation-local error for client.device.delete_bulk()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class DeleteBulkUnexpectedError(DeleteBulkError):
    """Operation-local response error for delete_bulk (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteBulkError.response_error_map = {
    "default": DeleteBulkUnexpectedError,
}


class GetError(DeviceError):
    """Operation-local error for client.device.get()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class GetByNameError(DeviceError):
    """Operation-local error for client.device.get_by_name()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class GetByNameUnexpectedError(GetByNameError):
    """Operation-local response error for get_by_name (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetByNameError.response_error_map = {
    "default": GetByNameUnexpectedError,
}


class ListError(DeviceError):
    """Operation-local error for client.device.list()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class UpdateError(DeviceError):
    """Operation-local error for client.device.update()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class UpdateUnexpectedError(UpdateError):
    """Operation-local response error for update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateError.response_error_map = {
    "default": UpdateUnexpectedError,
}


class UpdateBulkError(DeviceError):
    """Operation-local error for client.device.update_bulk()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class UpdateBulkUnexpectedError(UpdateBulkError):
    """Operation-local response error for update_bulk (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateBulkError.response_error_map = {
    "default": UpdateBulkUnexpectedError,
}


class UpdateLabelsError(DeviceError):
    """Operation-local error for client.device.update_labels()."""

    response_error_map: dict[str, type[DeviceError]] = {}


class UpdateLabelsUnexpectedError(UpdateLabelsError):
    """Operation-local response error for update_labels (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateLabelsError.response_error_map = {
    "default": UpdateLabelsUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[DeviceError]] = {
    "create": CreateError,
    "create_bulk": CreateBulkError,
    "delete": DeleteError,
    "delete_bulk": DeleteBulkError,
    "get": GetError,
    "get_by_name": GetByNameError,
    "list": ListError,
    "update": UpdateError,
    "update_bulk": UpdateBulkError,
    "update_labels": UpdateLabelsError,
}

__all__ = [
    "DeviceError",
    "CreateUnexpectedError",
    "CreateBulkUnexpectedError",
    "DeleteUnexpectedError",
    "DeleteBulkUnexpectedError",
    "GetUnexpectedError",
    "GetByNameUnexpectedError",
    "ListUnexpectedError",
    "UpdateUnexpectedError",
    "UpdateBulkUnexpectedError",
    "UpdateLabelsUnexpectedError",
    "CreateError",
    "CreateBulkError",
    "DeleteError",
    "DeleteBulkError",
    "GetError",
    "GetByNameError",
    "ListError",
    "UpdateError",
    "UpdateBulkError",
    "UpdateLabelsError",
    "ERROR_BY_METHOD",
]
