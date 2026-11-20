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
    GetProviderSummaryError,
    ListProvidersError,
    ListProviderSummariesError,
)
from ..models import (  # noqa: F401
    CostProviderConcise,
    CostProviderSummary,
    GetCostProviderSummaryResponse,
    ListCostProvidersResponse,
    ListCostProviderSummariesResponse,
    Status,
    googlerpcStatus,
    protobufAny,
)


def ListCostProviders(
    api_config_override: Optional[APIConfig] = None,
) -> ListCostProvidersResponse:
    """
    List all cost providers.

    Returns list of configured cost providers.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/cost/v202308/cost/providers",
        path_template="/cost/v202308/cost/providers",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCostProviders",
        error_cls=ListProvidersError,
    )

    return parse_response_model(
        ListCostProvidersResponse,
        body,
        operation_name="ListCostProviders",
        method="get",
        path="/cost/v202308/cost/providers",
    )


def ListCostProviderSummaries(
    api_config_override: Optional[APIConfig] = None, *, date: Optional[str] = None
) -> ListCostProviderSummariesResponse:
    """
    List all cost provider summaries.

    Returns list of summaries of configured cost providers.
    """
    query_params: Dict[str, Any] = {"date": date}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/cost/v202308/cost/summary",
        path_template="/cost/v202308/cost/summary",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCostProviderSummaries",
        error_cls=ListProviderSummariesError,
    )

    return parse_response_model(
        ListCostProviderSummariesResponse,
        body,
        operation_name="ListCostProviderSummaries",
        method="get",
        path="/cost/v202308/cost/summary",
    )


def GetCostProviderSummary(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    date: Optional[str] = None,
) -> GetCostProviderSummaryResponse:
    """
    Get cost provider summary.

    Returns summary of configured cost provider.
    """
    query_params: Dict[str, Any] = {"date": date}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/cost/v202308/cost/summary/{path_segment(id)}",
        path_template="/cost/v202308/cost/summary/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetCostProviderSummary",
        error_cls=GetProviderSummaryError,
    )

    return parse_response_model(
        GetCostProviderSummaryResponse,
        body,
        operation_name="GetCostProviderSummary",
        method="get",
        path="/cost/v202308/cost/summary/{id}",
    )
