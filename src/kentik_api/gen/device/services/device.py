from typing import Optional, Union, cast

import kentik_api.gen.device.services.DeviceService as RestDeviceModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.device import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class DeviceServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.device.pb.device_pb2 as _pb2_1_mod
                import kentik_api.gen.device.pb.device_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.DeviceServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        querynoCustomColumns: Optional[bool] = None,
        view: Optional[str] = None,
    ) -> rest_models.ListDevicesResponse:
        """
        List all devices.

        Returns list of configured devices. Use the 'view' parameter to control response detail: FULL (default), BASIC (id, name, status), or ID_ONLY (id only). See [About Devices](https://kb.kentik.com/v4/Cb01.htm).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListDevicesRequest,
                None,
                {"query.noCustomColumns": querynoCustomColumns, "view": view},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListDevices,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListDevicesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListDevices,
                operation_name="ListDevices",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.ListDevices(
                api_config_override=api_config_override or rest_transport.api_config,
                querynoCustomColumns=querynoCustomColumns,
                view=view,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateDeviceRequest,
    ) -> rest_models.CreateDeviceResponse:
        """
        Configure a new device.

        Create configuration for a new device. Returns the newly created configuration (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateDeviceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateDevice,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateDeviceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateDevice,
                operation_name="CreateDevice",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.CreateDevice(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_bulk(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateDevicesRequest,
    ) -> rest_models.CreateDevicesResponse:
        """
        Configure multiple devices (max 100).

        Create configuration for multiple devices. Returns the newly created configurations (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateDevicesRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateDevices,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.CreateBulkError,
            )
            return parse_grpc_response(
                rest_models.CreateDevicesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateDevices,
                operation_name="CreateDevices",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.CreateDevices(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_bulk(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.DeleteDevicesRequest,
    ) -> rest_models.DeleteDevicesResponse:
        """
        Delete configuration of multiple devices.

        Deletes configuration of multiple devices with specific IDs (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteDevicesRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteDevices,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.DeleteBulkError,
            )
            return parse_grpc_response(
                rest_models.DeleteDevicesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteDevices,
                operation_name="DeleteDevices",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.DeleteDevices(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_bulk(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.UpdateDevicesRequest,
    ) -> rest_models.UpdateDevicesResponse:
        """
        Updates configuration of multiple devices (max 100).

        Replaces configuration of multiple devices with attributes in the request. Returns the updated configurations (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateDevicesRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateDevices,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.UpdateBulkError,
            )
            return parse_grpc_response(
                rest_models.UpdateDevicesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateDevices,
                operation_name="UpdateDevices",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.UpdateDevices(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_by_name(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        deviceName: str,
        querynoCustomColumns: Optional[bool] = None,
    ) -> rest_models.GetDeviceByNameResponse:
        """
        Retrieve configuration of a device by name.

        Returns configuration of a device specified by name (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetDeviceByNameRequest,
                None,
                {
                    "device_name": deviceName,
                    "query.noCustomColumns": querynoCustomColumns,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetDeviceByName,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.GetByNameError,
            )
            return parse_grpc_response(
                rest_models.GetDeviceByNameResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetDeviceByName,
                operation_name="GetDeviceByName",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.GetDeviceByName(
                api_config_override=api_config_override or rest_transport.api_config,
                deviceName=deviceName,
                querynoCustomColumns=querynoCustomColumns,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        deviceid: str,
        querynoCustomColumns: Optional[bool] = None,
    ) -> rest_models.GetDeviceResponse:
        """
        Retrieve configuration of a device.

        Returns configuration of a device specified by ID (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetDeviceRequest,
                None,
                {"id": deviceid, "query.noCustomColumns": querynoCustomColumns},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetDevice,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetDeviceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetDevice,
                operation_name="GetDevice",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.GetDevice(
                api_config_override=api_config_override or rest_transport.api_config,
                deviceid=deviceid,
                querynoCustomColumns=querynoCustomColumns,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        deviceid: str,
        data: rest_models.DeviceServiceUpdateDeviceBody,
    ) -> rest_models.UpdateDeviceResponse:
        """
        Updates configuration of a device.

        Replaces configuration of a device with attributes in the request. Returns the updated configuration (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateDeviceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"device.id": deviceid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateDevice,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateDeviceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateDevice,
                operation_name="UpdateDevice",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.UpdateDevice(
                api_config_override=api_config_override or rest_transport.api_config,
                deviceid=deviceid,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, deviceid: str
    ) -> rest_models.DeleteDeviceResponse:
        """
        Delete configuration of a device.

        Deletes configuration of a device with specific ID (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteDeviceRequest, None, {"id": deviceid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteDevice,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteDeviceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteDevice,
                operation_name="DeleteDevice",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.DeleteDevice(
                api_config_override=api_config_override or rest_transport.api_config,
                deviceid=deviceid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_labels(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.DeviceServiceUpdateDeviceLabelsBody,
    ) -> rest_models.UpdateDeviceLabelsResponse:
        """
        Updates labels of a device.

        Removes all existing labels from the device and applies the device labels (see [About Device Labels](https://kb.kentik.com/v4/Cb16.htm)) specified by id. Returns the updated configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for device service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateDeviceLabelsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateDeviceLabels,
                _req,
                api_config=api_config_override,
                error_cls=RestDeviceModule1.UpdateLabelsError,
            )
            return parse_grpc_response(
                rest_models.UpdateDeviceLabelsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateDeviceLabels,
                operation_name="UpdateDeviceLabels",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDeviceModule1.UpdateDeviceLabels(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
