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
    TenantCreateError,
    TenantDeleteError,
    TenantGetError,
    TenantListError,
    TenantUpdateError,
)
from ..models import (  # noqa: F401
    Activate,
    Alert,
    Asset,
    AssetReport,
    Condition,
    CreatePackageRequest,
    CreatePackageResponse,
    CreateTenantRequest,
    CreateTenantResponse,
    CreateTenantUserResponse,
    CustomDimension,
    DeletePackageResponse,
    DeleteTenantResponse,
    DeleteTenantUserResponse,
    Devices,
    Filter,
    FilterField,
    GetPackageResponse,
    GetTenantResponse,
    LandingType,
    ListPackageResponse,
    ListTenantResponse,
    ListTenantUserResponse,
    Mitigation,
    NotificationChannel,
    Package,
    PackageServiceUpdatePackageBody,
    PermissionEntry,
    Role,
    Tenant,
    TenantLink,
    TenantServiceUpdateTenantBody,
    TenantUser,
    TenantUserServiceCreateTenantUserBody,
    TenantUserServiceUpdateTenantUserBody,
    Threshold,
    UpdatePackageResponse,
    UpdateTenantResponse,
    UpdateTenantUserResponse,
    User,
    protobufAny,
    rpcStatus,
)


def TenantList(api_config_override: Optional[APIConfig] = None) -> ListTenantResponse:
    """
    List MKP tenants.

    Returns a list of MKP tenants.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/mkp/v202407/tenants",
        path_template="/mkp/v202407/tenants",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="TenantList",
        error_cls=TenantListError,
    )

    return parse_response_model(
        ListTenantResponse,
        body,
        operation_name="TenantList",
        method="get",
        path="/mkp/v202407/tenants",
    )


def TenantCreate(
    api_config_override: Optional[APIConfig] = None, *, data: CreateTenantRequest
) -> CreateTenantResponse:
    """
    Create a tenant.

    Create tenant from request. returns created tenant.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/mkp/v202407/tenants",
        path_template="/mkp/v202407/tenants",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="TenantCreate",
        error_cls=TenantCreateError,
    )

    return parse_response_model(
        CreateTenantResponse,
        body,
        operation_name="TenantCreate",
        method="post",
        path="/mkp/v202407/tenants",
    )


def TenantGet(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetTenantResponse:
    """
    Get information aboout a tenant.

    Returns information about package specified with ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/mkp/v202407/tenants/{path_segment(id)}",
        path_template="/mkp/v202407/tenants/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="TenantGet",
        error_cls=TenantGetError,
    )

    return parse_response_model(
        GetTenantResponse,
        body,
        operation_name="TenantGet",
        method="get",
        path="/mkp/v202407/tenants/{id}",
    )


def TenantUpdate(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: TenantServiceUpdateTenantBody,
) -> UpdateTenantResponse:
    """
    Update a tenant.

    Update tenant attributes specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/mkp/v202407/tenants/{path_segment(id)}",
        path_template="/mkp/v202407/tenants/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="TenantUpdate",
        error_cls=TenantUpdateError,
    )

    return parse_response_model(
        UpdateTenantResponse,
        body,
        operation_name="TenantUpdate",
        method="put",
        path="/mkp/v202407/tenants/{id}",
    )


def TenantDelete(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteTenantResponse:
    """
    Delete a tenant.

    Deletes the tenant specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/mkp/v202407/tenants/{path_segment(id)}",
        path_template="/mkp/v202407/tenants/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="TenantDelete",
        error_cls=TenantDeleteError,
    )

    return parse_response_model(
        DeleteTenantResponse,
        body,
        operation_name="TenantDelete",
        method="delete",
        path="/mkp/v202407/tenants/{id}",
    )
