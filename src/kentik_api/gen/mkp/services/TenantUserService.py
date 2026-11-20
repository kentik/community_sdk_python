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
    TenantUserCreateError,
    TenantUserDeleteError,
    TenantUserListError,
    TenantUserUpdateError,
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


def TenantUserList(
    api_config_override: Optional[APIConfig] = None, *, tenantId: str
) -> ListTenantUserResponse:
    """
    List users for a tenant.

    Returns a list of users associated with the specified tenant.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/mkp/v202407/tenants/{path_segment(tenantId)}/users",
        path_template="/mkp/v202407/tenants/{tenantId}/users",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="TenantUserList",
        error_cls=TenantUserListError,
    )

    return parse_response_model(
        ListTenantUserResponse,
        body,
        operation_name="TenantUserList",
        method="get",
        path="/mkp/v202407/tenants/{tenantId}/users",
    )


def TenantUserCreate(
    api_config_override: Optional[APIConfig] = None,
    *,
    tenantId: str,
    data: TenantUserServiceCreateTenantUserBody,
) -> CreateTenantUserResponse:
    """
    Add a user to a tenant.

    Creates a user association with the specified tenant.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/mkp/v202407/tenants/{path_segment(tenantId)}/users",
        path_template="/mkp/v202407/tenants/{tenantId}/users",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="TenantUserCreate",
        error_cls=TenantUserCreateError,
    )

    return parse_response_model(
        CreateTenantUserResponse,
        body,
        operation_name="TenantUserCreate",
        method="post",
        path="/mkp/v202407/tenants/{tenantId}/users",
    )


def TenantUserUpdate(
    api_config_override: Optional[APIConfig] = None,
    *,
    tenantId: str,
    id: str,
    data: TenantUserServiceUpdateTenantUserBody,
) -> UpdateTenantUserResponse:
    """
    Update a tenant user.

    Updates the user associated with the specified tenant and user ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/mkp/v202407/tenants/{path_segment(tenantId)}/users/{path_segment(id)}",
        path_template="/mkp/v202407/tenants/{tenantId}/users/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="TenantUserUpdate",
        error_cls=TenantUserUpdateError,
    )

    return parse_response_model(
        UpdateTenantUserResponse,
        body,
        operation_name="TenantUserUpdate",
        method="put",
        path="/mkp/v202407/tenants/{tenantId}/users/{id}",
    )


def TenantUserDelete(
    api_config_override: Optional[APIConfig] = None, *, tenantId: str, id: str
) -> DeleteTenantUserResponse:
    """
    Remove a user from a tenant.

    Deletes the user association with the specified tenant.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/mkp/v202407/tenants/{path_segment(tenantId)}/users/{path_segment(id)}",
        path_template="/mkp/v202407/tenants/{tenantId}/users/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="TenantUserDelete",
        error_cls=TenantUserDeleteError,
    )

    return parse_response_model(
        DeleteTenantUserResponse,
        body,
        operation_name="TenantUserDelete",
        method="delete",
        path="/mkp/v202407/tenants/{tenantId}/users/{id}",
    )
