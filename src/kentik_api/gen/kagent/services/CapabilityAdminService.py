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
    CreateCapabilityError,
    DeleteCapabilityError,
    GetCapabilityError,
    ListCapabilitiesError,
    UpdateCapabilityError,
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


def CapabilityAdminService_ListCapabilities(
    api_config_override: Optional[APIConfig] = None,
) -> ListCapabilitiesResponse:
    """
    List all capabilities
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/capabilities",
        path_template="/kagent/v202401/capabilities",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityAdminService_ListCapabilities",
        error_cls=ListCapabilitiesError,
    )

    return parse_response_model(
        ListCapabilitiesResponse,
        body,
        operation_name="CapabilityAdminService_ListCapabilities",
        method="get",
        path="/kagent/v202401/capabilities",
    )


def CapabilityAdminService_CreateCapability(
    api_config_override: Optional[APIConfig] = None, *, data: Capability
) -> CreateCapabilityResponse:
    """
    Create a new capability
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/kagent/v202401/capabilities",
        path_template="/kagent/v202401/capabilities",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityAdminService_CreateCapability",
        error_cls=CreateCapabilityError,
    )

    return parse_response_model(
        CreateCapabilityResponse,
        body,
        operation_name="CapabilityAdminService_CreateCapability",
        method="post",
        path="/kagent/v202401/capabilities",
    )


def CapabilityAdminService_GetCapability(
    api_config_override: Optional[APIConfig] = None, *, capabilityname: str
) -> GetCapabilityResponse:
    """
    Get a capabilities
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityAdminService_GetCapability",
        error_cls=GetCapabilityError,
    )

    return parse_response_model(
        GetCapabilityResponse,
        body,
        operation_name="CapabilityAdminService_GetCapability",
        method="get",
        path="/kagent/v202401/capabilities/{capability.name}",
    )


def CapabilityAdminService_DeleteCapability(
    api_config_override: Optional[APIConfig] = None, *, capabilityname: str
) -> DeleteCapabilityResponse:
    """
    Delete a capability
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/kagent/v202401/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityAdminService_DeleteCapability",
        error_cls=DeleteCapabilityError,
    )

    return parse_response_model(
        DeleteCapabilityResponse,
        body,
        operation_name="CapabilityAdminService_DeleteCapability",
        method="delete",
        path="/kagent/v202401/capabilities/{capability.name}",
    )


def CapabilityAdminService_UpdateCapability(
    api_config_override: Optional[APIConfig] = None,
    *,
    capabilityname: str,
    data: CapabilityAdminServiceUpdateCapabilityBody,
) -> UpdateCapabilityResponse:
    """
    Update an existing capability
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/kagent/v202401/capabilities/{path_segment(capabilityname)}",
        path_template="/kagent/v202401/capabilities/{capability.name}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityAdminService_UpdateCapability",
        error_cls=UpdateCapabilityError,
    )

    return parse_response_model(
        UpdateCapabilityResponse,
        body,
        operation_name="CapabilityAdminService_UpdateCapability",
        method="patch",
        path="/kagent/v202401/capabilities/{capability.name}",
    )
