# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class CapacityPlanError(HTTPException):
    """Base service-local error for the capacity_plan API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "CapacityPlanError":
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
    ) -> "CapacityPlanError":
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


class GetError(CapacityPlanError):
    """Operation-local error for client.capacity_plan.get()."""

    response_error_map: dict[str, type[CapacityPlanError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class GetCapacitySummaryError(CapacityPlanError):
    """Operation-local error for client.capacity_plan.get_capacity_summary()."""

    response_error_map: dict[str, type[CapacityPlanError]] = {}


class GetCapacitySummaryUnexpectedError(GetCapacitySummaryError):
    """Operation-local response error for get_capacity_summary (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetCapacitySummaryError.response_error_map = {
    "default": GetCapacitySummaryUnexpectedError,
}


class ListError(CapacityPlanError):
    """Operation-local error for client.capacity_plan.list()."""

    response_error_map: dict[str, type[CapacityPlanError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class ListCapacitySummariesError(CapacityPlanError):
    """Operation-local error for client.capacity_plan.list_capacity_summaries()."""

    response_error_map: dict[str, type[CapacityPlanError]] = {}


class ListCapacitySummariesUnexpectedError(ListCapacitySummariesError):
    """Operation-local response error for list_capacity_summaries (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListCapacitySummariesError.response_error_map = {
    "default": ListCapacitySummariesUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[CapacityPlanError]] = {
    "get": GetError,
    "get_capacity_summary": GetCapacitySummaryError,
    "list": ListError,
    "list_capacity_summaries": ListCapacitySummariesError,
}

__all__ = [
    "CapacityPlanError",
    "GetUnexpectedError",
    "GetCapacitySummaryUnexpectedError",
    "ListUnexpectedError",
    "ListCapacitySummariesUnexpectedError",
    "GetError",
    "GetCapacitySummaryError",
    "ListError",
    "ListCapacitySummariesError",
    "ERROR_BY_METHOD",
]
