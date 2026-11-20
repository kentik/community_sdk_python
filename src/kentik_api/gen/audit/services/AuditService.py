# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import GetEventByCtimeError, GetEventError, ListEventsError
from ..models import (  # noqa: F401
    AuditEvent,
    GenericEvent,
    GetAuditEventResponse,
    ListAuditEventsResponse,
    protobufAny,
    rpcStatus,
)


def ListAuditEvents(
    api_config_override: Optional[APIConfig] = None,
    *,
    startTime: Optional[str] = None,
    endTime: Optional[str] = None,
    offset: Optional[str] = None,
    limit: Optional[str] = None,
) -> ListAuditEventsResponse:
    """
    List Audit Events.

    Returns a list of audit events.
    """
    query_params: Dict[str, Any] = {
        "startTime": startTime,
        "endTime": endTime,
        "offset": offset,
        "limit": limit,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/audit/v202601/events",
        path_template="/audit/v202601/events",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAuditEvents",
        error_cls=ListEventsError,
    )

    return parse_response_model(
        ListAuditEventsResponse,
        body,
        operation_name="ListAuditEvents",
        method="get",
        path="/audit/v202601/events",
    )


def GetAuditEvent(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    ctime: Optional[str] = None,
) -> GetAuditEventResponse:
    """
    Get an Audit Event

    Return a specific audit event.
    """
    query_params: Dict[str, Any] = {"ctime": ctime}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/audit/v202601/events/{path_segment(id)}",
        path_template="/audit/v202601/events/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAuditEvent",
        error_cls=GetEventError,
    )

    return parse_response_model(
        GetAuditEventResponse,
        body,
        operation_name="GetAuditEvent",
        method="get",
        path="/audit/v202601/events/{id}",
    )


def GetAuditEvent_2(
    api_config_override: Optional[APIConfig] = None, *, id: str, ctime: str
) -> GetAuditEventResponse:
    """
    Get an Audit Event

    Return a specific audit event.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/audit/v202601/events/{path_segment(id)}/{path_segment(ctime)}",
        path_template="/audit/v202601/events/{id}/{ctime}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAuditEvent",
        error_cls=GetEventByCtimeError,
    )

    return parse_response_model(
        GetAuditEventResponse,
        body,
        operation_name="GetAuditEvent",
        method="get",
        path="/audit/v202601/events/{id}/{ctime}",
    )
