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
    CreateError,
    CreatePopulatorError,
    DeleteError,
    DeletePopulatorError,
    GetInfoError,
    GetPopulatorError,
    GetPopulatorFieldError,
    ListError,
    UpdateError,
    UpdatePopulatorError,
)
from ..models import (  # noqa: F401
    CreateCustomDimensionResponse,
    CreatePopulatorResponse,
    CustomDimension,
    DeleteCustomDimensionResponse,
    DeletePopulatorResponse,
    ExtendedField,
    GetCustomDimensionInfoResponse,
    GetPopulatorFieldResponse,
    GetPopulatorResponse,
    ListCustomDimensionsResponse,
    Populator,
    UpdateCustomDimensionResponse,
    UpdatePopulatorResponse,
    protobufAny,
    rpcStatus,
)


def ListCustomDimensions(
    api_config_override: Optional[APIConfig] = None,
) -> ListCustomDimensionsResponse:
    """
    List Custom Dimensions

    Returns an array of custom dimension objects that each contain information about an individual custom dimension.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/custom_dimensions/v202411alpha1",
        path_template="/custom_dimensions/v202411alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCustomDimensions",
        error_cls=ListError,
    )

    return parse_response_model(
        ListCustomDimensionsResponse,
        body,
        operation_name="ListCustomDimensions",
        method="get",
        path="/custom_dimensions/v202411alpha1",
    )


def GetCustomDimensionInfo(
    api_config_override: Optional[APIConfig] = None, *, customDimensionId: str
) -> GetCustomDimensionInfoResponse:
    """
    Custom Dimension Info

    Returns a custom dimension object containing information about an individual custom dimension.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetCustomDimensionInfo",
        error_cls=GetInfoError,
    )

    return parse_response_model(
        GetCustomDimensionInfoResponse,
        body,
        operation_name="GetCustomDimensionInfo",
        method="get",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}",
    )


def UpdateCustomDimension(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    data: CustomDimension,
) -> UpdateCustomDimensionResponse:
    """
    Update Custom Dimension

    Updates and returns a custom dimension object containing information about an individual custom dimension (see About Custom Dimensions). Populators are not sent back in the response body. To get them use 'Custom Dimension info' API instead.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateCustomDimension",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateCustomDimensionResponse,
        body,
        operation_name="UpdateCustomDimension",
        method="put",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}",
    )


def DeleteCustomDimension(
    api_config_override: Optional[APIConfig] = None, *, customDimensionId: str
) -> DeleteCustomDimensionResponse:
    """
    Delete Custom Dimension

    Deletes a custom dimension.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteCustomDimension",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteCustomDimensionResponse,
        body,
        operation_name="DeleteCustomDimension",
        method="delete",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}",
    )


def CreatePopulator(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    data: Populator,
) -> CreatePopulatorResponse:
    """
    Create Populator

    Creates and returns a populator object containing information about an individual populator.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}/populator",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}/populator",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreatePopulator",
        error_cls=CreatePopulatorError,
    )

    return parse_response_model(
        CreatePopulatorResponse,
        body,
        operation_name="CreatePopulator",
        method="post",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}/populator",
    )


def GetPopulator(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    populatorId: str,
    fieldLimit: Optional[int] = None,
) -> GetPopulatorResponse:
    """
    Get Populator

    Get Populator by Dimension and Populator ID.
    """
    query_params: Dict[str, Any] = {"fieldLimit": fieldLimit}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}/populator/{path_segment(populatorId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetPopulator",
        error_cls=GetPopulatorError,
    )

    return parse_response_model(
        GetPopulatorResponse,
        body,
        operation_name="GetPopulator",
        method="get",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
    )


def UpdatePopulator(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    populatorId: str,
    data: Populator,
) -> UpdatePopulatorResponse:
    """
    Update Populator

    Updates and returns a populator object containing information about an individual populator.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}/populator/{path_segment(populatorId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdatePopulator",
        error_cls=UpdatePopulatorError,
    )

    return parse_response_model(
        UpdatePopulatorResponse,
        body,
        operation_name="UpdatePopulator",
        method="put",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
    )


def DeletePopulator(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    populatorId: str,
) -> DeletePopulatorResponse:
    """
    Delete Populator

    Deletes a populator.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}/populator/{path_segment(populatorId)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeletePopulator",
        error_cls=DeletePopulatorError,
    )

    return parse_response_model(
        DeletePopulatorResponse,
        body,
        operation_name="DeletePopulator",
        method="delete",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}",
    )


def GetPopulatorField(
    api_config_override: Optional[APIConfig] = None,
    *,
    customDimensionId: str,
    populatorId: str,
    fieldName: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> GetPopulatorFieldResponse:
    """
    Get Populator Field

    Get Populator field by Dimension, Populator ID, and field name.
    """
    query_params: Dict[str, Any] = {"offset": offset, "limit": limit}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/custom_dimensions/v202411alpha1/{path_segment(customDimensionId)}/populator/{path_segment(populatorId)}/field/{path_segment(fieldName)}",
        path_template="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}/field/{fieldName}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetPopulatorField",
        error_cls=GetPopulatorFieldError,
    )

    return parse_response_model(
        GetPopulatorFieldResponse,
        body,
        operation_name="GetPopulatorField",
        method="get",
        path="/custom_dimensions/v202411alpha1/{customDimensionId}/populator/{populatorId}/field/{fieldName}",
    )


def CreateCustomDimension(
    api_config_override: Optional[APIConfig] = None, *, data: CustomDimension
) -> CreateCustomDimensionResponse:
    """
    Create Custom Dimension

    Creates and returns a custom dimension object containing information about an individual custom dimension
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v1/customdimension",
        path_template="/v1/customdimension",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateCustomDimension",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateCustomDimensionResponse,
        body,
        operation_name="CreateCustomDimension",
        method="post",
        path="/v1/customdimension",
    )
