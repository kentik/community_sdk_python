# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class CredentialError(HTTPException):
    """Base service-local error for the credential API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "CredentialError":
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
    ) -> "CredentialError":
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


class AssignConsumerError(CredentialError):
    """Operation-local error for client.credential.assign_consumer()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class AssignConsumerUnexpectedError(AssignConsumerError):
    """Operation-local response error for assign_consumer (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AssignConsumerError.response_error_map = {
    "default": AssignConsumerUnexpectedError,
}


class CreateGroupError(CredentialError):
    """Operation-local error for client.credential.create_group()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class CreateGroupUnexpectedError(CreateGroupError):
    """Operation-local response error for create_group (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateGroupError.response_error_map = {
    "default": CreateGroupUnexpectedError,
}


class DeleteError(CredentialError):
    """Operation-local error for client.credential.delete()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class DeleteUnexpectedError(DeleteError):
    """Operation-local response error for delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteError.response_error_map = {
    "default": DeleteUnexpectedError,
}


class DeleteGroupError(CredentialError):
    """Operation-local error for client.credential.delete_group()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class DeleteGroupUnexpectedError(DeleteGroupError):
    """Operation-local response error for delete_group (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteGroupError.response_error_map = {
    "default": DeleteGroupUnexpectedError,
}


class GetError(CredentialError):
    """Operation-local error for client.credential.get()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class GetGroupError(CredentialError):
    """Operation-local error for client.credential.get_group()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class GetGroupUnexpectedError(GetGroupError):
    """Operation-local response error for get_group (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetGroupError.response_error_map = {
    "default": GetGroupUnexpectedError,
}


class ListError(CredentialError):
    """Operation-local error for client.credential.list()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class ListGroupError(CredentialError):
    """Operation-local error for client.credential.list_group()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class ListGroupUnexpectedError(ListGroupError):
    """Operation-local response error for list_group (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListGroupError.response_error_map = {
    "default": ListGroupUnexpectedError,
}


class ListOverviewsError(CredentialError):
    """Operation-local error for client.credential.list_overviews()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class ListOverviewsUnexpectedError(ListOverviewsError):
    """Operation-local response error for list_overviews (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListOverviewsError.response_error_map = {
    "default": ListOverviewsUnexpectedError,
}


class UpdateGroupError(CredentialError):
    """Operation-local error for client.credential.update_group()."""

    response_error_map: dict[str, type[CredentialError]] = {}


class UpdateGroupUnexpectedError(UpdateGroupError):
    """Operation-local response error for update_group (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateGroupError.response_error_map = {
    "default": UpdateGroupUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[CredentialError]] = {
    "assign_consumer": AssignConsumerError,
    "create_group": CreateGroupError,
    "delete": DeleteError,
    "delete_group": DeleteGroupError,
    "get": GetError,
    "get_group": GetGroupError,
    "list": ListError,
    "list_group": ListGroupError,
    "list_overviews": ListOverviewsError,
    "update_group": UpdateGroupError,
}

__all__ = [
    "CredentialError",
    "AssignConsumerUnexpectedError",
    "CreateGroupUnexpectedError",
    "DeleteUnexpectedError",
    "DeleteGroupUnexpectedError",
    "GetUnexpectedError",
    "GetGroupUnexpectedError",
    "ListUnexpectedError",
    "ListGroupUnexpectedError",
    "ListOverviewsUnexpectedError",
    "UpdateGroupUnexpectedError",
    "AssignConsumerError",
    "CreateGroupError",
    "DeleteError",
    "DeleteGroupError",
    "GetError",
    "GetGroupError",
    "ListError",
    "ListGroupError",
    "ListOverviewsError",
    "UpdateGroupError",
    "ERROR_BY_METHOD",
]
