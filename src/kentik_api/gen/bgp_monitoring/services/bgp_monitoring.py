from typing import Optional, Union, cast

import kentik_api.gen.bgp_monitoring.services.BgpMonitoringAdminService as RestBgpMonitoringModule1
import kentik_api.gen.bgp_monitoring.services.BgpMonitoringDataService as RestBgpMonitoringModule2
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.bgp_monitoring import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class BgpMonitoringServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.bgp_monitoring.pb.bgp_monitoring_pb2 as _pb2_1_mod
                import kentik_api.gen.bgp_monitoring.pb.bgp_monitoring_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.BgpMonitoringAdminServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.bgp_monitoring.pb.bgp_monitoring_pb2 as _pb2_2_mod
                import kentik_api.gen.bgp_monitoring.pb.bgp_monitoring_pb2_grpc as _pb2_grpc_2_mod

                self._grpc_pb2_2 = _pb2_2_mod
                self._grpc_stub_2 = _pb2_grpc_2_mod.BgpMonitoringDataServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_2 = None
                self._grpc_stub_2 = None
                self._grpc_import_error_2 = exc

    def list_monitors(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListMonitorsResponse:
        """
        List BGP Monitors.

        Returns list of all BGP monitors present in the account.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListMonitorsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListMonitors,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.ListMonitorsError,
            )
            return parse_grpc_response(
                rest_models.ListMonitorsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListMonitors,
                operation_name="ListMonitors",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.ListMonitors(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_monitor(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateMonitorRequest,
    ) -> rest_models.CreateMonitorResponse:
        """
        Create new BGP Monitor instance.

        Creates new BGP Monitor and if successful returns its configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateMonitorRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateMonitor,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.CreateMonitorError,
            )
            return parse_grpc_response(
                rest_models.CreateMonitorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateMonitor,
                operation_name="CreateMonitor",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.CreateMonitor(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_monitor(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetMonitorResponse:
        """
        Get BGP Monitor configuration.

        Returns configuration of existing BGP monitor with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetMonitorRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetMonitor,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.GetMonitorError,
            )
            return parse_grpc_response(
                rest_models.GetMonitorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetMonitor,
                operation_name="GetMonitor",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.GetMonitor(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_monitor(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.BgpMonitoringAdminServiceUpdateMonitorBody,
    ) -> rest_models.UpdateMonitorResponse:
        """
        Update configuration of a BGP monitor.

        Updates configuration of BGP monitor with specific ID and returns updated  configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateMonitorRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"monitor.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateMonitor,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.UpdateMonitorError,
            )
            return parse_grpc_response(
                rest_models.UpdateMonitorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateMonitor,
                operation_name="UpdateMonitor",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.UpdateMonitor(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_monitor(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteMonitorResponse:
        """
        Delete existing BGP Monitor.

        Delete BGP monitor with with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteMonitorRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteMonitor,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.DeleteMonitorError,
            )
            return parse_grpc_response(
                rest_models.DeleteMonitorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteMonitor,
                operation_name="DeleteMonitor",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.DeleteMonitor(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def set_monitor_status(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.BgpMonitoringAdminServiceSetMonitorStatusBody,
    ) -> rest_models.SetMonitorStatusResponse:
        """
        Sets administrative status of a BGP monitor.

        Sets administrative status of BGP monitor with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.SetMonitorStatusRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.SetMonitorStatus,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule1.SetMonitorStatusError,
            )
            return parse_grpc_response(
                rest_models.SetMonitorStatusResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.SetMonitorStatus,
                operation_name="SetMonitorStatus",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule1.SetMonitorStatus(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_metrics_for_target(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GetMetricsForTargetRequest,
    ) -> rest_models.GetMetricsForTargetResponse:
        """
        Get metrics for a BGP prefix.

        Retrieve metric data for single BGP prefix and time interval.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetMetricsForTargetRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetMetricsForTarget,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule2.GetMetricsForTargetError,
            )
            return parse_grpc_response(
                rest_models.GetMetricsForTargetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetMetricsForTarget,
                operation_name="GetMetricsForTarget",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule2.GetMetricsForTarget(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_routes_for_target(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GetRoutesForTargetRequest,
    ) -> rest_models.GetRoutesForTargetResponse:
        """
        Get routes for a BGP prefix.

        Retrieve snapshot of route information for single BGP prefix at specific time.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for bgp_monitoring service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetRoutesForTargetRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetRoutesForTarget,
                _req,
                api_config=api_config_override,
                error_cls=RestBgpMonitoringModule2.GetRoutesForTargetError,
            )
            return parse_grpc_response(
                rest_models.GetRoutesForTargetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetRoutesForTarget,
                operation_name="GetRoutesForTarget",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestBgpMonitoringModule2.GetRoutesForTarget(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
