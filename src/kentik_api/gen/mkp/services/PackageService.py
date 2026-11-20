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
    PackageCreateError,
    PackageDeleteError,
    PackageGetError,
    PackageListError,
    PackageUpdateError,
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


def PackageList(api_config_override: Optional[APIConfig] = None) -> ListPackageResponse:
    """
    List MKP packages.

    Returns a list of MKP packages.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/mkp/v202407/packages",
        path_template="/mkp/v202407/packages",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="PackageList",
        error_cls=PackageListError,
    )

    return parse_response_model(
        ListPackageResponse,
        body,
        operation_name="PackageList",
        method="get",
        path="/mkp/v202407/packages",
    )


def PackageCreate(
    api_config_override: Optional[APIConfig] = None, *, data: CreatePackageRequest
) -> CreatePackageResponse:
    """
    Create a package template.

    Create package from request. returns created package.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/mkp/v202407/packages",
        path_template="/mkp/v202407/packages",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="PackageCreate",
        error_cls=PackageCreateError,
    )

    return parse_response_model(
        CreatePackageResponse,
        body,
        operation_name="PackageCreate",
        method="post",
        path="/mkp/v202407/packages",
    )


def PackageGet(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetPackageResponse:
    """
    Get information aboout a package.

    Returns information about package specified with ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/mkp/v202407/packages/{path_segment(id)}",
        path_template="/mkp/v202407/packages/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="PackageGet",
        error_cls=PackageGetError,
    )

    return parse_response_model(
        GetPackageResponse,
        body,
        operation_name="PackageGet",
        method="get",
        path="/mkp/v202407/packages/{id}",
    )


def PackageUpdate(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: PackageServiceUpdatePackageBody,
) -> UpdatePackageResponse:
    """
    Update a package.

    Update package attributes specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/mkp/v202407/packages/{path_segment(id)}",
        path_template="/mkp/v202407/packages/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="PackageUpdate",
        error_cls=PackageUpdateError,
    )

    return parse_response_model(
        UpdatePackageResponse,
        body,
        operation_name="PackageUpdate",
        method="put",
        path="/mkp/v202407/packages/{id}",
    )


def PackageDelete(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeletePackageResponse:
    """
    Delete a package.

    Deletes the package specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/mkp/v202407/packages/{path_segment(id)}",
        path_template="/mkp/v202407/packages/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="PackageDelete",
        error_cls=PackageDeleteError,
    )

    return parse_response_model(
        DeletePackageResponse,
        body,
        operation_name="PackageDelete",
        method="delete",
        path="/mkp/v202407/packages/{id}",
    )
