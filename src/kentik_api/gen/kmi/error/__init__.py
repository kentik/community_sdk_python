# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class KmiError(HTTPException):
    """Base service-local error for the kmi API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "KmiError":
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
    ) -> "KmiError":
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


class GetAsnDetailsError(KmiError):
    """Operation-local error for client.kmi.get_asn_details()."""

    response_error_map: dict[str, type[KmiError]] = {}


class GetAsnDetailsUnexpectedError(GetAsnDetailsError):
    """Operation-local response error for get_asn_details (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAsnDetailsError.response_error_map = {
    "default": GetAsnDetailsUnexpectedError,
}


class GetAsnInsightsError(KmiError):
    """Operation-local error for client.kmi.get_asn_insights()."""

    response_error_map: dict[str, type[KmiError]] = {}


class GetAsnInsightsUnexpectedError(GetAsnInsightsError):
    """Operation-local response error for get_asn_insights (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAsnInsightsError.response_error_map = {
    "default": GetAsnInsightsUnexpectedError,
}


class GetGlobalInsightsError(KmiError):
    """Operation-local error for client.kmi.get_global_insights()."""

    response_error_map: dict[str, type[KmiError]] = {}


class GetGlobalInsightsUnexpectedError(GetGlobalInsightsError):
    """Operation-local response error for get_global_insights (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetGlobalInsightsError.response_error_map = {
    "default": GetGlobalInsightsUnexpectedError,
}


class GetRankingsError(KmiError):
    """Operation-local error for client.kmi.get_rankings()."""

    response_error_map: dict[str, type[KmiError]] = {}


class GetRankingsUnexpectedError(GetRankingsError):
    """Operation-local response error for get_rankings (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetRankingsError.response_error_map = {
    "default": GetRankingsUnexpectedError,
}


class ListMarketsError(KmiError):
    """Operation-local error for client.kmi.list_markets()."""

    response_error_map: dict[str, type[KmiError]] = {}


class ListMarketsUnexpectedError(ListMarketsError):
    """Operation-local response error for list_markets (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListMarketsError.response_error_map = {
    "default": ListMarketsUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[KmiError]] = {
    "get_asn_details": GetAsnDetailsError,
    "get_asn_insights": GetAsnInsightsError,
    "get_global_insights": GetGlobalInsightsError,
    "get_rankings": GetRankingsError,
    "list_markets": ListMarketsError,
}

__all__ = [
    "KmiError",
    "GetAsnDetailsUnexpectedError",
    "GetAsnInsightsUnexpectedError",
    "GetGlobalInsightsUnexpectedError",
    "GetRankingsUnexpectedError",
    "ListMarketsUnexpectedError",
    "GetAsnDetailsError",
    "GetAsnInsightsError",
    "GetGlobalInsightsError",
    "GetRankingsError",
    "ListMarketsError",
    "ERROR_BY_METHOD",
]
