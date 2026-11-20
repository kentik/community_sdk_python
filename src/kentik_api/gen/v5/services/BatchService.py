# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import BatchPopulatorsError, BatchStatusError, BatchTagsError
from ..models import (  # noqa: F401
    Aggregate,
    BatchCriterion,
    BatchDelete,
    BatchDeleteCounts,
    BatchPart,
    BatchReplaceAll,
    BatchResponse,
    BatchStatus,
    BatchStatusCustomDimension,
    BatchStatusUser,
    BatchUpsert,
    BatchUpsertCounts,
    ChartRequest,
    ChartResponse,
    Filter,
    FilterGroup,
    Query,
    QueryFilters,
    QueryItem,
    QueryRequest,
    ResultBucket,
    SavedFilterRef,
    TopXDataResponse,
    V5Error,
)


def BatchService_Tags(
    api_config_override: Optional[APIConfig] = None, *, data: BatchPart
) -> BatchResponse:
    """
    Batch flow tags

    Creates, updates, or deletes flow tags in bulk. Sends one part of a batch. The API applies upserts as parts arrive and deletes only after the part with complete=true. Each part is at most 4 MB. Every part after the first carries the guid from the first response. kentik_api.v5_tools.split_batch() and send_batch() do this. The SDK never resends a part.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/batch/tags",
        path_template="/batch/tags",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=202,
        operation_name="BatchService_Tags",
        error_cls=BatchTagsError,
    )

    return parse_response_model(
        BatchResponse,
        body,
        operation_name="BatchService_Tags",
        method="post",
        path="/batch/tags",
    )


def BatchService_Populators(
    api_config_override: Optional[APIConfig] = None,
    *,
    dimensionName: str,
    data: BatchPart,
) -> BatchResponse:
    """
    Batch populators

    Creates, updates, or deletes the populators of one custom dimension in bulk. Sends one part of a batch. The API applies upserts as parts arrive and deletes only after the part with complete=true. Each part is at most 4 MB. Every part after the first carries the guid from the first response. kentik_api.v5_tools.split_batch() and send_batch() do this. The SDK never resends a part.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/batch/customdimensions/{path_segment(dimensionName)}/populators",
        path_template="/batch/customdimensions/{dimensionName}/populators",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=202,
        operation_name="BatchService_Populators",
        error_cls=BatchPopulatorsError,
    )

    return parse_response_model(
        BatchResponse,
        body,
        operation_name="BatchService_Populators",
        method="post",
        path="/batch/customdimensions/{dimensionName}/populators",
    )


def BatchService_Status(
    api_config_override: Optional[APIConfig] = None, *, guid: str
) -> BatchStatus:
    """
    Batch status

    Returns the progress of a batch. kentik_api.v5_tools.wait_for_batch() polls it until is_complete is true.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/batch/{path_segment(guid)}/status",
        path_template="/batch/{guid}/status",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="BatchService_Status",
        error_cls=BatchStatusError,
    )

    return parse_response_model(
        BatchStatus,
        body,
        operation_name="BatchService_Status",
        method="get",
        path="/batch/{guid}/status",
    )
