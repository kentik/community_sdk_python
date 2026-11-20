# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class AssetTagsError(HTTPException):
    """Base service-local error for the asset_tags API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "AssetTagsError":
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
    ) -> "AssetTagsError":
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


class CreateTagKeyError(AssetTagsError):
    """Operation-local error for client.asset_tags.create_tag_key()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class CreateTagKeyUnexpectedError(CreateTagKeyError):
    """Operation-local response error for create_tag_key (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateTagKeyError.response_error_map = {
    "default": CreateTagKeyUnexpectedError,
}


class DeleteTagKeyError(AssetTagsError):
    """Operation-local error for client.asset_tags.delete_tag_key()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class DeleteTagKeyUnexpectedError(DeleteTagKeyError):
    """Operation-local response error for delete_tag_key (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteTagKeyError.response_error_map = {
    "default": DeleteTagKeyUnexpectedError,
}


class DeleteTagValuesError(AssetTagsError):
    """Operation-local error for client.asset_tags.delete_tag_values()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class DeleteTagValuesUnexpectedError(DeleteTagValuesError):
    """Operation-local response error for delete_tag_values (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteTagValuesError.response_error_map = {
    "default": DeleteTagValuesUnexpectedError,
}


class GetTagKeyError(AssetTagsError):
    """Operation-local error for client.asset_tags.get_tag_key()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class GetTagKeyUnexpectedError(GetTagKeyError):
    """Operation-local response error for get_tag_key (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetTagKeyError.response_error_map = {
    "default": GetTagKeyUnexpectedError,
}


class GetTagValuesError(AssetTagsError):
    """Operation-local error for client.asset_tags.get_tag_values()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class GetTagValuesUnexpectedError(GetTagValuesError):
    """Operation-local response error for get_tag_values (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetTagValuesError.response_error_map = {
    "default": GetTagValuesUnexpectedError,
}


class ListTagKeysError(AssetTagsError):
    """Operation-local error for client.asset_tags.list_tag_keys()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class ListTagKeysUnexpectedError(ListTagKeysError):
    """Operation-local response error for list_tag_keys (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListTagKeysError.response_error_map = {
    "default": ListTagKeysUnexpectedError,
}


class ListTagValuesError(AssetTagsError):
    """Operation-local error for client.asset_tags.list_tag_values()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class ListTagValuesUnexpectedError(ListTagValuesError):
    """Operation-local response error for list_tag_values (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListTagValuesError.response_error_map = {
    "default": ListTagValuesUnexpectedError,
}


class SetTagValuesError(AssetTagsError):
    """Operation-local error for client.asset_tags.set_tag_values()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class SetTagValuesUnexpectedError(SetTagValuesError):
    """Operation-local response error for set_tag_values (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SetTagValuesError.response_error_map = {
    "default": SetTagValuesUnexpectedError,
}


class UpdateTagKeyError(AssetTagsError):
    """Operation-local error for client.asset_tags.update_tag_key()."""

    response_error_map: dict[str, type[AssetTagsError]] = {}


class UpdateTagKeyUnexpectedError(UpdateTagKeyError):
    """Operation-local response error for update_tag_key (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateTagKeyError.response_error_map = {
    "default": UpdateTagKeyUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[AssetTagsError]] = {
    "create_tag_key": CreateTagKeyError,
    "delete_tag_key": DeleteTagKeyError,
    "delete_tag_values": DeleteTagValuesError,
    "get_tag_key": GetTagKeyError,
    "get_tag_values": GetTagValuesError,
    "list_tag_keys": ListTagKeysError,
    "list_tag_values": ListTagValuesError,
    "set_tag_values": SetTagValuesError,
    "update_tag_key": UpdateTagKeyError,
}

__all__ = [
    "AssetTagsError",
    "CreateTagKeyUnexpectedError",
    "DeleteTagKeyUnexpectedError",
    "DeleteTagValuesUnexpectedError",
    "GetTagKeyUnexpectedError",
    "GetTagValuesUnexpectedError",
    "ListTagKeysUnexpectedError",
    "ListTagValuesUnexpectedError",
    "SetTagValuesUnexpectedError",
    "UpdateTagKeyUnexpectedError",
    "CreateTagKeyError",
    "DeleteTagKeyError",
    "DeleteTagValuesError",
    "GetTagKeyError",
    "GetTagValuesError",
    "ListTagKeysError",
    "ListTagValuesError",
    "SetTagValuesError",
    "UpdateTagKeyError",
    "ERROR_BY_METHOD",
]
