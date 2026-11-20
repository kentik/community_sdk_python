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
    CreateBulkError,
    CreateError,
    DeleteBulkError,
    DeleteError,
    GetByNameError,
    GetError,
    ListError,
    UpdateBulkError,
    UpdateError,
    UpdateLabelsError,
)
from ..models import (  # noqa: F401
    CreateDeviceRequest,
    CreateDeviceResponse,
    CreateDevicesRequest,
    CreateDevicesResponse,
    CustomColumnData,
    DeleteDeviceResponse,
    DeleteDevicesRequest,
    DeleteDevicesResponse,
    DeviceConcise,
    DeviceDetailed,
    DeviceNmsConfig,
    DeviceNmsSnmpConfig,
    DeviceNmsStConfig,
    DeviceQuery,
    DeviceServiceUpdateDeviceBody,
    DeviceServiceUpdateDeviceLabelsBody,
    DeviceSnmpV3Conf,
    DeviceView,
    GetDeviceByNameResponse,
    GetDeviceResponse,
    GnmiV1Conf,
    Interface,
    Label,
    LabelConcise,
    ListDevicesResponse,
    Plan,
    Site,
    UpdateDeviceLabelsResponse,
    UpdateDeviceResponse,
    UpdateDevicesRequest,
    UpdateDevicesResponse,
    protobufAny,
    rpcStatus,
)


def ListDevices(
    api_config_override: Optional[APIConfig] = None,
    *,
    querynoCustomColumns: Optional[bool] = None,
    view: Optional[str] = None,
) -> ListDevicesResponse:
    """
    List all devices.

    Returns list of configured devices. Use the 'view' parameter to control response detail: FULL (default), BASIC (id, name, status), or ID_ONLY (id only). See [About Devices](https://kb.kentik.com/v4/Cb01.htm).
    """
    query_params: Dict[str, Any] = {
        "query.noCustomColumns": querynoCustomColumns,
        "view": view,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/device/v202504beta2/device",
        path_template="/device/v202504beta2/device",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListDevices",
        error_cls=ListError,
    )

    return parse_response_model(
        ListDevicesResponse,
        body,
        operation_name="ListDevices",
        method="get",
        path="/device/v202504beta2/device",
    )


def CreateDevice(
    api_config_override: Optional[APIConfig] = None, *, data: CreateDeviceRequest
) -> CreateDeviceResponse:
    """
    Configure a new device.

    Create configuration for a new device. Returns the newly created configuration (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/device/v202504beta2/device",
        path_template="/device/v202504beta2/device",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateDevice",
        error_cls=CreateError,
    )

    return parse_response_model(
        CreateDeviceResponse,
        body,
        operation_name="CreateDevice",
        method="post",
        path="/device/v202504beta2/device",
    )


def CreateDevices(
    api_config_override: Optional[APIConfig] = None, *, data: CreateDevicesRequest
) -> CreateDevicesResponse:
    """
    Configure multiple devices (max 100).

    Create configuration for multiple devices. Returns the newly created configurations (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/device/v202504beta2/device/batch_create",
        path_template="/device/v202504beta2/device/batch_create",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateDevices",
        error_cls=CreateBulkError,
    )

    return parse_response_model(
        CreateDevicesResponse,
        body,
        operation_name="CreateDevices",
        method="post",
        path="/device/v202504beta2/device/batch_create",
    )


def DeleteDevices(
    api_config_override: Optional[APIConfig] = None, *, data: DeleteDevicesRequest
) -> DeleteDevicesResponse:
    """
    Delete configuration of multiple devices.

    Deletes configuration of multiple devices with specific IDs (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/device/v202504beta2/device/batch_delete",
        path_template="/device/v202504beta2/device/batch_delete",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteDevices",
        error_cls=DeleteBulkError,
    )

    return parse_response_model(
        DeleteDevicesResponse,
        body,
        operation_name="DeleteDevices",
        method="post",
        path="/device/v202504beta2/device/batch_delete",
    )


def UpdateDevices(
    api_config_override: Optional[APIConfig] = None, *, data: UpdateDevicesRequest
) -> UpdateDevicesResponse:
    """
    Updates configuration of multiple devices (max 100).

    Replaces configuration of multiple devices with attributes in the request. Returns the updated configurations (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path="/device/v202504beta2/device/batch_update",
        path_template="/device/v202504beta2/device/batch_update",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateDevices",
        error_cls=UpdateBulkError,
    )

    return parse_response_model(
        UpdateDevicesResponse,
        body,
        operation_name="UpdateDevices",
        method="put",
        path="/device/v202504beta2/device/batch_update",
    )


def GetDeviceByName(
    api_config_override: Optional[APIConfig] = None,
    *,
    deviceName: str,
    querynoCustomColumns: Optional[bool] = None,
) -> GetDeviceByNameResponse:
    """
    Retrieve configuration of a device by name.

    Returns configuration of a device specified by name (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {"query.noCustomColumns": querynoCustomColumns}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/device/v202504beta2/device/name/{path_segment(deviceName)}",
        path_template="/device/v202504beta2/device/name/{deviceName}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetDeviceByName",
        error_cls=GetByNameError,
    )

    return parse_response_model(
        GetDeviceByNameResponse,
        body,
        operation_name="GetDeviceByName",
        method="get",
        path="/device/v202504beta2/device/name/{deviceName}",
    )


def GetDevice(
    api_config_override: Optional[APIConfig] = None,
    *,
    deviceid: str,
    querynoCustomColumns: Optional[bool] = None,
) -> GetDeviceResponse:
    """
    Retrieve configuration of a device.

    Returns configuration of a device specified by ID (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {"query.noCustomColumns": querynoCustomColumns}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/device/v202504beta2/device/{path_segment(deviceid)}",
        path_template="/device/v202504beta2/device/{device.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetDevice",
        error_cls=GetError,
    )

    return parse_response_model(
        GetDeviceResponse,
        body,
        operation_name="GetDevice",
        method="get",
        path="/device/v202504beta2/device/{device.id}",
    )


def UpdateDevice(
    api_config_override: Optional[APIConfig] = None,
    *,
    deviceid: str,
    data: DeviceServiceUpdateDeviceBody,
) -> UpdateDeviceResponse:
    """
    Updates configuration of a device.

    Replaces configuration of a device with attributes in the request. Returns the updated configuration (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/device/v202504beta2/device/{path_segment(deviceid)}",
        path_template="/device/v202504beta2/device/{device.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateDevice",
        error_cls=UpdateError,
    )

    return parse_response_model(
        UpdateDeviceResponse,
        body,
        operation_name="UpdateDevice",
        method="put",
        path="/device/v202504beta2/device/{device.id}",
    )


def DeleteDevice(
    api_config_override: Optional[APIConfig] = None, *, deviceid: str
) -> DeleteDeviceResponse:
    """
    Delete configuration of a device.

    Deletes configuration of a device with specific ID (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/device/v202504beta2/device/{path_segment(deviceid)}",
        path_template="/device/v202504beta2/device/{device.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteDevice",
        error_cls=DeleteError,
    )

    return parse_response_model(
        DeleteDeviceResponse,
        body,
        operation_name="DeleteDevice",
        method="delete",
        path="/device/v202504beta2/device/{device.id}",
    )


def UpdateDeviceLabels(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: DeviceServiceUpdateDeviceLabelsBody,
) -> UpdateDeviceLabelsResponse:
    """
    Updates labels of a device.

    Removes all existing labels from the device and applies the device labels (see [About Device Labels](https://kb.kentik.com/v4/Cb16.htm)) specified by id. Returns the updated configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/device/v202504beta2/device/{path_segment(id)}/labels",
        path_template="/device/v202504beta2/device/{id}/labels",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateDeviceLabels",
        error_cls=UpdateLabelsError,
    )

    return parse_response_model(
        UpdateDeviceLabelsResponse,
        body,
        operation_name="UpdateDeviceLabels",
        method="put",
        path="/device/v202504beta2/device/{id}/labels",
    )
