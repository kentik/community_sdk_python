# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import GetMetricsForTargetError, GetRoutesForTargetError
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


def GetMetricsForTarget(
    api_config_override: Optional[APIConfig] = None, *, data: GetMetricsForTargetRequest
) -> GetMetricsForTargetResponse:
    """
    Get metrics for a BGP prefix.

    Retrieve metric data for single BGP prefix and time interval.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/bgp_monitoring/v202210/metrics",
        path_template="/bgp_monitoring/v202210/metrics",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetMetricsForTarget",
        error_cls=GetMetricsForTargetError,
    )

    return parse_response_model(
        GetMetricsForTargetResponse,
        body,
        operation_name="GetMetricsForTarget",
        method="post",
        path="/bgp_monitoring/v202210/metrics",
    )


def GetRoutesForTarget(
    api_config_override: Optional[APIConfig] = None, *, data: GetRoutesForTargetRequest
) -> GetRoutesForTargetResponse:
    """
    Get routes for a BGP prefix.

    Retrieve snapshot of route information for single BGP prefix at specific time.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/bgp_monitoring/v202210/routes",
        path_template="/bgp_monitoring/v202210/routes",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetRoutesForTarget",
        error_cls=GetRoutesForTargetError,
    )

    return parse_response_model(
        GetRoutesForTargetResponse,
        body,
        operation_name="GetRoutesForTarget",
        method="post",
        path="/bgp_monitoring/v202210/routes",
    )
