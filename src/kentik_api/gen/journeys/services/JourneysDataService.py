# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import GetNlqError
from ..models import (  # noqa: F401
    GetJourneysNlqResponse,
    ResultFormat,
    ResultType,
    protobufAny,
    rpcStatus,
)


def GetJourneysNlq(
    api_config_override: Optional[APIConfig] = None, *, prompt: str
) -> GetJourneysNlqResponse:
    """
    Journeys AI NLQ Service

    Perform Natural Language (NLQ) to query object translation
    """
    query_params: Dict[str, Any] = {"prompt": prompt}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/journeys/v202406/GetJourneysNlq",
        path_template="/journeys/v202406/GetJourneysNlq",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetJourneysNlq",
        error_cls=GetNlqError,
    )

    return parse_response_model(
        GetJourneysNlqResponse,
        body,
        operation_name="GetJourneysNlq",
        method="get",
        path="/journeys/v202406/GetJourneysNlq",
    )
