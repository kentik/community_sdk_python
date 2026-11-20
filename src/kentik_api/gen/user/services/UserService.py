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
    CreateError,
    DeleteError,
    GetError,
    ListError,
    ResetActiveSessionsError,
    ResetApiTokenError,
    UpdateError,
)
from ..models import (  # noqa: F401
    CreateUserRequest,
    CreateUserResponse,
    DeleteUserResponse,
    GetUserResponse,
    LandingType,
    ListUsersResponse,
    PermissionEntry,
    ResetActiveSessionsResponse,
    ResetApiTokenResponse,
    Role,
    UpdateUserResponse,
    User,
    UserServiceUpdateUserBody,
    protobufAny,
    rpcStatus,
)


def ListUsers(api_config_override: Optional[APIConfig] = None) -> ListUsersResponse:
    """
    List all users.

    Returns a list of all user accounts in the company.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/user/v202211/users",
        path_template="/user/v202211/users",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListUsers",
        error_cls=ListError,
    )

    return parse_response_model(
        ListUsersResponse,
        body,
        operation_name="ListUsers",
        method="get",
        path="/user/v202211/users",
    )


def CreateUser(
    api_config_override: Optional[APIConfig] = None, *, data: CreateUserRequest
) -> CreateUserResponse:
    """
    Create new user account.

    Creates new user account based on attributes in the request. Returns attributes of the newly created account.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/user/v202211/users",
        path_template="/user/v202211/users",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateUser",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateUserResponse,
        body,
        operation_name="CreateUser",
        method="post",
        path="/user/v202211/users",
    )


def GetUser(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetUserResponse:
    """
    Get attributes of a user account.

    Returns attributes of a user account specified by ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/user/v202211/users/{path_segment(id)}",
        path_template="/user/v202211/users/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetUser",
        error_cls=GetError,
    )

    return parse_response_model(
        GetUserResponse,
        body,
        operation_name="GetUser",
        method="get",
        path="/user/v202211/users/{id}",
    )


def UpdateUser(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: UserServiceUpdateUserBody,
) -> UpdateUserResponse:
    """
    Update attributes of a user account.

    Replaces all attributes of a user account specified by ID with attributes in the request. Returns updated attributes.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/user/v202211/users/{path_segment(id)}",
        path_template="/user/v202211/users/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateUser",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateUserResponse,
        body,
        operation_name="UpdateUser",
        method="put",
        path="/user/v202211/users/{id}",
    )


def DeleteUser(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteUserResponse:
    """
    Delete a user account.

    Deletes user account specified by ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/user/v202211/users/{path_segment(id)}",
        path_template="/user/v202211/users/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteUser",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteUserResponse,
        body,
        operation_name="DeleteUser",
        method="delete",
        path="/user/v202211/users/{id}",
    )


def ResetActiveSessions(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> ResetActiveSessionsResponse:
    """
    Resets active sessions for a user.

    Resets active sessions for a user specified by ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/user/v202211/users/{path_segment(id)}/reset_active_sessions",
        path_template="/user/v202211/users/{id}/reset_active_sessions",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ResetActiveSessions",
        error_cls=ResetActiveSessionsError,
    )

    return parse_response_model(
        ResetActiveSessionsResponse,
        body,
        operation_name="ResetActiveSessions",
        method="put",
        path="/user/v202211/users/{id}/reset_active_sessions",
    )


def ResetApiToken(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> ResetApiTokenResponse:
    """
    Reset API token for a user.

    Resets API token for a user specified by ID.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/user/v202211/users/{path_segment(id)}/reset_api_token",
        path_template="/user/v202211/users/{id}/reset_api_token",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ResetApiToken",
        error_cls=ResetApiTokenError,
    )

    return parse_response_model(
        ResetApiTokenResponse,
        body,
        operation_name="ResetApiToken",
        method="put",
        path="/user/v202211/users/{id}/reset_api_token",
    )
