# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import GetError, UpdateError
from ..models import (  # noqa: F401
    CloudSubnet,
    CloudType,
    GetNetworkClassResponse,
    NetworkClass,
    UpdateNetworkClassRequest,
    UpdateNetworkClassResponse,
    protobufAny,
    rpcStatus,
)


def NetworkClassGet(
    api_config_override: Optional[APIConfig] = None,
) -> GetNetworkClassResponse:
    """
    Get a network classification.

    Returns information about a network classification for the company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/network_class/v202109alpha1/network_class",
        path_template="/network_class/v202109alpha1/network_class",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="NetworkClassGet",
        error_cls=GetError,
    )

    return parse_response_model(
        GetNetworkClassResponse,
        body,
        operation_name="NetworkClassGet",
        method="get",
        path="/network_class/v202109alpha1/network_class",
    )


def NetworkClassUpdate(
    api_config_override: Optional[APIConfig] = None, *, data: UpdateNetworkClassRequest
) -> UpdateNetworkClassResponse:
    """
    Update a network classification.

    Replaces the entire network classification attributes for the company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/network_class/v202109alpha1/network_class",
        path_template="/network_class/v202109alpha1/network_class",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="NetworkClassUpdate",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateNetworkClassResponse,
        body,
        operation_name="NetworkClassUpdate",
        method="post",
        path="/network_class/v202109alpha1/network_class",
    )
