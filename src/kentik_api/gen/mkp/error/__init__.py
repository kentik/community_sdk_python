# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class MkpError(HTTPException):
    """Base service-local error for the mkp API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "MkpError":
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
    ) -> "MkpError":
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


class PackageCreateError(MkpError):
    """Operation-local error for client.mkp.package_create()."""

    response_error_map: dict[str, type[MkpError]] = {}


class PackageCreateUnexpectedError(PackageCreateError):
    """Operation-local response error for package_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PackageCreateError.response_error_map = {
    "default": PackageCreateUnexpectedError,
}


class PackageDeleteError(MkpError):
    """Operation-local error for client.mkp.package_delete()."""

    response_error_map: dict[str, type[MkpError]] = {}


class PackageDeleteUnexpectedError(PackageDeleteError):
    """Operation-local response error for package_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PackageDeleteError.response_error_map = {
    "default": PackageDeleteUnexpectedError,
}


class PackageGetError(MkpError):
    """Operation-local error for client.mkp.package_get()."""

    response_error_map: dict[str, type[MkpError]] = {}


class PackageGetUnexpectedError(PackageGetError):
    """Operation-local response error for package_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PackageGetError.response_error_map = {
    "default": PackageGetUnexpectedError,
}


class PackageListError(MkpError):
    """Operation-local error for client.mkp.package_list()."""

    response_error_map: dict[str, type[MkpError]] = {}


class PackageListUnexpectedError(PackageListError):
    """Operation-local response error for package_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PackageListError.response_error_map = {
    "default": PackageListUnexpectedError,
}


class PackageUpdateError(MkpError):
    """Operation-local error for client.mkp.package_update()."""

    response_error_map: dict[str, type[MkpError]] = {}


class PackageUpdateUnexpectedError(PackageUpdateError):
    """Operation-local response error for package_update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PackageUpdateError.response_error_map = {
    "default": PackageUpdateUnexpectedError,
}


class TenantCreateError(MkpError):
    """Operation-local error for client.mkp.tenant_create()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantCreateUnexpectedError(TenantCreateError):
    """Operation-local response error for tenant_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantCreateError.response_error_map = {
    "default": TenantCreateUnexpectedError,
}


class TenantDeleteError(MkpError):
    """Operation-local error for client.mkp.tenant_delete()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantDeleteUnexpectedError(TenantDeleteError):
    """Operation-local response error for tenant_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantDeleteError.response_error_map = {
    "default": TenantDeleteUnexpectedError,
}


class TenantGetError(MkpError):
    """Operation-local error for client.mkp.tenant_get()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantGetUnexpectedError(TenantGetError):
    """Operation-local response error for tenant_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantGetError.response_error_map = {
    "default": TenantGetUnexpectedError,
}


class TenantListError(MkpError):
    """Operation-local error for client.mkp.tenant_list()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantListUnexpectedError(TenantListError):
    """Operation-local response error for tenant_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantListError.response_error_map = {
    "default": TenantListUnexpectedError,
}


class TenantUpdateError(MkpError):
    """Operation-local error for client.mkp.tenant_update()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantUpdateUnexpectedError(TenantUpdateError):
    """Operation-local response error for tenant_update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantUpdateError.response_error_map = {
    "default": TenantUpdateUnexpectedError,
}


class TenantUserCreateError(MkpError):
    """Operation-local error for client.mkp.tenant_user_create()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantUserCreateUnexpectedError(TenantUserCreateError):
    """Operation-local response error for tenant_user_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantUserCreateError.response_error_map = {
    "default": TenantUserCreateUnexpectedError,
}


class TenantUserDeleteError(MkpError):
    """Operation-local error for client.mkp.tenant_user_delete()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantUserDeleteUnexpectedError(TenantUserDeleteError):
    """Operation-local response error for tenant_user_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantUserDeleteError.response_error_map = {
    "default": TenantUserDeleteUnexpectedError,
}


class TenantUserListError(MkpError):
    """Operation-local error for client.mkp.tenant_user_list()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantUserListUnexpectedError(TenantUserListError):
    """Operation-local response error for tenant_user_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantUserListError.response_error_map = {
    "default": TenantUserListUnexpectedError,
}


class TenantUserUpdateError(MkpError):
    """Operation-local error for client.mkp.tenant_user_update()."""

    response_error_map: dict[str, type[MkpError]] = {}


class TenantUserUpdateUnexpectedError(TenantUserUpdateError):
    """Operation-local response error for tenant_user_update (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


TenantUserUpdateError.response_error_map = {
    "default": TenantUserUpdateUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[MkpError]] = {
    "package_create": PackageCreateError,
    "package_delete": PackageDeleteError,
    "package_get": PackageGetError,
    "package_list": PackageListError,
    "package_update": PackageUpdateError,
    "tenant_create": TenantCreateError,
    "tenant_delete": TenantDeleteError,
    "tenant_get": TenantGetError,
    "tenant_list": TenantListError,
    "tenant_update": TenantUpdateError,
    "tenant_user_create": TenantUserCreateError,
    "tenant_user_delete": TenantUserDeleteError,
    "tenant_user_list": TenantUserListError,
    "tenant_user_update": TenantUserUpdateError,
}

__all__ = [
    "MkpError",
    "PackageCreateUnexpectedError",
    "PackageDeleteUnexpectedError",
    "PackageGetUnexpectedError",
    "PackageListUnexpectedError",
    "PackageUpdateUnexpectedError",
    "TenantCreateUnexpectedError",
    "TenantDeleteUnexpectedError",
    "TenantGetUnexpectedError",
    "TenantListUnexpectedError",
    "TenantUpdateUnexpectedError",
    "TenantUserCreateUnexpectedError",
    "TenantUserDeleteUnexpectedError",
    "TenantUserListUnexpectedError",
    "TenantUserUpdateUnexpectedError",
    "PackageCreateError",
    "PackageDeleteError",
    "PackageGetError",
    "PackageListError",
    "PackageUpdateError",
    "TenantCreateError",
    "TenantDeleteError",
    "TenantGetError",
    "TenantListError",
    "TenantUpdateError",
    "TenantUserCreateError",
    "TenantUserDeleteError",
    "TenantUserListError",
    "TenantUserUpdateError",
    "ERROR_BY_METHOD",
]
