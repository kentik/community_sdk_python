# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

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
    ListError,
    ManualClassifyError,
    UpdateError,
)
from ..models import (  # noqa: F401
    ConnectivityType,
    CreateInterfaceRequest,
    CreateInterfaceResponse,
    DeleteInterfaceResponse,
    GetInterfaceResponse,
    Interface,
    InterfaceFilter,
    InterfaceServiceUpdateInterfaceBody,
    InterfaceVrf,
    IpFilter,
    ListInterfaceResponse,
    ManualClassifyRequest,
    ManualClassifyResponse,
    NetworkBoundary,
    UpdateInterfaceResponse,
    protobufAny,
    rpcStatus,
)


def ListInterface(
    api_config_override: Optional[APIConfig] = None,
    *,
    filterstext: Optional[str] = None,
    filtersdeviceIds: Optional[List[str]] = None,
    filtersconnectivityTypes: Optional[List[str]] = None,
    filtersnetworkBoundaries: Optional[List[str]] = None,
    filtersproviders: Optional[List[str]] = None,
    filterssnmpSpeeds: Optional[List[int]] = None,
    filtersipTypes: Optional[List[str]] = None,
) -> ListInterfaceResponse:
    """
    Fetch Search Interfaces

    Return list of interfaces matches search critera.
    """
    query_params: Dict[str, Any] = {
        "filters.text": filterstext,
        "filters.deviceIds": filtersdeviceIds,
        "filters.connectivityTypes": filtersconnectivityTypes,
        "filters.networkBoundaries": filtersnetworkBoundaries,
        "filters.providers": filtersproviders,
        "filters.snmpSpeeds": filterssnmpSpeeds,
        "filters.ipTypes": filtersipTypes,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/interface/v202108alpha1/interfaces",
        path_template="/interface/v202108alpha1/interfaces",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListInterface",
        error_cls=ListError,
    )

    return parse_response_model(
        ListInterfaceResponse,
        body,
        operation_name="ListInterface",
        method="get",
        path="/interface/v202108alpha1/interfaces",
    )


def InterfaceCreate(
    api_config_override: Optional[APIConfig] = None, *, data: CreateInterfaceRequest
) -> CreateInterfaceResponse:
    """
    Create a interface.

    Create a interface from request. returns created.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/interface/v202108alpha1/interfaces",
        path_template="/interface/v202108alpha1/interfaces",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="InterfaceCreate",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateInterfaceResponse,
        body,
        operation_name="InterfaceCreate",
        method="post",
        path="/interface/v202108alpha1/interfaces",
    )


def InterfaceGet(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetInterfaceResponse:
    """
    Get a interface.

    Returns information about a interface specified with ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/interface/v202108alpha1/interfaces/{path_segment(id)}",
        path_template="/interface/v202108alpha1/interfaces/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="InterfaceGet",
        error_cls=GetError,
    )

    return parse_response_model(
        GetInterfaceResponse,
        body,
        operation_name="InterfaceGet",
        method="get",
        path="/interface/v202108alpha1/interfaces/{id}",
    )


def InterfaceUpdate(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: InterfaceServiceUpdateInterfaceBody,
) -> UpdateInterfaceResponse:
    """
    Update a interface.

    Replaces the entire interface attributes specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/interface/v202108alpha1/interfaces/{path_segment(id)}",
        path_template="/interface/v202108alpha1/interfaces/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="InterfaceUpdate",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateInterfaceResponse,
        body,
        operation_name="InterfaceUpdate",
        method="put",
        path="/interface/v202108alpha1/interfaces/{id}",
    )


def InterfaceDelete(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteInterfaceResponse:
    """
    Delete a interface.

    Deletes the interface specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/interface/v202108alpha1/interfaces/{path_segment(id)}",
        path_template="/interface/v202108alpha1/interfaces/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="InterfaceDelete",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteInterfaceResponse,
        body,
        operation_name="InterfaceDelete",
        method="delete",
        path="/interface/v202108alpha1/interfaces/{id}",
    )


def ManualClassify(
    api_config_override: Optional[APIConfig] = None, *, data: ManualClassifyRequest
) -> ManualClassifyResponse:
    """
    Manual Classify Interface

    Manually set interface(s) classification.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/interface/v202108alpha1/manual_classify",
        path_template="/interface/v202108alpha1/manual_classify",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="ManualClassify",
        error_cls=ManualClassifyError,
    )

    return parse_response_model(
        ManualClassifyResponse,
        body,
        operation_name="ManualClassify",
        method="post",
        path="/interface/v202108alpha1/manual_classify",
    )
