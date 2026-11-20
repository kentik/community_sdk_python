# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import RouteAnnounceError, RouteListError, RouteWithdrawError
from ..models import (  # noqa: F401
    AdvertStatus,
    BitwiseOp,
    DeviceAdverts,
    ExtendedCommunityRouteType,
    FlowspecAction,
    FlowspecActionAccept,
    FlowspecActionDiscard,
    FlowspecActionExtendedCommunity,
    FlowspecActionIPNextHopCopy,
    FlowspecActionIPNextHopRedirect,
    FlowspecActionLargeCommunity,
    FlowspecActionMarkDSCP,
    FlowspecActionRegularCommunity,
    FlowspecActionRouteTargetRedirect,
    FlowspecActionTerminalSample,
    FlowspecActionTrafficRateBytes,
    FlowspecMatch,
    FlowspecUpdate,
    Fragment,
    FragmentFormula,
    FragmentPredicate,
    FragmentPredicateGroup,
    InetType,
    NumericFormula,
    NumericOp,
    NumericPredicate,
    NumericPredicateGroup,
    RouteServiceAnnounceRequest,
    RouteServiceAnnounceResponse,
    RouteServiceListRequest,
    RouteServiceListResponse,
    RouteServiceWithdrawRequest,
    RouteServiceWithdrawResponse,
    RoutesFilter,
    RTBHAction,
    RTBHMatch,
    RTBHUpdate,
    TCPFlag,
    TCPFlagsFormula,
    TCPFlagsPredicate,
    TCPFlagsPredicateGroup,
    UpdateResult,
    Withdraw,
    protobufAny,
    rpcStatus,
)


def RouteService_Announce(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: RouteServiceAnnounceRequest,
) -> RouteServiceAnnounceResponse:
    """
    Announce a BGP route to a specified set of devices
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/routes/announce",
        path_template="/routes/announce",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="RouteService_Announce",
        error_cls=RouteAnnounceError,
    )

    return parse_response_model(
        RouteServiceAnnounceResponse,
        body,
        operation_name="RouteService_Announce",
        method="post",
        path="/routes/announce",
    )


def RouteService_List(
    api_config_override: Optional[APIConfig] = None, *, data: RouteServiceListRequest
) -> RouteServiceListResponse:
    """
    List active BGP updates for a specified set of devices
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/routes/list",
        path_template="/routes/list",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="RouteService_List",
        error_cls=RouteListError,
    )

    return parse_response_model(
        RouteServiceListResponse,
        body,
        operation_name="RouteService_List",
        method="post",
        path="/routes/list",
    )


def RouteService_Withdraw(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: RouteServiceWithdrawRequest,
) -> RouteServiceWithdrawResponse:
    """
    Withdraw active BGP updates from devices
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/routes/withdraw",
        path_template="/routes/withdraw",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="RouteService_Withdraw",
        error_cls=RouteWithdrawError,
    )

    return parse_response_model(
        RouteServiceWithdrawResponse,
        body,
        operation_name="RouteService_Withdraw",
        method="post",
        path="/routes/withdraw",
    )
