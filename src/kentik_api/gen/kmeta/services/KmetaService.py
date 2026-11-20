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
    CreateServiceNowConfigError,
    DeleteServiceNowConfigError,
    GetServiceNowConfigError,
    ListServiceNowConfigsError,
    UpdateServiceNowConfigError,
)
from ..models import (  # noqa: F401
    CreateServiceNowConfigResponse,
    DeleteServiceNowConfigResponse,
    GetServiceNowConfigResponse,
    ListServiceNowConfigsResponse,
    ServiceNowConfig,
    UpdateServiceNowConfigResponse,
    protobufAny,
    rpcStatus,
)


def ListServiceNowConfigs(
    api_config_override: Optional[APIConfig] = None, *, cid: str
) -> ListServiceNowConfigsResponse:
    """
    List ServiceNow Configs

    Returns all ServiceNow integration configurations for the specified company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kmeta/v202607alpha1/{path_segment(cid)}/servicenow/config",
        path_template="/kmeta/v202607alpha1/{cid}/servicenow/config",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListServiceNowConfigs",
        error_cls=ListServiceNowConfigsError,
    )

    return parse_response_model(
        ListServiceNowConfigsResponse,
        body,
        operation_name="ListServiceNowConfigs",
        method="get",
        path="/kmeta/v202607alpha1/{cid}/servicenow/config",
    )


def CreateServiceNowConfig(
    api_config_override: Optional[APIConfig] = None, *, cid: str, data: ServiceNowConfig
) -> CreateServiceNowConfigResponse:
    """
    Create ServiceNow Config

    Creates a new ServiceNow integration configuration for the specified company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/kmeta/v202607alpha1/{path_segment(cid)}/servicenow/config",
        path_template="/kmeta/v202607alpha1/{cid}/servicenow/config",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateServiceNowConfig",
        error_cls=CreateServiceNowConfigError,
    )

    return parse_response_model(
        CreateServiceNowConfigResponse,
        body,
        operation_name="CreateServiceNowConfig",
        method="post",
        path="/kmeta/v202607alpha1/{cid}/servicenow/config",
    )


def GetServiceNowConfig(
    api_config_override: Optional[APIConfig] = None, *, cid: str, id: str
) -> GetServiceNowConfigResponse:
    """
    Get ServiceNow Config

    Returns a single ServiceNow integration configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kmeta/v202607alpha1/{path_segment(cid)}/servicenow/config/{path_segment(id)}",
        path_template="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetServiceNowConfig",
        error_cls=GetServiceNowConfigError,
    )

    return parse_response_model(
        GetServiceNowConfigResponse,
        body,
        operation_name="GetServiceNowConfig",
        method="get",
        path="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
    )


def UpdateServiceNowConfig(
    api_config_override: Optional[APIConfig] = None,
    *,
    cid: str,
    id: str,
    data: ServiceNowConfig,
) -> UpdateServiceNowConfigResponse:
    """
    Update ServiceNow Config

    Updates an existing ServiceNow integration configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/kmeta/v202607alpha1/{path_segment(cid)}/servicenow/config/{path_segment(id)}",
        path_template="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateServiceNowConfig",
        error_cls=UpdateServiceNowConfigError,
    )

    return parse_response_model(
        UpdateServiceNowConfigResponse,
        body,
        operation_name="UpdateServiceNowConfig",
        method="put",
        path="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
    )


def DeleteServiceNowConfig(
    api_config_override: Optional[APIConfig] = None, *, cid: str, id: str
) -> DeleteServiceNowConfigResponse:
    """
    Delete ServiceNow Config

    Deletes a ServiceNow integration configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/kmeta/v202607alpha1/{path_segment(cid)}/servicenow/config/{path_segment(id)}",
        path_template="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteServiceNowConfig",
        error_cls=DeleteServiceNowConfigError,
    )

    return parse_response_model(
        DeleteServiceNowConfigResponse,
        body,
        operation_name="DeleteServiceNowConfig",
        method="delete",
        path="/kmeta/v202607alpha1/{cid}/servicenow/config/{id}",
    )
