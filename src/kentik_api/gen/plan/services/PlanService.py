# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import ListError
from ..models import (  # noqa: F401
    DeviceSubtype,
    ListPlansResponse,
    Plan,
    PlanDevice,
    protobufAny,
    rpcStatus,
)


def ListPlans(api_config_override: Optional[APIConfig] = None) -> ListPlansResponse:
    """
    List Plans

    Returns all plans configured for the user's company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/plans/v202501alpha1",
        path_template="/plans/v202501alpha1",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListPlans",
        error_cls=ListError,
    )

    return parse_response_model(
        ListPlansResponse,
        body,
        operation_name="ListPlans",
        method="get",
        path="/plans/v202501alpha1",
    )
