# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import CreateReportError
from ..models import (  # noqa: F401
    CloudProvider,
    CreatePathfinderReportRequest,
    CreatePathfinderReportResponse,
    EntityType,
    PathElement,
    protobufAny,
    rpcStatus,
)


def CreatePathfinderReport(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: CreatePathfinderReportRequest,
) -> CreatePathfinderReportResponse:
    """
    Create a Pathfinder Report.

    Create a pathfinder report based on configuration provided in the request.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/pathfinder/v202505beta1/create",
        path_template="/pathfinder/v202505beta1/create",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreatePathfinderReport",
        error_cls=CreateReportError,
    )

    return parse_response_model(
        CreatePathfinderReportResponse,
        body,
        operation_name="CreatePathfinderReport",
        method="post",
        path="/pathfinder/v202505beta1/create",
    )
