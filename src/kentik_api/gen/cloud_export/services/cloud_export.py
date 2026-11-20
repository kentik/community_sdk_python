from typing import Optional, Union, cast

import kentik_api.gen.cloud_export.services.CloudExportAdminService as RestCloudExportModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.cloud_export import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CloudExportServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.cloud_export.pb.cloud_export_pb2 as _pb2_1_mod
                import kentik_api.gen.cloud_export.pb.cloud_export_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CloudExportAdminServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCloudExportsResponse:
        """
        List cloud exports.

        Returns a list of all cloud exports in the account.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cloud_export service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCloudExportsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCloudExports,
                _req,
                api_config=api_config_override,
                error_cls=RestCloudExportModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListCloudExportsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCloudExports,
                operation_name="ListCloudExports",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCloudExportModule1.ListCloudExports(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateCloudExportRequest,
    ) -> rest_models.CreateCloudExportResponse:
        """
        Create Cloud Export.

        Create new cloud export based on configuration in the request.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cloud_export service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateCloudExportRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateCloudExport,
                _req,
                api_config=api_config_override,
                error_cls=RestCloudExportModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateCloudExportResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateCloudExport,
                operation_name="CreateCloudExport",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCloudExportModule1.CreateCloudExport(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, exportid: str
    ) -> rest_models.GetCloudExportResponse:
        """
        Get cloud export configuration and status.

        Returns configuration and status of cloud export with specified ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cloud_export service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCloudExportRequest, None, {"id": exportid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCloudExport,
                _req,
                api_config=api_config_override,
                error_cls=RestCloudExportModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetCloudExportResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCloudExport,
                operation_name="GetCloudExport",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCloudExportModule1.GetCloudExport(
                api_config_override=api_config_override or rest_transport.api_config,
                exportid=exportid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        exportid: str,
        data: rest_models.CloudExportAdminServiceUpdateCloudExportBody,
    ) -> rest_models.UpdateCloudExportResponse:
        """
        Update configuration of cloud export.

        Replace complete configuration of a cloud export with data in the request.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cloud_export service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateCloudExportRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"export.id": exportid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateCloudExport,
                _req,
                api_config=api_config_override,
                error_cls=RestCloudExportModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateCloudExportResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateCloudExport,
                operation_name="UpdateCloudExport",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCloudExportModule1.UpdateCloudExport(
                api_config_override=api_config_override or rest_transport.api_config,
                exportid=exportid,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, exportid: str
    ) -> rest_models.DeleteCloudExportResponse:
        """
        Delete a cloud export.

        Delete cloud export with specified ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cloud_export service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteCloudExportRequest, None, {"id": exportid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteCloudExport,
                _req,
                api_config=api_config_override,
                error_cls=RestCloudExportModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteCloudExportResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteCloudExport,
                operation_name="DeleteCloudExport",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCloudExportModule1.DeleteCloudExport(
                api_config_override=api_config_override or rest_transport.api_config,
                exportid=exportid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
