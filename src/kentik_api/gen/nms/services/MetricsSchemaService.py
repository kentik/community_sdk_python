# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import GetMetricsSchemaError
from ..models import (  # noqa: F401
    FieldDisplay,
    FieldSchema,
    FieldType,
    GetMetricsSchemaResponse,
    MeasurementSchema,
    MetricsSchema,
    Usage,
    protobufAny,
    rpcStatus,
)


def MetricsSchemaService_GetMetricsSchema(
    api_config_override: Optional[APIConfig] = None,
) -> GetMetricsSchemaResponse:
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/nms/v202505/metrics_schema",
        path_template="/nms/v202505/metrics_schema",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="MetricsSchemaService_GetMetricsSchema",
        error_cls=GetMetricsSchemaError,
    )

    return parse_response_model(
        GetMetricsSchemaResponse,
        body,
        operation_name="MetricsSchemaService_GetMetricsSchema",
        method="get",
        path="/nms/v202505/metrics_schema",
    )
