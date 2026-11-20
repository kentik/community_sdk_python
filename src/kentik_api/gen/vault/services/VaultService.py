# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import GetSecretError, ListSecretError
from ..models import (  # noqa: F401
    GetSecretResponse,
    ListSecretResponse,
    Secret,
    SecretType,
    protobufAny,
    rpcStatus,
)


def ListSecret(
    api_config_override: Optional[APIConfig] = None, *, names: List[str]
) -> ListSecretResponse:
    """
    List secrets.

    Returns list of secret values stored in Kentik vault.
    """
    query_params: Dict[str, Any] = {"names": names}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/vault/v202312alpha1/secrets",
        path_template="/vault/v202312alpha1/secrets",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListSecret",
        error_cls=ListSecretError,
    )

    return parse_response_model(
        ListSecretResponse,
        body,
        operation_name="ListSecret",
        method="get",
        path="/vault/v202312alpha1/secrets",
    )


def GetSecret(
    api_config_override: Optional[APIConfig] = None, *, name: str
) -> GetSecretResponse:
    """
    Get a secret by name.

    Returns a secret value stored in Kentik vault.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/vault/v202312alpha1/secrets/{path_segment(name)}",
        path_template="/vault/v202312alpha1/secrets/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetSecret",
        error_cls=GetSecretError,
    )

    return parse_response_model(
        GetSecretResponse,
        body,
        operation_name="GetSecret",
        method="get",
        path="/vault/v202312alpha1/secrets/{name}",
    )
