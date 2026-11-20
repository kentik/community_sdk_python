# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import CreateError, DeleteError, GetError, ListError, UpdateError
from ..models import (  # noqa: F401
    ASGroupConcise,
    ASGroupDetailed,
    ASGroupServiceUpdateASGroupBody,
    AutonomousSystem,
    CreateASGroupRequest,
    CreateASGroupResponse,
    DeleteASGroupResponse,
    GetASGroupResponse,
    ListASGroupsResponse,
    UpdateASGroupResponse,
    protobufAny,
    rpcStatus,
)


def ListASGroups(
    api_config_override: Optional[APIConfig] = None,
) -> ListASGroupsResponse:
    """
    List all AS groups.

    Returns list of configured AS groups.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/as_group/v202212/as_group",
        path_template="/as_group/v202212/as_group",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListASGroups",
        error_cls=ListError,
    )

    return parse_response_model(
        ListASGroupsResponse,
        body,
        operation_name="ListASGroups",
        method="get",
        path="/as_group/v202212/as_group",
    )


def CreateASGroup(
    api_config_override: Optional[APIConfig] = None, *, data: CreateASGroupRequest
) -> CreateASGroupResponse:
    """
    Configure a new AS group.

    Create configuration for a new AS group. Returns the newly created configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/as_group/v202212/as_group",
        path_template="/as_group/v202212/as_group",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateASGroup",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateASGroupResponse,
        body,
        operation_name="CreateASGroup",
        method="post",
        path="/as_group/v202212/as_group",
    )


def GetASGroup(
    api_config_override: Optional[APIConfig] = None, *, asGroupid: str
) -> GetASGroupResponse:
    """
    Retrieve configuration of a AS group.

    Returns configuration of a AS group specified by ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/as_group/v202212/as_group/{path_segment(asGroupid)}",
        path_template="/as_group/v202212/as_group/{asGroup.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetASGroup",
        error_cls=GetError,
    )

    return parse_response_model(
        GetASGroupResponse,
        body,
        operation_name="GetASGroup",
        method="get",
        path="/as_group/v202212/as_group/{asGroup.id}",
    )


def UpdateASGroup(
    api_config_override: Optional[APIConfig] = None,
    *,
    asGroupid: str,
    data: ASGroupServiceUpdateASGroupBody,
) -> UpdateASGroupResponse:
    """
    Updates configuration of a AS group.

    Replaces configuration of a AS group with attributes in the request. Returns the updated configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/as_group/v202212/as_group/{path_segment(asGroupid)}",
        path_template="/as_group/v202212/as_group/{asGroup.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        # Upstream REST drops this camelCase key: AGENTS.md, Upstream workarounds.
        json_body={
            {"asGroup": "as_group"}.get(key, key): value
            for key, value in data.model_dump(by_alias=True, exclude_unset=True).items()
        },
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateASGroup",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateASGroupResponse,
        body,
        operation_name="UpdateASGroup",
        method="put",
        path="/as_group/v202212/as_group/{asGroup.id}",
    )


def DeleteASGroup(
    api_config_override: Optional[APIConfig] = None, *, asGroupid: str
) -> DeleteASGroupResponse:
    """
    Delete configuration of a AS group.

    Deletes configuration of a AS group with specific ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/as_group/v202212/as_group/{path_segment(asGroupid)}",
        path_template="/as_group/v202212/as_group/{asGroup.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteASGroup",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteASGroupResponse,
        body,
        operation_name="DeleteASGroup",
        method="delete",
        path="/as_group/v202212/as_group/{asGroup.id}",
    )
