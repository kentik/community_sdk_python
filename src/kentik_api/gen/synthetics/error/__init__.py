# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class SyntheticsError(HTTPException):
    """Base service-local error for the synthetics API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "SyntheticsError":
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
    ) -> "SyntheticsError":
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


class BulkUpdateTestsError(SyntheticsError):
    """Operation-local error for client.synthetics.bulk_update_tests()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class BulkUpdateTestsUnexpectedError(BulkUpdateTestsError):
    """Operation-local response error for bulk_update_tests (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


BulkUpdateTestsError.response_error_map = {
    "default": BulkUpdateTestsUnexpectedError,
}


class CreateAgentAlertError(SyntheticsError):
    """Operation-local error for client.synthetics.create_agent_alert()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class CreateAgentAlertUnexpectedError(CreateAgentAlertError):
    """Operation-local response error for create_agent_alert (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateAgentAlertError.response_error_map = {
    "default": CreateAgentAlertUnexpectedError,
}


class CreateTestError(SyntheticsError):
    """Operation-local error for client.synthetics.create_test()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class CreateTestUnexpectedError(CreateTestError):
    """Operation-local response error for create_test (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateTestError.response_error_map = {
    "default": CreateTestUnexpectedError,
}


class DeleteAgentError(SyntheticsError):
    """Operation-local error for client.synthetics.delete_agent()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class DeleteAgentUnexpectedError(DeleteAgentError):
    """Operation-local response error for delete_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteAgentError.response_error_map = {
    "default": DeleteAgentUnexpectedError,
}


class DeleteAgentAlertError(SyntheticsError):
    """Operation-local error for client.synthetics.delete_agent_alert()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class DeleteAgentAlertUnexpectedError(DeleteAgentAlertError):
    """Operation-local response error for delete_agent_alert (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteAgentAlertError.response_error_map = {
    "default": DeleteAgentAlertUnexpectedError,
}


class DeleteTestError(SyntheticsError):
    """Operation-local error for client.synthetics.delete_test()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class DeleteTestUnexpectedError(DeleteTestError):
    """Operation-local response error for delete_test (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteTestError.response_error_map = {
    "default": DeleteTestUnexpectedError,
}


class GetAgentError(SyntheticsError):
    """Operation-local error for client.synthetics.get_agent()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetAgentUnexpectedError(GetAgentError):
    """Operation-local response error for get_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAgentError.response_error_map = {
    "default": GetAgentUnexpectedError,
}


class GetAgentAlertError(SyntheticsError):
    """Operation-local error for client.synthetics.get_agent_alert()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetAgentAlertUnexpectedError(GetAgentAlertError):
    """Operation-local response error for get_agent_alert (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAgentAlertError.response_error_map = {
    "default": GetAgentAlertUnexpectedError,
}


class GetBulkUpdateTestsStatusError(SyntheticsError):
    """Operation-local error for client.synthetics.get_bulk_update_tests_status()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetBulkUpdateTestsStatusUnexpectedError(GetBulkUpdateTestsStatusError):
    """Operation-local response error for get_bulk_update_tests_status (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetBulkUpdateTestsStatusError.response_error_map = {
    "default": GetBulkUpdateTestsStatusUnexpectedError,
}


class GetResultsForTestsError(SyntheticsError):
    """Operation-local error for client.synthetics.get_results_for_tests()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetResultsForTestsUnexpectedError(GetResultsForTestsError):
    """Operation-local response error for get_results_for_tests (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetResultsForTestsError.response_error_map = {
    "default": GetResultsForTestsUnexpectedError,
}


class GetResultsForTestsCsvError(SyntheticsError):
    """Operation-local error for client.synthetics.get_results_for_tests_csv()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetResultsForTestsCsvUnexpectedError(GetResultsForTestsCsvError):
    """Operation-local response error for get_results_for_tests_csv (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetResultsForTestsCsvError.response_error_map = {
    "default": GetResultsForTestsCsvUnexpectedError,
}


class GetTestError(SyntheticsError):
    """Operation-local error for client.synthetics.get_test()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetTestUnexpectedError(GetTestError):
    """Operation-local response error for get_test (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetTestError.response_error_map = {
    "default": GetTestUnexpectedError,
}


class GetTraceForTestError(SyntheticsError):
    """Operation-local error for client.synthetics.get_trace_for_test()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class GetTraceForTestUnexpectedError(GetTraceForTestError):
    """Operation-local response error for get_trace_for_test (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetTraceForTestError.response_error_map = {
    "default": GetTraceForTestUnexpectedError,
}


class ListAgentAlertsError(SyntheticsError):
    """Operation-local error for client.synthetics.list_agent_alerts()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class ListAgentAlertsUnexpectedError(ListAgentAlertsError):
    """Operation-local response error for list_agent_alerts (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListAgentAlertsError.response_error_map = {
    "default": ListAgentAlertsUnexpectedError,
}


class ListAgentsError(SyntheticsError):
    """Operation-local error for client.synthetics.list_agents()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class ListAgentsUnexpectedError(ListAgentsError):
    """Operation-local response error for list_agents (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListAgentsError.response_error_map = {
    "default": ListAgentsUnexpectedError,
}


class ListTestsError(SyntheticsError):
    """Operation-local error for client.synthetics.list_tests()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class ListTestsUnexpectedError(ListTestsError):
    """Operation-local response error for list_tests (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListTestsError.response_error_map = {
    "default": ListTestsUnexpectedError,
}


class SetTestStatusError(SyntheticsError):
    """Operation-local error for client.synthetics.set_test_status()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class SetTestStatusUnexpectedError(SetTestStatusError):
    """Operation-local response error for set_test_status (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SetTestStatusError.response_error_map = {
    "default": SetTestStatusUnexpectedError,
}


class UpdateAgentError(SyntheticsError):
    """Operation-local error for client.synthetics.update_agent()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class UpdateAgentUnexpectedError(UpdateAgentError):
    """Operation-local response error for update_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateAgentError.response_error_map = {
    "default": UpdateAgentUnexpectedError,
}


class UpdateAgentAlertError(SyntheticsError):
    """Operation-local error for client.synthetics.update_agent_alert()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class UpdateAgentAlertUnexpectedError(UpdateAgentAlertError):
    """Operation-local response error for update_agent_alert (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateAgentAlertError.response_error_map = {
    "default": UpdateAgentAlertUnexpectedError,
}


class UpdateTestError(SyntheticsError):
    """Operation-local error for client.synthetics.update_test()."""

    response_error_map: dict[str, type[SyntheticsError]] = {}


class UpdateTestUnexpectedError(UpdateTestError):
    """Operation-local response error for update_test (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateTestError.response_error_map = {
    "default": UpdateTestUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[SyntheticsError]] = {
    "bulk_update_tests": BulkUpdateTestsError,
    "create_agent_alert": CreateAgentAlertError,
    "create_test": CreateTestError,
    "delete_agent": DeleteAgentError,
    "delete_agent_alert": DeleteAgentAlertError,
    "delete_test": DeleteTestError,
    "get_agent": GetAgentError,
    "get_agent_alert": GetAgentAlertError,
    "get_bulk_update_tests_status": GetBulkUpdateTestsStatusError,
    "get_results_for_tests": GetResultsForTestsError,
    "get_results_for_tests_csv": GetResultsForTestsCsvError,
    "get_test": GetTestError,
    "get_trace_for_test": GetTraceForTestError,
    "list_agent_alerts": ListAgentAlertsError,
    "list_agents": ListAgentsError,
    "list_tests": ListTestsError,
    "set_test_status": SetTestStatusError,
    "update_agent": UpdateAgentError,
    "update_agent_alert": UpdateAgentAlertError,
    "update_test": UpdateTestError,
}

__all__ = [
    "SyntheticsError",
    "BulkUpdateTestsUnexpectedError",
    "CreateAgentAlertUnexpectedError",
    "CreateTestUnexpectedError",
    "DeleteAgentUnexpectedError",
    "DeleteAgentAlertUnexpectedError",
    "DeleteTestUnexpectedError",
    "GetAgentUnexpectedError",
    "GetAgentAlertUnexpectedError",
    "GetBulkUpdateTestsStatusUnexpectedError",
    "GetResultsForTestsUnexpectedError",
    "GetResultsForTestsCsvUnexpectedError",
    "GetTestUnexpectedError",
    "GetTraceForTestUnexpectedError",
    "ListAgentAlertsUnexpectedError",
    "ListAgentsUnexpectedError",
    "ListTestsUnexpectedError",
    "SetTestStatusUnexpectedError",
    "UpdateAgentUnexpectedError",
    "UpdateAgentAlertUnexpectedError",
    "UpdateTestUnexpectedError",
    "BulkUpdateTestsError",
    "CreateAgentAlertError",
    "CreateTestError",
    "DeleteAgentError",
    "DeleteAgentAlertError",
    "DeleteTestError",
    "GetAgentError",
    "GetAgentAlertError",
    "GetBulkUpdateTestsStatusError",
    "GetResultsForTestsError",
    "GetResultsForTestsCsvError",
    "GetTestError",
    "GetTraceForTestError",
    "ListAgentAlertsError",
    "ListAgentsError",
    "ListTestsError",
    "SetTestStatusError",
    "UpdateAgentError",
    "UpdateAgentAlertError",
    "UpdateTestError",
    "ERROR_BY_METHOD",
]
