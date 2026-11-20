# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class BgpMonitoringError(HTTPException):
    """Base service-local error for the bgp_monitoring API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "BgpMonitoringError":
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
    ) -> "BgpMonitoringError":
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


class CreateMonitorError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.create_monitor()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class CreateMonitorUnexpectedError(CreateMonitorError):
    """Operation-local response error for create_monitor (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateMonitorError.response_error_map = {
    "default": CreateMonitorUnexpectedError,
}


class DeleteMonitorError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.delete_monitor()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class DeleteMonitorUnexpectedError(DeleteMonitorError):
    """Operation-local response error for delete_monitor (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteMonitorError.response_error_map = {
    "default": DeleteMonitorUnexpectedError,
}


class GetMetricsForTargetError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.get_metrics_for_target()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class GetMetricsForTargetUnexpectedError(GetMetricsForTargetError):
    """Operation-local response error for get_metrics_for_target (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetMetricsForTargetError.response_error_map = {
    "default": GetMetricsForTargetUnexpectedError,
}


class GetMonitorError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.get_monitor()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class GetMonitorUnexpectedError(GetMonitorError):
    """Operation-local response error for get_monitor (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetMonitorError.response_error_map = {
    "default": GetMonitorUnexpectedError,
}


class GetRoutesForTargetError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.get_routes_for_target()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class GetRoutesForTargetUnexpectedError(GetRoutesForTargetError):
    """Operation-local response error for get_routes_for_target (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetRoutesForTargetError.response_error_map = {
    "default": GetRoutesForTargetUnexpectedError,
}


class ListMonitorsError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.list_monitors()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class ListMonitorsUnexpectedError(ListMonitorsError):
    """Operation-local response error for list_monitors (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListMonitorsError.response_error_map = {
    "default": ListMonitorsUnexpectedError,
}


class SetMonitorStatusError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.set_monitor_status()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class SetMonitorStatusUnexpectedError(SetMonitorStatusError):
    """Operation-local response error for set_monitor_status (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SetMonitorStatusError.response_error_map = {
    "default": SetMonitorStatusUnexpectedError,
}


class UpdateMonitorError(BgpMonitoringError):
    """Operation-local error for client.bgp_monitoring.update_monitor()."""

    response_error_map: dict[str, type[BgpMonitoringError]] = {}


class UpdateMonitorUnexpectedError(UpdateMonitorError):
    """Operation-local response error for update_monitor (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateMonitorError.response_error_map = {
    "default": UpdateMonitorUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[BgpMonitoringError]] = {
    "create_monitor": CreateMonitorError,
    "delete_monitor": DeleteMonitorError,
    "get_metrics_for_target": GetMetricsForTargetError,
    "get_monitor": GetMonitorError,
    "get_routes_for_target": GetRoutesForTargetError,
    "list_monitors": ListMonitorsError,
    "set_monitor_status": SetMonitorStatusError,
    "update_monitor": UpdateMonitorError,
}

__all__ = [
    "BgpMonitoringError",
    "CreateMonitorUnexpectedError",
    "DeleteMonitorUnexpectedError",
    "GetMetricsForTargetUnexpectedError",
    "GetMonitorUnexpectedError",
    "GetRoutesForTargetUnexpectedError",
    "ListMonitorsUnexpectedError",
    "SetMonitorStatusUnexpectedError",
    "UpdateMonitorUnexpectedError",
    "CreateMonitorError",
    "DeleteMonitorError",
    "GetMetricsForTargetError",
    "GetMonitorError",
    "GetRoutesForTargetError",
    "ListMonitorsError",
    "SetMonitorStatusError",
    "UpdateMonitorError",
    "ERROR_BY_METHOD",
]
