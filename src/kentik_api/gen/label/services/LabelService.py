# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import CreateError, DeleteError, ListError, UpdateError
from ..models import (  # noqa: F401
    CreateLabelRequest,
    CreateLabelResponse,
    DeleteLabelResponse,
    Label,
    LabelServiceUpdateLabelBody,
    ListLabelsResponse,
    UpdateLabelResponse,
    protobufAny,
    rpcStatus,
)


def ListLabels(api_config_override: Optional[APIConfig] = None) -> ListLabelsResponse:
    """
    List all configured labels

    Returns list of all labels configured in the account.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/label/v202210/labels",
        path_template="/label/v202210/labels",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListLabels",
        error_cls=ListError,
    )

    return parse_response_model(
        ListLabelsResponse,
        body,
        operation_name="ListLabels",
        method="get",
        path="/label/v202210/labels",
    )


def CreateLabel(
    api_config_override: Optional[APIConfig] = None, *, data: CreateLabelRequest
) -> CreateLabelResponse:
    """
    Create a new label.

    Creates a new label based on data in the request.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/label/v202210/labels",
        path_template="/label/v202210/labels",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateLabel",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateLabelResponse,
        body,
        operation_name="CreateLabel",
        method="post",
        path="/label/v202210/labels",
    )


def UpdateLabel(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: LabelServiceUpdateLabelBody,
) -> UpdateLabelResponse:
    """
    Update an existing label.

    Updates configuration of a label.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/label/v202210/labels/{path_segment(id)}",
        path_template="/label/v202210/labels/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateLabel",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateLabelResponse,
        body,
        operation_name="UpdateLabel",
        method="post",
        path="/label/v202210/labels/{id}",
    )


def DeleteLabel(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteLabelResponse:
    """
    Delete a label.

    Deletes label with specified with id.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/label/v202210/labels/{path_segment(id)}",
        path_template="/label/v202210/labels/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteLabel",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteLabelResponse,
        body,
        operation_name="DeleteLabel",
        method="delete",
        path="/label/v202210/labels/{id}",
    )
