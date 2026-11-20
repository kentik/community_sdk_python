# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class KagentError(HTTPException):
    """Base service-local error for the kagent API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "KagentError":
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
    ) -> "KagentError":
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


class AuthorizeError(KagentError):
    """Operation-local error for client.kagent.authorize()."""

    response_error_map: dict[str, type[KagentError]] = {}


class AuthorizeUnexpectedError(AuthorizeError):
    """Operation-local response error for authorize (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AuthorizeError.response_error_map = {
    "default": AuthorizeUnexpectedError,
}


class CreateAgentError(KagentError):
    """Operation-local error for client.kagent.create_agent()."""

    response_error_map: dict[str, type[KagentError]] = {}


class CreateAgentUnexpectedError(CreateAgentError):
    """Operation-local response error for create_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateAgentError.response_error_map = {
    "default": CreateAgentUnexpectedError,
}


class CreateCapabilityError(KagentError):
    """Operation-local error for client.kagent.create_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class CreateCapabilityUnexpectedError(CreateCapabilityError):
    """Operation-local response error for create_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateCapabilityError.response_error_map = {
    "default": CreateCapabilityUnexpectedError,
}


class CreateConfigError(KagentError):
    """Operation-local error for client.kagent.create_config()."""

    response_error_map: dict[str, type[KagentError]] = {}


class CreateConfigUnexpectedError(CreateConfigError):
    """Operation-local response error for create_config (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateConfigError.response_error_map = {
    "default": CreateConfigUnexpectedError,
}


class CreateProvisioningTokenError(KagentError):
    """Operation-local error for client.kagent.create_provisioning_token()."""

    response_error_map: dict[str, type[KagentError]] = {}


class CreateProvisioningTokenUnexpectedError(CreateProvisioningTokenError):
    """Operation-local response error for create_provisioning_token (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


CreateProvisioningTokenError.response_error_map = {
    "default": CreateProvisioningTokenUnexpectedError,
}


class DeleteAgentError(KagentError):
    """Operation-local error for client.kagent.delete_agent()."""

    response_error_map: dict[str, type[KagentError]] = {}


class DeleteAgentUnexpectedError(DeleteAgentError):
    """Operation-local response error for delete_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteAgentError.response_error_map = {
    "default": DeleteAgentUnexpectedError,
}


class DeleteAgentCapabilityError(KagentError):
    """Operation-local error for client.kagent.delete_agent_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class DeleteAgentCapabilityUnexpectedError(DeleteAgentCapabilityError):
    """Operation-local response error for delete_agent_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteAgentCapabilityError.response_error_map = {
    "default": DeleteAgentCapabilityUnexpectedError,
}


class DeleteCapabilityError(KagentError):
    """Operation-local error for client.kagent.delete_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class DeleteCapabilityUnexpectedError(DeleteCapabilityError):
    """Operation-local response error for delete_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteCapabilityError.response_error_map = {
    "default": DeleteCapabilityUnexpectedError,
}


class DeleteConfigError(KagentError):
    """Operation-local error for client.kagent.delete_config()."""

    response_error_map: dict[str, type[KagentError]] = {}


class DeleteConfigUnexpectedError(DeleteConfigError):
    """Operation-local response error for delete_config (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DeleteConfigError.response_error_map = {
    "default": DeleteConfigUnexpectedError,
}


class GenerateInstallCommandsError(KagentError):
    """Operation-local error for client.kagent.generate_install_commands()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GenerateInstallCommandsUnexpectedError(GenerateInstallCommandsError):
    """Operation-local response error for generate_install_commands (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GenerateInstallCommandsError.response_error_map = {
    "default": GenerateInstallCommandsUnexpectedError,
}


class GetAgentError(KagentError):
    """Operation-local error for client.kagent.get_agent()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetAgentUnexpectedError(GetAgentError):
    """Operation-local response error for get_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAgentError.response_error_map = {
    "default": GetAgentUnexpectedError,
}


class GetAgentCapabilityError(KagentError):
    """Operation-local error for client.kagent.get_agent_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetAgentCapabilityUnexpectedError(GetAgentCapabilityError):
    """Operation-local response error for get_agent_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetAgentCapabilityError.response_error_map = {
    "default": GetAgentCapabilityUnexpectedError,
}


class GetCapabilityError(KagentError):
    """Operation-local error for client.kagent.get_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetCapabilityUnexpectedError(GetCapabilityError):
    """Operation-local response error for get_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetCapabilityError.response_error_map = {
    "default": GetCapabilityUnexpectedError,
}


class GetCapabilityLatestReleasesError(KagentError):
    """Operation-local error for client.kagent.get_capability_latest_releases()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetCapabilityLatestReleasesUnexpectedError(GetCapabilityLatestReleasesError):
    """Operation-local response error for get_capability_latest_releases (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetCapabilityLatestReleasesError.response_error_map = {
    "default": GetCapabilityLatestReleasesUnexpectedError,
}


class GetCapabilityReleaseError(KagentError):
    """Operation-local error for client.kagent.get_capability_release()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetCapabilityReleaseUnexpectedError(GetCapabilityReleaseError):
    """Operation-local response error for get_capability_release (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetCapabilityReleaseError.response_error_map = {
    "default": GetCapabilityReleaseUnexpectedError,
}


class GetCapabilitySupportedDistrosError(KagentError):
    """Operation-local error for client.kagent.get_capability_supported_distros()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetCapabilitySupportedDistrosUnexpectedError(GetCapabilitySupportedDistrosError):
    """Operation-local response error for get_capability_supported_distros (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetCapabilitySupportedDistrosError.response_error_map = {
    "default": GetCapabilitySupportedDistrosUnexpectedError,
}


class GetConfigError(KagentError):
    """Operation-local error for client.kagent.get_config()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetConfigUnexpectedError(GetConfigError):
    """Operation-local response error for get_config (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetConfigError.response_error_map = {
    "default": GetConfigUnexpectedError,
}


class GetProvisioningTokenError(KagentError):
    """Operation-local error for client.kagent.get_provisioning_token()."""

    response_error_map: dict[str, type[KagentError]] = {}


class GetProvisioningTokenUnexpectedError(GetProvisioningTokenError):
    """Operation-local response error for get_provisioning_token (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetProvisioningTokenError.response_error_map = {
    "default": GetProvisioningTokenUnexpectedError,
}


class ListAgentCapabilitiesError(KagentError):
    """Operation-local error for client.kagent.list_agent_capabilities()."""

    response_error_map: dict[str, type[KagentError]] = {}


class ListAgentCapabilitiesUnexpectedError(ListAgentCapabilitiesError):
    """Operation-local response error for list_agent_capabilities (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListAgentCapabilitiesError.response_error_map = {
    "default": ListAgentCapabilitiesUnexpectedError,
}


class ListAgentsError(KagentError):
    """Operation-local error for client.kagent.list_agents()."""

    response_error_map: dict[str, type[KagentError]] = {}


class ListAgentsUnexpectedError(ListAgentsError):
    """Operation-local response error for list_agents (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListAgentsError.response_error_map = {
    "default": ListAgentsUnexpectedError,
}


class ListAgentsByProvisioningTokenError(KagentError):
    """Operation-local error for client.kagent.list_agents_by_provisioning_token()."""

    response_error_map: dict[str, type[KagentError]] = {}


class ListAgentsByProvisioningTokenUnexpectedError(ListAgentsByProvisioningTokenError):
    """Operation-local response error for list_agents_by_provisioning_token (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListAgentsByProvisioningTokenError.response_error_map = {
    "default": ListAgentsByProvisioningTokenUnexpectedError,
}


class ListCapabilitiesError(KagentError):
    """Operation-local error for client.kagent.list_capabilities()."""

    response_error_map: dict[str, type[KagentError]] = {}


class ListCapabilitiesUnexpectedError(ListCapabilitiesError):
    """Operation-local response error for list_capabilities (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListCapabilitiesError.response_error_map = {
    "default": ListCapabilitiesUnexpectedError,
}


class ListProvisioningTokensError(KagentError):
    """Operation-local error for client.kagent.list_provisioning_tokens()."""

    response_error_map: dict[str, type[KagentError]] = {}


class ListProvisioningTokensUnexpectedError(ListProvisioningTokensError):
    """Operation-local response error for list_provisioning_tokens (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListProvisioningTokensError.response_error_map = {
    "default": ListProvisioningTokensUnexpectedError,
}


class RevokeProvisioningTokenError(KagentError):
    """Operation-local error for client.kagent.revoke_provisioning_token()."""

    response_error_map: dict[str, type[KagentError]] = {}


class RevokeProvisioningTokenUnexpectedError(RevokeProvisioningTokenError):
    """Operation-local response error for revoke_provisioning_token (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


RevokeProvisioningTokenError.response_error_map = {
    "default": RevokeProvisioningTokenUnexpectedError,
}


class UpdateAgentError(KagentError):
    """Operation-local error for client.kagent.update_agent()."""

    response_error_map: dict[str, type[KagentError]] = {}


class UpdateAgentUnexpectedError(UpdateAgentError):
    """Operation-local response error for update_agent (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateAgentError.response_error_map = {
    "default": UpdateAgentUnexpectedError,
}


class UpdateCapabilityError(KagentError):
    """Operation-local error for client.kagent.update_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class UpdateCapabilityUnexpectedError(UpdateCapabilityError):
    """Operation-local response error for update_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateCapabilityError.response_error_map = {
    "default": UpdateCapabilityUnexpectedError,
}


class UpdateConfigError(KagentError):
    """Operation-local error for client.kagent.update_config()."""

    response_error_map: dict[str, type[KagentError]] = {}


class UpdateConfigUnexpectedError(UpdateConfigError):
    """Operation-local response error for update_config (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpdateConfigError.response_error_map = {
    "default": UpdateConfigUnexpectedError,
}


class UpsertAgentCapabilityError(KagentError):
    """Operation-local error for client.kagent.upsert_agent_capability()."""

    response_error_map: dict[str, type[KagentError]] = {}


class UpsertAgentCapabilityUnexpectedError(UpsertAgentCapabilityError):
    """Operation-local response error for upsert_agent_capability (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UpsertAgentCapabilityError.response_error_map = {
    "default": UpsertAgentCapabilityUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[KagentError]] = {
    "authorize": AuthorizeError,
    "create_agent": CreateAgentError,
    "create_capability": CreateCapabilityError,
    "create_config": CreateConfigError,
    "create_provisioning_token": CreateProvisioningTokenError,
    "delete_agent": DeleteAgentError,
    "delete_agent_capability": DeleteAgentCapabilityError,
    "delete_capability": DeleteCapabilityError,
    "delete_config": DeleteConfigError,
    "generate_install_commands": GenerateInstallCommandsError,
    "get_agent": GetAgentError,
    "get_agent_capability": GetAgentCapabilityError,
    "get_capability": GetCapabilityError,
    "get_capability_latest_releases": GetCapabilityLatestReleasesError,
    "get_capability_release": GetCapabilityReleaseError,
    "get_capability_supported_distros": GetCapabilitySupportedDistrosError,
    "get_config": GetConfigError,
    "get_provisioning_token": GetProvisioningTokenError,
    "list_agent_capabilities": ListAgentCapabilitiesError,
    "list_agents": ListAgentsError,
    "list_agents_by_provisioning_token": ListAgentsByProvisioningTokenError,
    "list_capabilities": ListCapabilitiesError,
    "list_provisioning_tokens": ListProvisioningTokensError,
    "revoke_provisioning_token": RevokeProvisioningTokenError,
    "update_agent": UpdateAgentError,
    "update_capability": UpdateCapabilityError,
    "update_config": UpdateConfigError,
    "upsert_agent_capability": UpsertAgentCapabilityError,
}

__all__ = [
    "KagentError",
    "AuthorizeUnexpectedError",
    "CreateAgentUnexpectedError",
    "CreateCapabilityUnexpectedError",
    "CreateConfigUnexpectedError",
    "CreateProvisioningTokenUnexpectedError",
    "DeleteAgentUnexpectedError",
    "DeleteAgentCapabilityUnexpectedError",
    "DeleteCapabilityUnexpectedError",
    "DeleteConfigUnexpectedError",
    "GenerateInstallCommandsUnexpectedError",
    "GetAgentUnexpectedError",
    "GetAgentCapabilityUnexpectedError",
    "GetCapabilityUnexpectedError",
    "GetCapabilityLatestReleasesUnexpectedError",
    "GetCapabilityReleaseUnexpectedError",
    "GetCapabilitySupportedDistrosUnexpectedError",
    "GetConfigUnexpectedError",
    "GetProvisioningTokenUnexpectedError",
    "ListAgentCapabilitiesUnexpectedError",
    "ListAgentsUnexpectedError",
    "ListAgentsByProvisioningTokenUnexpectedError",
    "ListCapabilitiesUnexpectedError",
    "ListProvisioningTokensUnexpectedError",
    "RevokeProvisioningTokenUnexpectedError",
    "UpdateAgentUnexpectedError",
    "UpdateCapabilityUnexpectedError",
    "UpdateConfigUnexpectedError",
    "UpsertAgentCapabilityUnexpectedError",
    "AuthorizeError",
    "CreateAgentError",
    "CreateCapabilityError",
    "CreateConfigError",
    "CreateProvisioningTokenError",
    "DeleteAgentError",
    "DeleteAgentCapabilityError",
    "DeleteCapabilityError",
    "DeleteConfigError",
    "GenerateInstallCommandsError",
    "GetAgentError",
    "GetAgentCapabilityError",
    "GetCapabilityError",
    "GetCapabilityLatestReleasesError",
    "GetCapabilityReleaseError",
    "GetCapabilitySupportedDistrosError",
    "GetConfigError",
    "GetProvisioningTokenError",
    "ListAgentCapabilitiesError",
    "ListAgentsError",
    "ListAgentsByProvisioningTokenError",
    "ListCapabilitiesError",
    "ListProvisioningTokensError",
    "RevokeProvisioningTokenError",
    "UpdateAgentError",
    "UpdateCapabilityError",
    "UpdateConfigError",
    "UpsertAgentCapabilityError",
    "ERROR_BY_METHOD",
]
