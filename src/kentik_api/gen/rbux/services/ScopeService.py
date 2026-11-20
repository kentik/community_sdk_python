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
    CreateScopeError,
    DeleteScopeError,
    GetScopeError,
    ListScopesError,
    UpdateScopeError,
)
from ..models import (  # noqa: F401
    AssetTagSelector,
    CreateScopeResponse,
    DeleteScopeResponse,
    FilterField,
    FilterOperator,
    GetScopeResponse,
    ListScopesResponse,
    SavedFilterFilter,
    SavedFilterFilterGroup,
    SavedFilterFilterId,
    SavedFilterFilters,
    Scope,
    ScopeConfig,
    ScopeDimensions,
    ScopeServiceUpdateScopeBody,
    UpdateScopeResponse,
    protobufAny,
    rpcStatus,
)


def ListScopes(api_config_override: Optional[APIConfig] = None) -> ListScopesResponse:
    """
    List Focus Scopes

    Returns all Focus Scopes for the user's company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/rbux/v202607alpha1/scopes",
        path_template="/rbux/v202607alpha1/scopes",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListScopes",
        error_cls=ListScopesError,
    )

    return parse_response_model(
        ListScopesResponse,
        body,
        operation_name="ListScopes",
        method="get",
        path="/rbux/v202607alpha1/scopes",
    )


def CreateScope(
    api_config_override: Optional[APIConfig] = None, *, data: Scope
) -> CreateScopeResponse:
    """
    Create Focus Scope

    Creates and returns a new Focus Scope.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/rbux/v202607alpha1/scopes",
        path_template="/rbux/v202607alpha1/scopes",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateScope",
        error_cls=CreateScopeError,
    )

    return parse_response_model(
        CreateScopeResponse,
        body,
        operation_name="CreateScope",
        method="post",
        path="/rbux/v202607alpha1/scopes",
    )


def GetScope(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetScopeResponse:
    """
    Get Focus Scope

    Returns a single Focus Scope by id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/rbux/v202607alpha1/scopes/{path_segment(id)}",
        path_template="/rbux/v202607alpha1/scopes/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetScope",
        error_cls=GetScopeError,
    )

    return parse_response_model(
        GetScopeResponse,
        body,
        operation_name="GetScope",
        method="get",
        path="/rbux/v202607alpha1/scopes/{id}",
    )


def UpdateScope(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: ScopeServiceUpdateScopeBody,
) -> UpdateScopeResponse:
    """
    Update Focus Scope

    Updates and returns an existing Focus Scope.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/rbux/v202607alpha1/scopes/{path_segment(id)}",
        path_template="/rbux/v202607alpha1/scopes/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateScope",
        error_cls=UpdateScopeError,
    )

    return parse_response_model(
        UpdateScopeResponse,
        body,
        operation_name="UpdateScope",
        method="put",
        path="/rbux/v202607alpha1/scopes/{id}",
    )


def DeleteScope(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteScopeResponse:
    """
    Delete Focus Scope

    Deletes a Focus Scope.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/rbux/v202607alpha1/scopes/{path_segment(id)}",
        path_template="/rbux/v202607alpha1/scopes/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteScope",
        error_cls=DeleteScopeError,
    )

    return parse_response_model(
        DeleteScopeResponse,
        body,
        operation_name="DeleteScope",
        method="delete",
        path="/rbux/v202607alpha1/scopes/{id}",
    )
