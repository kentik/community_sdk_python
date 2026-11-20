# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class AiAdvisorError(HTTPException):
    """Base service-local error for the ai_advisor API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "AiAdvisorError":
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
    ) -> "AiAdvisorError":
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


class CreateChatSessionError(AiAdvisorError):
    """Operation-local error for client.ai_advisor.create_chat_session()."""

    response_error_map: dict[str, type[AiAdvisorError]] = {}


class CreateChatSessionUnexpectedError(CreateChatSessionError):
    """Operation-local response error for create_chat_session (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateChatSessionError.response_error_map = {
    "default": CreateChatSessionUnexpectedError,
}


class GetChatSessionError(AiAdvisorError):
    """Operation-local error for client.ai_advisor.get_chat_session()."""

    response_error_map: dict[str, type[AiAdvisorError]] = {}


class GetChatSessionUnexpectedError(GetChatSessionError):
    """Operation-local response error for get_chat_session (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetChatSessionError.response_error_map = {
    "default": GetChatSessionUnexpectedError,
}


class UpdateChatSessionError(AiAdvisorError):
    """Operation-local error for client.ai_advisor.update_chat_session()."""

    response_error_map: dict[str, type[AiAdvisorError]] = {}


class UpdateChatSessionUnexpectedError(UpdateChatSessionError):
    """Operation-local response error for update_chat_session (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateChatSessionError.response_error_map = {
    "default": UpdateChatSessionUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[AiAdvisorError]] = {
    "create_chat_session": CreateChatSessionError,
    "get_chat_session": GetChatSessionError,
    "update_chat_session": UpdateChatSessionError,
}

__all__ = [
    "AiAdvisorError",
    "CreateChatSessionUnexpectedError",
    "GetChatSessionUnexpectedError",
    "UpdateChatSessionUnexpectedError",
    "CreateChatSessionError",
    "GetChatSessionError",
    "UpdateChatSessionError",
    "ERROR_BY_METHOD",
]
