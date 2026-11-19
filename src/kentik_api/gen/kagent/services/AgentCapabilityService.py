# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    DeleteAgentCapabilityError,
    GetAgentCapabilityError,
    ListAgentCapabilitiesError,
    UpsertAgentCapabilityError,
)
from ..models import (  # noqa: F401
    Agent,
    AgentCapability,
    AgentCapabilityServiceUpsertAgentCapabilityBody,
    AgentConfig,
    AgentRegistration,
    AgentServiceUpdateAgentBody,
    AuthorizeResponse,
    BootstrapInfo,
    BundleSource,
    Capability,
    CapabilityAdminServiceUpdateCapabilityBody,
    CapabilityDistro,
    CapabilityRelease,
    CapabilitySupportedDistro,
    CompatibilityInfo,
    Config,
    ConfigLayer,
    ConfigLayerLayerType,
    ConfigServiceUpdateConfigBody,
    ConfigSource,
    CreateAgentRequest,
    CreateAgentResponse,
    CreateCapabilityResponse,
    CreateConfigResponse,
    CreateProvisioningTokenResponse,
    DeleteAgentCapabilityResponse,
    DeleteAgentResponse,
    DeleteCapabilityResponse,
    DeleteConfigResponse,
    GenerateInstallCommandsRequest,
    GenerateInstallCommandsResponse,
    GetAgentCapabilityResponse,
    GetAgentResponse,
    GetCapabilityLatestReleasesResponse,
    GetCapabilityReleaseResponse,
    GetCapabilityResponse,
    GetCapabilitySupportedDistrosResponse,
    GetConfigResponse,
    GetProvisioningTokenResponse,
    HostMetadata,
    InstallConfig,
    InstallerType,
    ListAgentCapabilitiesResponse,
    ListAgentsByProvisioningTokenResponse,
    ListAgentsResponse,
    ListCapabilitiesResponse,
    ListProvisioningTokensResponse,
    ProvisioningToken,
    ProvisioningTokenAgentConfig,
    ProvisioningTokenServiceRevokeProvisioningTokenBody,
    RegistrationConfig,
    ReleaseSource,
    RevokeProvisioningTokenResponse,
    RuntimeConfig,
    RuntimeConfigEnvVar,
    TelemetryConfig,
    TokenRevoked,
    UpdateAgentResponse,
    UpdateCapabilityResponse,
    UpdateConfigResponse,
    UpsertAgentCapabilityResponse,
    protobufAny,
    rpcStatus,
)


def ListAgentCapabilities(
    api_config_override: Optional[APIConfig] = None, *, agentId: str
) -> ListAgentCapabilitiesResponse:
    """
    List agent capabilities.

    Returns a list of all capabilities of the specified agent.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/agents/{path_segment(agentId)}/capabilities",
        path_template="/kagent/v202401/agents/{agentId}/capabilities",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAgentCapabilities",
        error_cls=ListAgentCapabilitiesError,
    )

    return parse_response_model(
        ListAgentCapabilitiesResponse,
        body,
        operation_name="ListAgentCapabilities",
        method="get",
        path="/kagent/v202401/agents/{agentId}/capabilities",
    )


def GetAgentCapability(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentId: str,
    capabilityname: str,
) -> GetAgentCapabilityResponse:
    """
    Get an agent capability.

    Returns configuration of the named capability of the specified agent.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/agents/{path_segment(agentId)}/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAgentCapability",
        error_cls=GetAgentCapabilityError,
    )

    return parse_response_model(
        GetAgentCapabilityResponse,
        body,
        operation_name="GetAgentCapability",
        method="get",
        path="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
    )


def DeleteAgentCapability(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentId: str,
    capabilityname: str,
) -> DeleteAgentCapabilityResponse:
    """
    Delete an agent capability.

    Removes the named capability from the specified agent.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/kagent/v202401/agents/{path_segment(agentId)}/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteAgentCapability",
        error_cls=DeleteAgentCapabilityError,
    )

    return parse_response_model(
        DeleteAgentCapabilityResponse,
        body,
        operation_name="DeleteAgentCapability",
        method="delete",
        path="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
    )


def UpsertAgentCapability(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentId: str,
    capabilityname: str,
    data: AgentCapabilityServiceUpsertAgentCapabilityBody,
    mask: Optional[str] = None,
) -> UpsertAgentCapabilityResponse:
    """
    Create or update an agent capability.

    Adds the capability to the agent, or updates it if already present.
    """
    query_params: Dict[str, Any] = {"mask": mask}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/kagent/v202401/agents/{path_segment(agentId)}/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpsertAgentCapability",
        error_cls=UpsertAgentCapabilityError,
    )

    return parse_response_model(
        UpsertAgentCapabilityResponse,
        body,
        operation_name="UpsertAgentCapability",
        method="patch",
        path="/kagent/v202401/agents/{agentId}/capabilities/{capability.name}",
    )
