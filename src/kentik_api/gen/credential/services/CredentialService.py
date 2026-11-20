# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    AssignConsumerError,
    CreateGroupError,
    DeleteError,
    DeleteGroupError,
    GetError,
    GetGroupError,
    ListError,
    ListGroupError,
    ListOverviewsError,
    UpdateGroupError,
)
from ..models import (  # noqa: F401
    AssignConsumerResponse,
    Consumer,
    CreateCredentialGroupRequest,
    CreateCredentialGroupResponse,
    CreatedBy,
    Credential,
    CredentialGroup,
    CredentialOverview,
    CredentialServiceAssignConsumerBody,
    CredentialServiceUpdateCredentialGroupBody,
    CredentialType,
    DeleteCredentialGroupResponse,
    DeleteCredentialResponse,
    GetCredentialGroupResponse,
    GetCredentialResponse,
    ListCredentialGroupResponse,
    ListCredentialOverviewsResponse,
    ListCredentialsResponse,
    Token,
    UpdateCredentialGroupResponse,
    protobufAny,
    rpcStatus,
)


def ListCredentials(
    api_config_override: Optional[APIConfig] = None,
) -> ListCredentialsResponse:
    """
    List credentials.

    Returns the latest version of every credential.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/credential/v20261020alpha1/credentials",
        path_template="/credential/v20261020alpha1/credentials",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCredentials",
        error_cls=ListError,
    )

    return parse_response_model(
        ListCredentialsResponse,
        body,
        operation_name="ListCredentials",
        method="get",
        path="/credential/v20261020alpha1/credentials",
    )


def GetCredential(
    api_config_override: Optional[APIConfig] = None,
    *,
    name: str,
    version: Optional[int] = None,
    allVersions: Optional[bool] = None,
) -> GetCredentialResponse:
    """
    Get a credential by name.

    Returns the latest, a specific, or every version of a credential.
    """
    query_params: Dict[str, Any] = {"version": version, "allVersions": allVersions}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/credential/v20261020alpha1/credentials/{path_segment(name)}",
        path_template="/credential/v20261020alpha1/credentials/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetCredential",
        error_cls=GetError,
    )

    return parse_response_model(
        GetCredentialResponse,
        body,
        operation_name="GetCredential",
        method="get",
        path="/credential/v20261020alpha1/credentials/{name}",
    )


def DeleteCredential(
    api_config_override: Optional[APIConfig] = None, *, name: str, version: int
) -> DeleteCredentialResponse:
    """
    Delete a credential version.

    Deletes a single version of a credential. Version Requires. Fails if the credential has consumers.
    """
    query_params: Dict[str, Any] = {"version": version}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/credential/v20261020alpha1/credentials/{path_segment(name)}",
        path_template="/credential/v20261020alpha1/credentials/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteCredential",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteCredentialResponse,
        body,
        operation_name="DeleteCredential",
        method="delete",
        path="/credential/v20261020alpha1/credentials/{name}",
    )


def AssignConsumer(
    api_config_override: Optional[APIConfig] = None,
    *,
    name: str,
    data: CredentialServiceAssignConsumerBody,
) -> AssignConsumerResponse:
    """
    Assign a consumer to a credential.

    Records that an entity (synthetic test, device, etc.) uses the credential.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/credential/v20261020alpha1/credentials/{path_segment(name)}/consumer",
        path_template="/credential/v20261020alpha1/credentials/{name}/consumer",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="AssignConsumer",
        error_cls=AssignConsumerError,
    )

    return parse_response_model(
        AssignConsumerResponse,
        body,
        operation_name="AssignConsumer",
        method="put",
        path="/credential/v20261020alpha1/credentials/{name}/consumer",
    )


def ListCredentialGroups(
    api_config_override: Optional[APIConfig] = None,
) -> ListCredentialGroupResponse:
    """
    List credential groups.

    Returns every credential group with the latest version of its credentials.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/credential/v20261020alpha1/groups",
        path_template="/credential/v20261020alpha1/groups",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCredentialGroups",
        error_cls=ListGroupError,
    )

    return parse_response_model(
        ListCredentialGroupResponse,
        body,
        operation_name="ListCredentialGroups",
        method="get",
        path="/credential/v20261020alpha1/groups",
    )


def CreateCredentialGroup(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: CreateCredentialGroupRequest,
) -> CreateCredentialGroupResponse:
    """
    Create a credential group.

    Creates one credential per token and returns the created group.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/credential/v20261020alpha1/groups",
        path_template="/credential/v20261020alpha1/groups",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateCredentialGroup",
        error_cls=CreateGroupError,
    )

    return parse_response_model(
        CreateCredentialGroupResponse,
        body,
        operation_name="CreateCredentialGroup",
        method="post",
        path="/credential/v20261020alpha1/groups",
    )


def GetCredentialGroup(
    api_config_override: Optional[APIConfig] = None, *, name: str
) -> GetCredentialGroupResponse:
    """
    Get a credential group by name.

    Returns a single credential group.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/credential/v20261020alpha1/groups/{path_segment(name)}",
        path_template="/credential/v20261020alpha1/groups/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetCredentialGroup",
        error_cls=GetGroupError,
    )

    return parse_response_model(
        GetCredentialGroupResponse,
        body,
        operation_name="GetCredentialGroup",
        method="get",
        path="/credential/v20261020alpha1/groups/{name}",
    )


def UpdateCredentialGroup(
    api_config_override: Optional[APIConfig] = None,
    *,
    name: str,
    data: CredentialServiceUpdateCredentialGroupBody,
) -> UpdateCredentialGroupResponse:
    """
    Update a credential group.

    Tokens with a value create a new credential version; tokens without one only update metadata.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/credential/v20261020alpha1/groups/{path_segment(name)}",
        path_template="/credential/v20261020alpha1/groups/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateCredentialGroup",
        error_cls=UpdateGroupError,
    )

    return parse_response_model(
        UpdateCredentialGroupResponse,
        body,
        operation_name="UpdateCredentialGroup",
        method="put",
        path="/credential/v20261020alpha1/groups/{name}",
    )


def DeleteCredentialGroup(
    api_config_override: Optional[APIConfig] = None, *, name: str
) -> DeleteCredentialGroupResponse:
    """
    Delete a credential group.

    Deletes every version of every credential in the group. Fails if any credential has consumers.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/credential/v20261020alpha1/groups/{path_segment(name)}",
        path_template="/credential/v20261020alpha1/groups/{name}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteCredentialGroup",
        error_cls=DeleteGroupError,
    )

    return parse_response_model(
        DeleteCredentialGroupResponse,
        body,
        operation_name="DeleteCredentialGroup",
        method="delete",
        path="/credential/v20261020alpha1/groups/{name}",
    )


def ListCredentialOverviews(
    api_config_override: Optional[APIConfig] = None,
) -> ListCredentialOverviewsResponse:
    """
    List credential group names and types.

    Returns a lightweight name and type listing of every credential group, for lookups.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/credential/v20261020alpha1/overviews",
        path_template="/credential/v20261020alpha1/overviews",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListCredentialOverviews",
        error_cls=ListOverviewsError,
    )

    return parse_response_model(
        ListCredentialOverviewsResponse,
        body,
        operation_name="ListCredentialOverviews",
        method="get",
        path="/credential/v20261020alpha1/overviews",
    )
