# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class SiteError(HTTPException):
    """Base service-local error for the site API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "SiteError":
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
    ) -> "SiteError":
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


class CreateError(SiteError):
    """Operation-local error for client.site.create()."""

    response_error_map: dict[str, type[SiteError]] = {}


class CreateUnexpectedError(CreateError):
    """Operation-local response error for create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateError.response_error_map = {
    "default": CreateUnexpectedError,
}


class CreateMarketError(SiteError):
    """Operation-local error for client.site.create_market()."""

    response_error_map: dict[str, type[SiteError]] = {}


class CreateMarketUnexpectedError(CreateMarketError):
    """Operation-local response error for create_market (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateMarketError.response_error_map = {
    "default": CreateMarketUnexpectedError,
}


class DeleteError(SiteError):
    """Operation-local error for client.site.delete()."""

    response_error_map: dict[str, type[SiteError]] = {}


class DeleteUnexpectedError(DeleteError):
    """Operation-local response error for delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteError.response_error_map = {
    "default": DeleteUnexpectedError,
}


class DeleteMarketError(SiteError):
    """Operation-local error for client.site.delete_market()."""

    response_error_map: dict[str, type[SiteError]] = {}


class DeleteMarketUnexpectedError(DeleteMarketError):
    """Operation-local response error for delete_market (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteMarketError.response_error_map = {
    "default": DeleteMarketUnexpectedError,
}


class GetError(SiteError):
    """Operation-local error for client.site.get()."""

    response_error_map: dict[str, type[SiteError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class GetMarketError(SiteError):
    """Operation-local error for client.site.get_market()."""

    response_error_map: dict[str, type[SiteError]] = {}


class GetMarketUnexpectedError(GetMarketError):
    """Operation-local response error for get_market (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetMarketError.response_error_map = {
    "default": GetMarketUnexpectedError,
}


class ListError(SiteError):
    """Operation-local error for client.site.list()."""

    response_error_map: dict[str, type[SiteError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class ListMarketsError(SiteError):
    """Operation-local error for client.site.list_markets()."""

    response_error_map: dict[str, type[SiteError]] = {}


class ListMarketsUnexpectedError(ListMarketsError):
    """Operation-local response error for list_markets (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListMarketsError.response_error_map = {
    "default": ListMarketsUnexpectedError,
}


class UpdateError(SiteError):
    """Operation-local error for client.site.update()."""

    response_error_map: dict[str, type[SiteError]] = {}


class UpdateUnexpectedError(UpdateError):
    """Operation-local response error for update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateError.response_error_map = {
    "default": UpdateUnexpectedError,
}


class UpdateMarketError(SiteError):
    """Operation-local error for client.site.update_market()."""

    response_error_map: dict[str, type[SiteError]] = {}


class UpdateMarketUnexpectedError(UpdateMarketError):
    """Operation-local response error for update_market (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateMarketError.response_error_map = {
    "default": UpdateMarketUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[SiteError]] = {
    "create": CreateError,
    "create_market": CreateMarketError,
    "delete": DeleteError,
    "delete_market": DeleteMarketError,
    "get": GetError,
    "get_market": GetMarketError,
    "list": ListError,
    "list_markets": ListMarketsError,
    "update": UpdateError,
    "update_market": UpdateMarketError,
}

__all__ = [
    "SiteError",
    "CreateUnexpectedError",
    "CreateMarketUnexpectedError",
    "DeleteUnexpectedError",
    "DeleteMarketUnexpectedError",
    "GetUnexpectedError",
    "GetMarketUnexpectedError",
    "ListUnexpectedError",
    "ListMarketsUnexpectedError",
    "UpdateUnexpectedError",
    "UpdateMarketUnexpectedError",
    "CreateError",
    "CreateMarketError",
    "DeleteError",
    "DeleteMarketError",
    "GetError",
    "GetMarketError",
    "ListError",
    "ListMarketsError",
    "UpdateError",
    "UpdateMarketError",
    "ERROR_BY_METHOD",
]
