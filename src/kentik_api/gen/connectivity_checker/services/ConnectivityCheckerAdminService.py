# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import CreateConnectivityReportError
from ..models import (  # noqa: F401
    CloudProvider,
    CreateConnectivityReportRequest,
    CreateConnectivityReportResponse,
    EntityType,
    protobufAny,
    rpcStatus,
)


def CreateConnectivityReport(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: CreateConnectivityReportRequest,
) -> CreateConnectivityReportResponse:
    """
    Create a Connectivity Checker Report.

    Create a connectivity checker report based on configuration provided in the request.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/connectivity_checker/v202410beta1/create",
        path_template="/connectivity_checker/v202410beta1/create",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateConnectivityReport",
        error_cls=CreateConnectivityReportError,
    )

    return parse_response_model(
        CreateConnectivityReportResponse,
        body,
        operation_name="CreateConnectivityReport",
        method="post",
        path="/connectivity_checker/v202410beta1/create",
    )
