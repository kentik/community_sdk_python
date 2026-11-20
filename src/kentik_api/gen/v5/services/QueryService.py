# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import QueryUrlError, TopXChartError, TopXDataError
from ..models import (  # noqa: F401
    Aggregate,
    BatchCriterion,
    BatchDelete,
    BatchDeleteCounts,
    BatchPart,
    BatchReplaceAll,
    BatchResponse,
    BatchStatus,
    BatchStatusCustomDimension,
    BatchStatusUser,
    BatchUpsert,
    BatchUpsertCounts,
    ChartRequest,
    ChartResponse,
    Filter,
    FilterGroup,
    Query,
    QueryFilters,
    QueryItem,
    QueryRequest,
    ResultBucket,
    SavedFilterRef,
    TopXDataResponse,
    V5Error,
)


def QueryService_TopXData(
    api_config_override: Optional[APIConfig] = None, *, data: QueryRequest
) -> TopXDataResponse:
    """
    Top-X data query

    Runs one or more queries on the Kentik Data Engine and returns the result rows of each bucket, with time series for the top-X rows.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/query/topXdata",
        path_template="/query/topXdata",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="QueryService_TopXData",
        error_cls=TopXDataError,
    )

    return parse_response_model(
        TopXDataResponse,
        body,
        operation_name="QueryService_TopXData",
        method="post",
        path="/query/topXdata",
    )


def QueryService_TopXChart(
    api_config_override: Optional[APIConfig] = None, *, data: ChartRequest
) -> ChartResponse:
    """
    Top-X chart query

    Runs one or more queries and returns a chart image as a base64 data URI. Not verified: in a live check on 2026-10-16 this endpoint gave no response within 180 seconds. Decode the result with kentik_api.v5_tools.decode_chart().
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/query/topXchart",
        path_template="/query/topXchart",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="QueryService_TopXChart",
        error_cls=TopXChartError,
    )

    return parse_response_model(
        ChartResponse,
        body,
        operation_name="QueryService_TopXChart",
        method="post",
        path="/query/topXchart",
    )


def QueryService_Url(
    api_config_override: Optional[APIConfig] = None, *, data: QueryRequest
) -> str:
    """
    Data Explorer URL

    Returns a link that opens Data Explorer in the Kentik portal with the sidebar set to the query.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/query/url",
        path_template="/query/url",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="QueryService_Url",
        error_cls=QueryUrlError,
    )

    return body
