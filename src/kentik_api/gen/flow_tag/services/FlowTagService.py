# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import CreateError, DeleteError, GetError, SearchError, UpdateError
from ..models import (  # noqa: F401
    AddressInfo,
    CreateFlowTagRequest,
    CreateFlowTagResponse,
    DeleteFlowTagResponse,
    FlowTag,
    FlowTagSearch,
    FlowTagServiceUpdateFlowTagBody,
    GetFlowTagResponse,
    LookupField,
    OrderDirection,
    OrderField,
    SearchFlowTagResponse,
    UpdateFlowTagResponse,
    protobufAny,
    rpcStatus,
)


def SearchFlowTag(
    api_config_override: Optional[APIConfig] = None,
    *,
    searchlimit: Optional[int] = None,
    searchoffset: Optional[int] = None,
    searchlookupFields: Optional[List[str]] = None,
    searchlookupValues: Optional[List[str]] = None,
    searchfieldLimit: Optional[int] = None,
) -> SearchFlowTagResponse:
    """
    Search flow tag configuration.

    Returns configuration of flow tag with search parameters.
    """
    query_params: Dict[str, Any] = {
        "search.limit": searchlimit,
        "search.offset": searchoffset,
        "search.lookupFields": searchlookupFields,
        "search.lookupValues": searchlookupValues,
        "search.fieldLimit": searchfieldLimit,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/flow_tag/v202404alpha1/tag",
        path_template="/flow_tag/v202404alpha1/tag",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="SearchFlowTag",
        error_cls=SearchError,
    )

    return parse_response_model(
        SearchFlowTagResponse,
        body,
        operation_name="SearchFlowTag",
        method="get",
        path="/flow_tag/v202404alpha1/tag",
    )


def CreateFlowTag(
    api_config_override: Optional[APIConfig] = None, *, data: CreateFlowTagRequest
) -> CreateFlowTagResponse:
    """
    Create flow tag configuration.

    Create a flow tag configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/flow_tag/v202404alpha1/tag",
        path_template="/flow_tag/v202404alpha1/tag",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateFlowTag",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateFlowTagResponse,
        body,
        operation_name="CreateFlowTag",
        method="post",
        path="/flow_tag/v202404alpha1/tag",
    )


def GetFlowTag(
    api_config_override: Optional[APIConfig] = None, *, flowTagid: str
) -> GetFlowTagResponse:
    """
    Get flow tag configuration.

    Returns configuration of flow tag with specified ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/flow_tag/v202404alpha1/tag/{path_segment(flowTagid)}",
        path_template="/flow_tag/v202404alpha1/tag/{flowTag.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetFlowTag",
        error_cls=GetError,
    )

    return parse_response_model(
        GetFlowTagResponse,
        body,
        operation_name="GetFlowTag",
        method="get",
        path="/flow_tag/v202404alpha1/tag/{flowTag.id}",
    )


def UpdateFlowTag(
    api_config_override: Optional[APIConfig] = None,
    *,
    flowTagid: str,
    data: FlowTagServiceUpdateFlowTagBody,
) -> UpdateFlowTagResponse:
    """
    Update flow tag configuration.

    Update a flow tag configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/flow_tag/v202404alpha1/tag/{path_segment(flowTagid)}",
        path_template="/flow_tag/v202404alpha1/tag/{flowTag.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        # Upstream REST drops this camelCase key: AGENTS.md, Upstream workarounds.
        json_body={
            {"flowTag": "flow_tag"}.get(key, key): value
            for key, value in data.model_dump(by_alias=True, exclude_unset=True).items()
        },
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateFlowTag",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateFlowTagResponse,
        body,
        operation_name="UpdateFlowTag",
        method="put",
        path="/flow_tag/v202404alpha1/tag/{flowTag.id}",
    )


def DeleteFlowTag(
    api_config_override: Optional[APIConfig] = None, *, flowTagid: str
) -> DeleteFlowTagResponse:
    """
    Delete flow tag configuration.

    Delete a flow tag configuration with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/flow_tag/v202404alpha1/tag/{path_segment(flowTagid)}",
        path_template="/flow_tag/v202404alpha1/tag/{flowTag.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteFlowTag",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteFlowTagResponse,
        body,
        operation_name="DeleteFlowTag",
        method="delete",
        path="/flow_tag/v202404alpha1/tag/{flowTag.id}",
    )
