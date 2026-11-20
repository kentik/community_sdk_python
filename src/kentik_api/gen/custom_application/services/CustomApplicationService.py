# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import CreateError, DeleteError, GetError, ListError, UpdateError
from ..models import (  # noqa: F401
    CreateCustomApplicationResponse,
    CustomApplication,
    DeleteCustomApplicationResponse,
    GetCustomApplicationResponse,
    ListCustomApplicationsResponse,
    UpdateCustomApplicationResponse,
    protobufAny,
    rpcStatus,
)


def ListCustomApplications(
    api_config_override: Optional[APIConfig] = None,
) -> ListCustomApplicationsResponse:
    """
    List Custom Applications

    Returns an array of custom application objects that each contain information about an individual custom application.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/custom_application/v202501alpha1",
        path_template="/custom_application/v202501alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCustomApplications",
        error_cls=ListError,
    )

    return parse_response_model(
        ListCustomApplicationsResponse,
        body,
        operation_name="ListCustomApplications",
        method="get",
        path="/custom_application/v202501alpha1",
    )


def CreateCustomApplication(
    api_config_override: Optional[APIConfig] = None, *, data: CustomApplication
) -> CreateCustomApplicationResponse:
    """
    Create Custom Application

    Creates and returns a custom application object containing information about an individual custom application.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/custom_application/v202501alpha1",
        path_template="/custom_application/v202501alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateCustomApplication",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateCustomApplicationResponse,
        body,
        operation_name="CreateCustomApplication",
        method="post",
        path="/custom_application/v202501alpha1",
    )


def GetCustomApplication(
    api_config_override: Optional[APIConfig] = None, *, customApplicationId: str
) -> GetCustomApplicationResponse:
    """
    Custom Application Info

    Returns a custom application object containing information about an individual custom application.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/custom_application/v202501alpha1/{path_segment(customApplicationId)}",
        path_template="/custom_application/v202501alpha1/{customApplicationId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetCustomApplication",
        error_cls=GetError,
    )

    return parse_response_model(
        GetCustomApplicationResponse,
        body,
        operation_name="GetCustomApplication",
        method="get",
        path="/custom_application/v202501alpha1/{customApplicationId}",
    )


def UpdateCustomApplication(
    api_config_override: Optional[APIConfig] = None,
    *,
    customApplicationId: str,
    data: CustomApplication,
) -> UpdateCustomApplicationResponse:
    """
    Update Custom Application

    Updates and returns a custom application object containing information about an individual custom application.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/custom_application/v202501alpha1/{path_segment(customApplicationId)}",
        path_template="/custom_application/v202501alpha1/{customApplicationId}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateCustomApplication",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateCustomApplicationResponse,
        body,
        operation_name="UpdateCustomApplication",
        method="put",
        path="/custom_application/v202501alpha1/{customApplicationId}",
    )


def DeleteCustomApplication(
    api_config_override: Optional[APIConfig] = None, *, customApplicationId: str
) -> DeleteCustomApplicationResponse:
    """
    Delete Custom Application

    Deletes a custom application.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/custom_application/v202501alpha1/{path_segment(customApplicationId)}",
        path_template="/custom_application/v202501alpha1/{customApplicationId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteCustomApplication",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteCustomApplicationResponse,
        body,
        operation_name="DeleteCustomApplication",
        method="delete",
        path="/custom_application/v202501alpha1/{customApplicationId}",
    )
