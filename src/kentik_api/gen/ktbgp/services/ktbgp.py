from typing import Optional, Union, cast

import kentik_api.gen.ktbgp.services.RouteService as RestKtbgpModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.ktbgp import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class KtbgpServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.ktbgp.pb.route_service_pb2 as _pb2_1_mod
                import kentik_api.gen.ktbgp.pb.route_service_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.RouteServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def route_announce(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.RouteServiceAnnounceRequest,
    ) -> rest_models.RouteServiceAnnounceResponse:
        """
        Announce a BGP route to a specified set of devices
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ktbgp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.RouteServiceAnnounceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.Announce,
                _req,
                api_config=api_config_override,
                error_cls=RestKtbgpModule1.RouteAnnounceError,
            )
            return parse_grpc_response(
                rest_models.RouteServiceAnnounceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.Announce,
                operation_name="RouteService_Announce",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKtbgpModule1.RouteService_Announce(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def route_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.RouteServiceListRequest,
    ) -> rest_models.RouteServiceListResponse:
        """
        List active BGP updates for a specified set of devices
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ktbgp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.RouteServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.List,
                _req,
                api_config=api_config_override,
                error_cls=RestKtbgpModule1.RouteListError,
            )
            return parse_grpc_response(
                rest_models.RouteServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.List,
                operation_name="RouteService_List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKtbgpModule1.RouteService_List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def route_withdraw(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.RouteServiceWithdrawRequest,
    ) -> rest_models.RouteServiceWithdrawResponse:
        """
        Withdraw active BGP updates from devices
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ktbgp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.RouteServiceWithdrawRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.Withdraw,
                _req,
                api_config=api_config_override,
                error_cls=RestKtbgpModule1.RouteWithdrawError,
            )
            return parse_grpc_response(
                rest_models.RouteServiceWithdrawResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.Withdraw,
                operation_name="RouteService_Withdraw",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKtbgpModule1.RouteService_Withdraw(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
