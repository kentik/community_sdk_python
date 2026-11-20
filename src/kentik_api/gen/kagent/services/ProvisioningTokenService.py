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
    CreateProvisioningTokenError,
    GetProvisioningTokenError,
    ListAgentsByProvisioningTokenError,
    ListProvisioningTokensError,
    RevokeProvisioningTokenError,
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


def ListProvisioningTokens(
    api_config_override: Optional[APIConfig] = None,
) -> ListProvisioningTokensResponse:
    """
    List provisioning tokens.

    Returns a list of all provisioning tokens in the account.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kagent/v202401/provisioning-tokens",
        path_template="/kagent/v202401/provisioning-tokens",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListProvisioningTokens",
        error_cls=ListProvisioningTokensError,
    )

    return parse_response_model(
        ListProvisioningTokensResponse,
        body,
        operation_name="ListProvisioningTokens",
        method="get",
        path="/kagent/v202401/provisioning-tokens",
    )


def CreateProvisioningToken(
    api_config_override: Optional[APIConfig] = None, *, data: ProvisioningToken
) -> CreateProvisioningTokenResponse:
    """
    Create a provisioning token.

    Creates a new provisioning token based on configuration in the request and returns it, including its secret value.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/kagent/v202401/provisioning-tokens",
        path_template="/kagent/v202401/provisioning-tokens",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateProvisioningToken",
        error_cls=CreateProvisioningTokenError,
    )

    return parse_response_model(
        CreateProvisioningTokenResponse,
        body,
        operation_name="CreateProvisioningToken",
        method="post",
        path="/kagent/v202401/provisioning-tokens",
    )


def GetProvisioningToken(
    api_config_override: Optional[APIConfig] = None, *, token: str
) -> GetProvisioningTokenResponse:
    """
    Get provisioning token configuration and status.

    Returns configuration, usage and revocation status of the provisioning token with the specified value.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/provisioning-tokens/{path_segment(token)}",
        path_template="/kagent/v202401/provisioning-tokens/{token}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetProvisioningToken",
        error_cls=GetProvisioningTokenError,
    )

    return parse_response_model(
        GetProvisioningTokenResponse,
        body,
        operation_name="GetProvisioningToken",
        method="get",
        path="/kagent/v202401/provisioning-tokens/{token}",
    )


def ListAgentsByProvisioningToken(
    api_config_override: Optional[APIConfig] = None, *, token: str
) -> ListAgentsByProvisioningTokenResponse:
    """
    List agents registered with a provisioning token.

    Returns the IDs of all agents that have registered with the provisioning token with the specified value.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kagent/v202401/provisioning-tokens/{path_segment(token)}/agents",
        path_template="/kagent/v202401/provisioning-tokens/{token}/agents",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAgentsByProvisioningToken",
        error_cls=ListAgentsByProvisioningTokenError,
    )

    return parse_response_model(
        ListAgentsByProvisioningTokenResponse,
        body,
        operation_name="ListAgentsByProvisioningToken",
        method="get",
        path="/kagent/v202401/provisioning-tokens/{token}/agents",
    )


def RevokeProvisioningToken(
    api_config_override: Optional[APIConfig] = None,
    *,
    token: str,
    data: ProvisioningTokenServiceRevokeProvisioningTokenBody,
) -> RevokeProvisioningTokenResponse:
    """
    Revoke a provisioning token.

    Revokes the provisioning token with the specified value. Agents already registered with the token are not affected, but the token can no longer be used for new registrations.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/kagent/v202401/provisioning-tokens/{path_segment(token)}/revoke",
        path_template="/kagent/v202401/provisioning-tokens/{token}/revoke",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="RevokeProvisioningToken",
        error_cls=RevokeProvisioningTokenError,
    )

    return parse_response_model(
        RevokeProvisioningTokenResponse,
        body,
        operation_name="RevokeProvisioningToken",
        method="post",
        path="/kagent/v202401/provisioning-tokens/{token}/revoke",
    )
