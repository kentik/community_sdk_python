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
    CreateConfigError,
    DeleteConfigError,
    GetConfigError,
    UpdateConfigError,
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


def CreateConfig(
    api_config_override: Optional[APIConfig] = None, *, data: Config
) -> CreateConfigResponse:
    """
    Create a config.

    Creates a new config based on the request and returns it.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/kagent/v202401/config",
        path_template="/kagent/v202401/config",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateConfig",
        error_cls=CreateConfigError,
    )

    return parse_response_model(
        CreateConfigResponse,
        body,
        operation_name="CreateConfig",
        method="post",
        path="/kagent/v202401/config",
    )


def GetConfig(
    api_config_override: Optional[APIConfig] = None, *, configname: str
) -> GetConfigResponse:
    """
    Get a config.

    Returns the config with the specified name.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/config/{path_segment(configname)}",
        path_template="/kagent/v202401/config/{config.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetConfig",
        error_cls=GetConfigError,
    )

    return parse_response_model(
        GetConfigResponse,
        body,
        operation_name="GetConfig",
        method="get",
        path="/kagent/v202401/config/{config.name}",
    )


def DeleteConfig(
    api_config_override: Optional[APIConfig] = None, *, configname: str
) -> DeleteConfigResponse:
    """
    Delete a config.

    Deletes the config with the specified name.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/kagent/v202401/config/{path_segment(configname)}",
        path_template="/kagent/v202401/config/{config.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteConfig",
        error_cls=DeleteConfigError,
    )

    return parse_response_model(
        DeleteConfigResponse,
        body,
        operation_name="DeleteConfig",
        method="delete",
        path="/kagent/v202401/config/{config.name}",
    )


def UpdateConfig(
    api_config_override: Optional[APIConfig] = None,
    *,
    configname: str,
    data: ConfigServiceUpdateConfigBody,
) -> UpdateConfigResponse:
    """
    Update a config.

    Updates the attributes of a config selected by the field mask in the request.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/kagent/v202401/config/{path_segment(configname)}",
        path_template="/kagent/v202401/config/{config.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateConfig",
        error_cls=UpdateConfigError,
    )

    return parse_response_model(
        UpdateConfigResponse,
        body,
        operation_name="UpdateConfig",
        method="patch",
        path="/kagent/v202401/config/{config.name}",
    )
