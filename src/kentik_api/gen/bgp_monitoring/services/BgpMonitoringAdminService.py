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
    CreateMonitorError,
    DeleteMonitorError,
    GetMonitorError,
    ListMonitorsError,
    SetMonitorStatusError,
    UpdateMonitorError,
)
from ..models import (  # noqa: F401
    Afi,
    BgpHealthSettings,
    BgpMetric,
    BgpMetricType,
    BgpMonitor,
    BgpMonitoringAdminServiceSetMonitorStatusBody,
    BgpMonitoringAdminServiceUpdateMonitorBody,
    BgpMonitorSettings,
    BgpMonitorStatus,
    CreateMonitorRequest,
    CreateMonitorResponse,
    DeleteMonitorResponse,
    GetMetricsForTargetRequest,
    GetMetricsForTargetResponse,
    GetMonitorResponse,
    GetRoutesForTargetRequest,
    GetRoutesForTargetResponse,
    ListMonitorsResponse,
    Nlri,
    RouteInfo,
    RpkiStatus,
    Safi,
    SetMonitorStatusResponse,
    UpdateMonitorResponse,
    UserInfo,
    VantagePoint,
    protobufAny,
    rpcStatus,
)


def ListMonitors(
    api_config_override: Optional[APIConfig] = None,
) -> ListMonitorsResponse:
    """
    List BGP Monitors.

    Returns list of all BGP monitors present in the account.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/bgp_monitoring/v202210/monitors",
        path_template="/bgp_monitoring/v202210/monitors",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListMonitors",
        error_cls=ListMonitorsError,
    )

    return parse_response_model(
        ListMonitorsResponse,
        body,
        operation_name="ListMonitors",
        method="get",
        path="/bgp_monitoring/v202210/monitors",
    )


def CreateMonitor(
    api_config_override: Optional[APIConfig] = None, *, data: CreateMonitorRequest
) -> CreateMonitorResponse:
    """
    Create new BGP Monitor instance.

    Creates new BGP Monitor and if successful returns its configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/bgp_monitoring/v202210/monitors",
        path_template="/bgp_monitoring/v202210/monitors",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateMonitor",
        error_cls=CreateMonitorError,
    )

    return parse_response_model(
        CreateMonitorResponse,
        body,
        operation_name="CreateMonitor",
        method="post",
        path="/bgp_monitoring/v202210/monitors",
    )


def GetMonitor(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetMonitorResponse:
    """
    Get BGP Monitor configuration.

    Returns configuration of existing BGP monitor with specific ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/bgp_monitoring/v202210/monitors/{path_segment(id)}",
        path_template="/bgp_monitoring/v202210/monitors/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetMonitor",
        error_cls=GetMonitorError,
    )

    return parse_response_model(
        GetMonitorResponse,
        body,
        operation_name="GetMonitor",
        method="get",
        path="/bgp_monitoring/v202210/monitors/{id}",
    )


def UpdateMonitor(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: BgpMonitoringAdminServiceUpdateMonitorBody,
) -> UpdateMonitorResponse:
    """
    Update configuration of a BGP monitor.

    Updates configuration of BGP monitor with specific ID and returns updated  configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/bgp_monitoring/v202210/monitors/{path_segment(id)}",
        path_template="/bgp_monitoring/v202210/monitors/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateMonitor",
        error_cls=UpdateMonitorError,
    )

    return parse_response_model(
        UpdateMonitorResponse,
        body,
        operation_name="UpdateMonitor",
        method="put",
        path="/bgp_monitoring/v202210/monitors/{id}",
    )


def DeleteMonitor(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteMonitorResponse:
    """
    Delete existing BGP Monitor.

    Delete BGP monitor with with specific ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/bgp_monitoring/v202210/monitors/{path_segment(id)}",
        path_template="/bgp_monitoring/v202210/monitors/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteMonitor",
        error_cls=DeleteMonitorError,
    )

    return parse_response_model(
        DeleteMonitorResponse,
        body,
        operation_name="DeleteMonitor",
        method="delete",
        path="/bgp_monitoring/v202210/monitors/{id}",
    )


def SetMonitorStatus(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: BgpMonitoringAdminServiceSetMonitorStatusBody,
) -> SetMonitorStatusResponse:
    """
    Sets administrative status of a BGP monitor.

    Sets administrative status of BGP monitor with specific ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/bgp_monitoring/v202210/monitors/{path_segment(id)}/status",
        path_template="/bgp_monitoring/v202210/monitors/{id}/status",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="SetMonitorStatus",
        error_cls=SetMonitorStatusError,
    )

    return parse_response_model(
        SetMonitorStatusResponse,
        body,
        operation_name="SetMonitorStatus",
        method="put",
        path="/bgp_monitoring/v202210/monitors/{id}/status",
    )
