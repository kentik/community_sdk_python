# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import GetError
from ..models import (  # noqa: F401
    AppProtocol,
    AppProtocolMetadata,
    AssetTag,
    BaseUnit,
    DimensionField,
    FieldDataType,
    FieldDirection,
    GetDictionaryResponse,
    MeasurementDetail,
    MeasurementFamily,
    MetricFamilyDef,
    MetricField,
    MetricQuantity,
    Operator,
    OperatorSet,
    OperatorSetKey,
    protobufAny,
    rpcStatus,
)


def GetDictionary(
    api_config_override: Optional[APIConfig] = None,
) -> GetDictionaryResponse:
    """
    Get Dictionary

    Returns the full UDE dictionary for the authenticated company, including all measurements with their dimension and metric fields, operator sets, and metric family definitions.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/dictionary/v20260604alpha1",
        path_template="/dictionary/v20260604alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetDictionary",
        error_cls=GetError,
    )

    return parse_response_model(
        GetDictionaryResponse,
        body,
        operation_name="GetDictionary",
        method="get",
        path="/dictionary/v20260604alpha1",
    )
