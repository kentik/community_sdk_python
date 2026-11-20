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
    CreateTagKeyError,
    DeleteTagKeyError,
    DeleteTagValuesError,
    GetTagKeyError,
    GetTagValuesError,
    ListTagKeysError,
    ListTagValuesError,
    SetTagValuesError,
    UpdateTagKeyError,
)
from ..models import (  # noqa: F401
    AssetTagsServiceUpdateTagKeyBody,
    AssetType,
    CreateTagKeyRequest,
    CreateTagKeyResponse,
    DeleteTagKeyResponse,
    DeleteTagValuesRequest,
    DeleteTagValuesResponse,
    GetTagKeyResponse,
    GetTagValuesResponse,
    ListTagKeysResponse,
    ListTagValuesResponse,
    SetTagValuesRequest,
    SetTagValuesResponse,
    TagKey,
    TagValue,
    UpdateTagKeyResponse,
    protobufAny,
    rpcStatus,
)


def GetTagValues(
    api_config_override: Optional[APIConfig] = None, *, assetType: str, assetId: str
) -> GetTagValuesResponse:
    """
    Gets tag values by asset id and type.

    Returns a list of tag values.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/asset_tags/v20260515beta1/assets/{path_segment(assetType)}/{path_segment(assetId)}/values",
        path_template="/asset_tags/v20260515beta1/assets/{assetType}/{assetId}/values",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetTagValues",
        error_cls=GetTagValuesError,
    )

    return parse_response_model(
        GetTagValuesResponse,
        body,
        operation_name="GetTagValues",
        method="get",
        path="/asset_tags/v20260515beta1/assets/{assetType}/{assetId}/values",
    )


def ListTagKeys(api_config_override: Optional[APIConfig] = None) -> ListTagKeysResponse:
    """
    Lists all tag keys.

    Returns a list of tag keys.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/asset_tags/v20260515beta1/keys",
        path_template="/asset_tags/v20260515beta1/keys",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListTagKeys",
        error_cls=ListTagKeysError,
    )

    return parse_response_model(
        ListTagKeysResponse,
        body,
        operation_name="ListTagKeys",
        method="get",
        path="/asset_tags/v20260515beta1/keys",
    )


def CreateTagKey(
    api_config_override: Optional[APIConfig] = None, *, data: CreateTagKeyRequest
) -> CreateTagKeyResponse:
    """
    Creates a new tag key.

    Returns the created tag key.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/asset_tags/v20260515beta1/keys",
        path_template="/asset_tags/v20260515beta1/keys",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateTagKey",
        error_cls=CreateTagKeyError,
    )

    return parse_response_model(
        CreateTagKeyResponse,
        body,
        operation_name="CreateTagKey",
        method="post",
        path="/asset_tags/v20260515beta1/keys",
    )


def GetTagKey(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetTagKeyResponse:
    """
    Get a single tag key by id.

    Returns a single tag key.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/asset_tags/v20260515beta1/keys/{path_segment(id)}",
        path_template="/asset_tags/v20260515beta1/keys/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetTagKey",
        error_cls=GetTagKeyError,
    )

    return parse_response_model(
        GetTagKeyResponse,
        body,
        operation_name="GetTagKey",
        method="get",
        path="/asset_tags/v20260515beta1/keys/{id}",
    )


def UpdateTagKey(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: AssetTagsServiceUpdateTagKeyBody,
) -> UpdateTagKeyResponse:
    """
    Updates the display name of a tag key.

    Returns the updated tag key.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/asset_tags/v20260515beta1/keys/{path_segment(id)}",
        path_template="/asset_tags/v20260515beta1/keys/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateTagKey",
        error_cls=UpdateTagKeyError,
    )

    return parse_response_model(
        UpdateTagKeyResponse,
        body,
        operation_name="UpdateTagKey",
        method="put",
        path="/asset_tags/v20260515beta1/keys/{id}",
    )


def DeleteTagKey(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteTagKeyResponse:
    """
    Deletes a tag key by id.

    Returns an empty response
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/asset_tags/v20260515beta1/keys/{path_segment(id)}",
        path_template="/asset_tags/v20260515beta1/keys/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteTagKey",
        error_cls=DeleteTagKeyError,
    )

    return parse_response_model(
        DeleteTagKeyResponse,
        body,
        operation_name="DeleteTagKey",
        method="delete",
        path="/asset_tags/v20260515beta1/keys/{id}",
    )


def ListTagValues(
    api_config_override: Optional[APIConfig] = None, *, tagId: str, assetType: str
) -> ListTagValuesResponse:
    """
    Lists all tag values by id, optionally filtered by asset type.

    Returns a list of tag values.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/asset_tags/v20260515beta1/keys/{path_segment(tagId)}/{path_segment(assetType)}/values",
        path_template="/asset_tags/v20260515beta1/keys/{tagId}/{assetType}/values",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListTagValues",
        error_cls=ListTagValuesError,
    )

    return parse_response_model(
        ListTagValuesResponse,
        body,
        operation_name="ListTagValues",
        method="get",
        path="/asset_tags/v20260515beta1/keys/{tagId}/{assetType}/values",
    )


def SetTagValues(
    api_config_override: Optional[APIConfig] = None, *, data: SetTagValuesRequest
) -> SetTagValuesResponse:
    """
    Bulk upserts a tag value for a list of asset ids of a given type.

    Returns a list of tag values.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path="/asset_tags/v20260515beta1/values",
        path_template="/asset_tags/v20260515beta1/values",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="SetTagValues",
        error_cls=SetTagValuesError,
    )

    return parse_response_model(
        SetTagValuesResponse,
        body,
        operation_name="SetTagValues",
        method="put",
        path="/asset_tags/v20260515beta1/values",
    )


def DeleteTagValues(
    api_config_override: Optional[APIConfig] = None, *, data: DeleteTagValuesRequest
) -> DeleteTagValuesResponse:
    """
    Bulk deletes a tag values for a list of asset ids of a given type.

    Returns an empty response.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/asset_tags/v20260515beta1/values/delete",
        path_template="/asset_tags/v20260515beta1/values/delete",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteTagValues",
        error_cls=DeleteTagValuesError,
    )

    return parse_response_model(
        DeleteTagValuesResponse,
        body,
        operation_name="DeleteTagValues",
        method="post",
        path="/asset_tags/v20260515beta1/values/delete",
    )
