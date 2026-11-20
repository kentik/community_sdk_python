# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    AuthorizeError,
    CreateAgentError,
    DeleteAgentError,
    GenerateInstallCommandsError,
    GetAgentError,
    ListAgentsError,
    UpdateAgentError,
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


def ListAgents(
    api_config_override: Optional[APIConfig] = None,
    *,
    unregistered: Optional[bool] = None,
    ids: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    includeDesiredState: Optional[bool] = None,
) -> ListAgentsResponse:
    """
    List agents.

    Returns a list of agents in the account, optionally filtered by registration state, IDs or capabilities.
    """
    query_params: Dict[str, Any] = {
        "unregistered": unregistered,
        "ids": ids,
        "capabilities": capabilities,
        "includeDesiredState": includeDesiredState,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/agents",
        path_template="/kagent/v202401/agents",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAgents",
        error_cls=ListAgentsError,
    )

    return parse_response_model(
        ListAgentsResponse,
        body,
        operation_name="ListAgents",
        method="get",
        path="/kagent/v202401/agents",
    )


def CreateAgent(
    api_config_override: Optional[APIConfig] = None, *, data: CreateAgentRequest
) -> CreateAgentResponse:
    """
    Create an agent.

    Registers a new agent based on configuration in the request and returns it together with the commands for installing it on the target host.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/kagent/v202401/agents",
        path_template="/kagent/v202401/agents",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateAgent",
        error_cls=CreateAgentError,
    )

    return parse_response_model(
        CreateAgentResponse,
        body,
        operation_name="CreateAgent",
        method="post",
        path="/kagent/v202401/agents",
    )


def Authorize(
    api_config_override: Optional[APIConfig] = None, *, installId: str
) -> AuthorizeResponse:
    """
    Authorize an unregistered agent.

    Approves the agent installed under the specified install ID and returns the ID assigned to it.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/kagent/v202401/agents/authorize/{path_segment(installId)}",
        path_template="/kagent/v202401/agents/authorize/{installId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Authorize",
        error_cls=AuthorizeError,
    )

    return parse_response_model(
        AuthorizeResponse,
        body,
        operation_name="Authorize",
        method="put",
        path="/kagent/v202401/agents/authorize/{installId}",
    )


def GenerateInstallCommands(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: GenerateInstallCommandsRequest,
) -> GenerateInstallCommandsResponse:
    """
    Generate agent install commands.

    Returns commands for deploying an agent. The commands embed a provisioning token and are ready to execute on the target host.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/kagent/v202401/agents/install-commands",
        path_template="/kagent/v202401/agents/install-commands",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GenerateInstallCommands",
        error_cls=GenerateInstallCommandsError,
    )

    return parse_response_model(
        GenerateInstallCommandsResponse,
        body,
        operation_name="GenerateInstallCommands",
        method="post",
        path="/kagent/v202401/agents/install-commands",
    )


def GetAgent(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentid: str,
    unregistered: Optional[bool] = None,
) -> GetAgentResponse:
    """
    Get agent configuration and state.

    Returns configuration and state of the agent with the specified ID.
    """
    query_params: Dict[str, Any] = {"unregistered": unregistered}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/agents/{path_segment(agentid)}",
        path_template="/kagent/v202401/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAgent",
        error_cls=GetAgentError,
    )

    return parse_response_model(
        GetAgentResponse,
        body,
        operation_name="GetAgent",
        method="get",
        path="/kagent/v202401/agents/{agent.id}",
    )


def DeleteAgent(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentid: str,
    unregistered: Optional[bool] = None,
) -> DeleteAgentResponse:
    """
    Delete an agent.

    Deletes the agent with the specified ID.
    """
    query_params: Dict[str, Any] = {"unregistered": unregistered}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/kagent/v202401/agents/{path_segment(agentid)}",
        path_template="/kagent/v202401/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteAgent",
        error_cls=DeleteAgentError,
    )

    return parse_response_model(
        DeleteAgentResponse,
        body,
        operation_name="DeleteAgent",
        method="delete",
        path="/kagent/v202401/agents/{agent.id}",
    )


def UpdateAgent(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentid: str,
    data: AgentServiceUpdateAgentBody,
    mask: Optional[str] = None,
) -> UpdateAgentResponse:
    """
    Update configuration of an agent.

    Updates the attributes of an agent selected by the field mask in the request.
    """
    query_params: Dict[str, Any] = {"mask": mask}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/kagent/v202401/agents/{path_segment(agentid)}",
        path_template="/kagent/v202401/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateAgent",
        error_cls=UpdateAgentError,
    )

    return parse_response_model(
        UpdateAgentResponse,
        body,
        operation_name="UpdateAgent",
        method="patch",
        path="/kagent/v202401/agents/{agent.id}",
    )
