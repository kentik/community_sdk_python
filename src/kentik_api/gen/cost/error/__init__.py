# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException


class CostError(HTTPException):
    """Base service-local error for the cost API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "CostError":
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
    ) -> "CostError":
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


class GetProviderSummaryError(CostError):
    """Operation-local error for client.cost.get_provider_summary()."""

    response_error_map: dict[str, type[CostError]] = {}


class GetProviderSummaryUnexpectedError(GetProviderSummaryError):
    """Operation-local response error for get_provider_summary (default: An unexpected error response. #/components/schemas/googlerpcStatus)."""

    pass


GetProviderSummaryError.response_error_map = {
    "default": GetProviderSummaryUnexpectedError,
}


class ListProviderSummariesError(CostError):
    """Operation-local error for client.cost.list_provider_summaries()."""

    response_error_map: dict[str, type[CostError]] = {}


class ListProviderSummariesUnexpectedError(ListProviderSummariesError):
    """Operation-local response error for list_provider_summaries (default: An unexpected error response. #/components/schemas/googlerpcStatus)."""

    pass


ListProviderSummariesError.response_error_map = {
    "default": ListProviderSummariesUnexpectedError,
}


class ListProvidersError(CostError):
    """Operation-local error for client.cost.list_providers()."""

    response_error_map: dict[str, type[CostError]] = {}


class ListProvidersUnexpectedError(ListProvidersError):
    """Operation-local response error for list_providers (default: An unexpected error response. #/components/schemas/googlerpcStatus)."""

    pass


ListProvidersError.response_error_map = {
    "default": ListProvidersUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[CostError]] = {
    "get_provider_summary": GetProviderSummaryError,
    "list_provider_summaries": ListProviderSummariesError,
    "list_providers": ListProvidersError,
}

__all__ = [
    "CostError",
    "GetProviderSummaryUnexpectedError",
    "ListProviderSummariesUnexpectedError",
    "ListProvidersUnexpectedError",
    "GetProviderSummaryError",
    "ListProviderSummariesError",
    "ListProvidersError",
    "ERROR_BY_METHOD",
]
