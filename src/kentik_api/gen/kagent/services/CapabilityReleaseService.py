# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import (
    GetCapabilityLatestReleasesError,
    GetCapabilityReleaseError,
    GetCapabilitySupportedDistrosError,
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


def CapabilityReleaseService_GetCapabilityRelease(
    api_config_override: Optional[APIConfig] = None,
    *,
    os: Optional[str] = None,
    arch: Optional[str] = None,
    channel: Optional[str] = None,
    capability: Optional[str] = None,
    semver: Optional[str] = None,
    distro: Optional[str] = None,
) -> GetCapabilityReleaseResponse:
    """
    GetCapabilityRelease can be used by install/upgrade modules to fetch a single release.
    """
    query_params: Dict[str, Any] = {
        "os": os,
        "arch": arch,
        "channel": channel,
        "capability": capability,
        "semver": semver,
        "distro": distro,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/releases",
        path_template="/kagent/v202401/releases",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityReleaseService_GetCapabilityRelease",
        error_cls=GetCapabilityReleaseError,
    )

    return parse_response_model(
        GetCapabilityReleaseResponse,
        body,
        operation_name="CapabilityReleaseService_GetCapabilityRelease",
        method="get",
        path="/kagent/v202401/releases",
    )


def CapabilityReleaseService_GetCapabilityLatestReleases(
    api_config_override: Optional[APIConfig] = None,
    *,
    os: Optional[str] = None,
    arch: Optional[str] = None,
    channel: Optional[str] = None,
    installId: Optional[str] = None,
    capabilities: Optional[List[str]] = None,
    distro: Optional[str] = None,
) -> GetCapabilityLatestReleasesResponse:
    """
    GetCapabilityLatestReleases can be used by install/upgrade modules to fetch the latest available releases.
    """
    query_params: Dict[str, Any] = {
        "os": os,
        "arch": arch,
        "channel": channel,
        "installId": installId,
        "capabilities": capabilities,
        "distro": distro,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/releases/latest",
        path_template="/kagent/v202401/releases/latest",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityReleaseService_GetCapabilityLatestReleases",
        error_cls=GetCapabilityLatestReleasesError,
    )

    return parse_response_model(
        GetCapabilityLatestReleasesResponse,
        body,
        operation_name="CapabilityReleaseService_GetCapabilityLatestReleases",
        method="get",
        path="/kagent/v202401/releases/latest",
    )


def CapabilityReleaseService_GetCapabilitySupportedDistros(
    api_config_override: Optional[APIConfig] = None,
    *,
    capabilities: Optional[List[str]] = None,
) -> GetCapabilitySupportedDistrosResponse:
    query_params: Dict[str, Any] = {"capabilities": capabilities}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/releases/supported_distros",
        path_template="/kagent/v202401/releases/supported_distros",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="CapabilityReleaseService_GetCapabilitySupportedDistros",
        error_cls=GetCapabilitySupportedDistrosError,
    )

    return parse_response_model(
        GetCapabilitySupportedDistrosResponse,
        body,
        operation_name="CapabilityReleaseService_GetCapabilitySupportedDistros",
        method="get",
        path="/kagent/v202401/releases/supported_distros",
    )
