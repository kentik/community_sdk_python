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
    DeleteError,
    GetError,
    ListAllError,
    ListError,
    UpdateError,
)
from ..models import (  # noqa: F401
    CreateSavedFilterResponse,
    DeleteSavedFilterResponse,
    FilterField,
    FilterLevel,
    FilterOperator,
    GetSavedFilterResponse,
    ListSavedFiltersAllResponse,
    ListSavedFiltersResponse,
    SavedFilter,
    SavedFilterFilter,
    SavedFilterFilterGroup,
    SavedFilterFilterId,
    SavedFilterFilters,
    UpdateSavedFilterResponse,
    protobufAny,
    rpcStatus,
)


def CreateSavedFilter(
    api_config_override: Optional[APIConfig] = None, *, data: SavedFilter
) -> CreateSavedFilterResponse:
    """
    Create Saved Filter

    Creates and returns a saved filter object containing information about an individual saved filter.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/saved-filter/v202501alpha1",
        path_template="/saved-filter/v202501alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateSavedFilter",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateSavedFilterResponse,
        body,
        operation_name="CreateSavedFilter",
        method="post",
        path="/saved-filter/v202501alpha1",
    )


def GetSavedFilter(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetSavedFilterResponse:
    """
    Custom Saved Filter Info

    Returns a saved filter object containing information about an individual saved filter.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/saved-filter/v202501alpha1/{path_segment(id)}",
        path_template="/saved-filter/v202501alpha1/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetSavedFilter",
        error_cls=GetError,
    )

    return parse_response_model(
        GetSavedFilterResponse,
        body,
        operation_name="GetSavedFilter",
        method="get",
        path="/saved-filter/v202501alpha1/{id}",
    )


def UpdateSavedFilter(
    api_config_override: Optional[APIConfig] = None, *, id: str, data: SavedFilter
) -> UpdateSavedFilterResponse:
    """
    Update Saved Filter

    Updates and returns a saved filter object containing information about an individual saved filter.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/saved-filter/v202501alpha1/{path_segment(id)}",
        path_template="/saved-filter/v202501alpha1/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateSavedFilter",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateSavedFilterResponse,
        body,
        operation_name="UpdateSavedFilter",
        method="put",
        path="/saved-filter/v202501alpha1/{id}",
    )


def DeleteSavedFilter(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteSavedFilterResponse:
    """
    Delete Saved Filter

    Deletes a saved filter.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/saved-filter/v202501alpha1/{path_segment(id)}",
        path_template="/saved-filter/v202501alpha1/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteSavedFilter",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteSavedFilterResponse,
        body,
        operation_name="DeleteSavedFilter",
        method="delete",
        path="/saved-filter/v202501alpha1/{id}",
    )


def ListSavedFilters(
    api_config_override: Optional[APIConfig] = None,
) -> ListSavedFiltersResponse:
    """
    List Saved Filters

    Returns all custom saved filters created by the user's company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/saved-filters/v202501alpha1",
        path_template="/saved-filters/v202501alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListSavedFilters",
        error_cls=ListError,
    )

    return parse_response_model(
        ListSavedFiltersResponse,
        body,
        operation_name="ListSavedFilters",
        method="get",
        path="/saved-filters/v202501alpha1",
    )


def ListSavedFiltersAll(
    api_config_override: Optional[APIConfig] = None,
) -> ListSavedFiltersAllResponse:
    """
    List All Saved Filters

    Returns all saved filters, including system default filters.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/saved-filters/v202501alpha1/all",
        path_template="/saved-filters/v202501alpha1/all",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListSavedFiltersAll",
        error_cls=ListAllError,
    )

    return parse_response_model(
        ListSavedFiltersAllResponse,
        body,
        operation_name="ListSavedFiltersAll",
        method="get",
        path="/saved-filters/v202501alpha1/all",
    )
