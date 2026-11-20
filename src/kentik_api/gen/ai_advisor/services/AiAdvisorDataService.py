# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import CreateChatSessionError, GetChatSessionError, UpdateChatSessionError
from ..models import (  # noqa: F401
    ChatMessage,
    CreateChatSessionRequest,
    CreateChatSessionResponse,
    GetChatSessionResponse,
    SessionStatus,
    UpdateChatSessionRequest,
    UpdateChatSessionResponse,
    protobufAny,
    rpcStatus,
)


def CreateChatSession(
    api_config_override: Optional[APIConfig] = None, *, data: CreateChatSessionRequest
) -> CreateChatSessionResponse:
    """
    Create AI Advisor Chat Session

    Create a new AI Advisor Chat session with a prompt
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/ai_advisor/v202511/chat",
        path_template="/ai_advisor/v202511/chat",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateChatSession",
        error_cls=CreateChatSessionError,
    )

    return parse_response_model(
        CreateChatSessionResponse,
        body,
        operation_name="CreateChatSession",
        method="post",
        path="/ai_advisor/v202511/chat",
    )


def UpdateChatSession(
    api_config_override: Optional[APIConfig] = None, *, data: UpdateChatSessionRequest
) -> UpdateChatSessionResponse:
    """
    Update AI Advisor Chat Session

    Update AI Advisor Chat session with a prompt
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path="/ai_advisor/v202511/chat",
        path_template="/ai_advisor/v202511/chat",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateChatSession",
        error_cls=UpdateChatSessionError,
    )

    return parse_response_model(
        UpdateChatSessionResponse,
        body,
        operation_name="UpdateChatSession",
        method="put",
        path="/ai_advisor/v202511/chat",
    )


def GetChatSession(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetChatSessionResponse:
    """
    Get AI Advisor Chat Session

    Retrieve the status and results of an AI Advisor chat session
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/ai_advisor/v202511/chat/{path_segment(id)}",
        path_template="/ai_advisor/v202511/chat/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetChatSession",
        error_cls=GetChatSessionError,
    )

    return parse_response_model(
        GetChatSessionResponse,
        body,
        operation_name="GetChatSession",
        method="get",
        path="/ai_advisor/v202511/chat/{id}",
    )
