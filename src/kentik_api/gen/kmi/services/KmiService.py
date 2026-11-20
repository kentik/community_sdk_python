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
    GetAsnDetailsError,
    GetAsnInsightsError,
    GetGlobalInsightsError,
    GetRankingsError,
    ListMarketsError,
)
from ..models import (  # noqa: F401
    ASNDetails,
    CustomerProvider,
    GetASNDetailsResponse,
    GetASNInsightsResponse,
    GetGlobalInsightsResponse,
    GetRankingsResponse,
    Insight,
    KmiServiceGetASNDetailsBody,
    KmiServiceGetRankingsBody,
    ListMarketsResponse,
    Market,
    Peer,
    Ranking,
    protobufAny,
    rpcStatus,
)


def GetGlobalInsights(
    api_config_override: Optional[APIConfig] = None,
    *,
    limit: Optional[int] = None,
    marketId: Optional[str] = None,
    ip: Optional[str] = None,
    lookback: Optional[int] = None,
    types: Optional[List[str]] = None,
    magnitude: Optional[int] = None,
) -> GetGlobalInsightsResponse:
    """
    List global KMI insights.

    Returns list of global KMI insights.
    """
    query_params: Dict[str, Any] = {
        "limit": limit,
        "marketId": marketId,
        "ip": ip,
        "lookback": lookback,
        "types": types,
        "magnitude": magnitude,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kmi/v202212/insights",
        path_template="/kmi/v202212/insights",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetGlobalInsights",
        error_cls=GetGlobalInsightsError,
    )

    return parse_response_model(
        GetGlobalInsightsResponse,
        body,
        operation_name="GetGlobalInsights",
        method="get",
        path="/kmi/v202212/insights",
    )


def GetASNInsights(
    api_config_override: Optional[APIConfig] = None,
    *,
    asn: str,
    limit: Optional[int] = None,
    marketId: Optional[str] = None,
    ip: Optional[str] = None,
    lookback: Optional[int] = None,
    types: Optional[List[str]] = None,
    magnitude: Optional[int] = None,
) -> GetASNInsightsResponse:
    """
    List ASN-specific KMI insights.

    Returns list of KMI insights for a specific Autonomous System.
    """
    query_params: Dict[str, Any] = {
        "limit": limit,
        "marketId": marketId,
        "ip": ip,
        "lookback": lookback,
        "types": types,
        "magnitude": magnitude,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/kmi/v202212/insights/{path_segment(asn)}",
        path_template="/kmi/v202212/insights/{asn}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetASNInsights",
        error_cls=GetAsnInsightsError,
    )

    return parse_response_model(
        GetASNInsightsResponse,
        body,
        operation_name="GetASNInsights",
        method="get",
        path="/kmi/v202212/insights/{asn}",
    )


def GetASNDetails(
    api_config_override: Optional[APIConfig] = None,
    *,
    marketId: str,
    asn: str,
    type: str,
    data: KmiServiceGetASNDetailsBody,
) -> GetASNDetailsResponse:
    """
    List metadata and list of customers, providers, and peers for an Autonomous System.

    Returns metadata and list of customers, providers, and peers for an Autonomous System.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/kmi/v202212/market/{path_segment(marketId)}/network/{path_segment(asn)}/{path_segment(type)}",
        path_template="/kmi/v202212/market/{marketId}/network/{asn}/{type}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetASNDetails",
        error_cls=GetAsnDetailsError,
    )

    return parse_response_model(
        GetASNDetailsResponse,
        body,
        operation_name="GetASNDetails",
        method="post",
        path="/kmi/v202212/market/{marketId}/network/{asn}/{type}",
    )


def GetRankings(
    api_config_override: Optional[APIConfig] = None,
    *,
    marketId: str,
    rankType: str,
    ip: str,
    data: KmiServiceGetRankingsBody,
) -> GetRankingsResponse:
    """
    List KMI rankings by geo market and rank type.

    Returns list of KMI rankings.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/kmi/v202212/market/{path_segment(marketId)}/rankings/{path_segment(rankType)}/ip/{path_segment(ip)}",
        path_template="/kmi/v202212/market/{marketId}/rankings/{rankType}/ip/{ip}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetRankings",
        error_cls=GetRankingsError,
    )

    return parse_response_model(
        GetRankingsResponse,
        body,
        operation_name="GetRankings",
        method="post",
        path="/kmi/v202212/market/{marketId}/rankings/{rankType}/ip/{ip}",
    )


def ListMarkets(api_config_override: Optional[APIConfig] = None) -> ListMarketsResponse:
    """
    List all geo markets for KMI.

    Returns list of geo markets for KMI.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/kmi/v202212/markets",
        path_template="/kmi/v202212/markets",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListMarkets",
        error_cls=ListMarketsError,
    )

    return parse_response_model(
        ListMarketsResponse,
        body,
        operation_name="ListMarkets",
        method="get",
        path="/kmi/v202212/markets",
    )
