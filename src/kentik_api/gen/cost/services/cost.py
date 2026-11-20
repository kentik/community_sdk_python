from typing import Optional, Union, cast

import kentik_api.gen.cost.services.CostService as RestCostModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.cost import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CostServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.cost.pb.cost_pb2 as _pb2_1_mod
                import kentik_api.gen.cost.pb.cost_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CostServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list_providers(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCostProvidersResponse:
        """
        List all cost providers.

        Returns list of configured cost providers.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cost service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCostProvidersRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCostProviders,
                _req,
                api_config=api_config_override,
                error_cls=RestCostModule1.ListProvidersError,
            )
            return parse_grpc_response(
                rest_models.ListCostProvidersResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCostProviders,
                operation_name="ListCostProviders",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCostModule1.ListCostProviders(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_provider_summaries(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        date: Optional[str] = None,
    ) -> rest_models.ListCostProviderSummariesResponse:
        """
        List all cost provider summaries.

        Returns list of summaries of configured cost providers.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cost service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCostProviderSummariesRequest, None, {"date": date}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCostProviderSummaries,
                _req,
                api_config=api_config_override,
                error_cls=RestCostModule1.ListProviderSummariesError,
            )
            return parse_grpc_response(
                rest_models.ListCostProviderSummariesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCostProviderSummaries,
                operation_name="ListCostProviderSummaries",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCostModule1.ListCostProviderSummaries(
                api_config_override=api_config_override or rest_transport.api_config,
                date=date,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_provider_summary(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        date: Optional[str] = None,
    ) -> rest_models.GetCostProviderSummaryResponse:
        """
        Get cost provider summary.

        Returns summary of configured cost provider.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for cost service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCostProviderSummaryRequest,
                None,
                {"id": id, "date": date},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCostProviderSummary,
                _req,
                api_config=api_config_override,
                error_cls=RestCostModule1.GetProviderSummaryError,
            )
            return parse_grpc_response(
                rest_models.GetCostProviderSummaryResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCostProviderSummary,
                operation_name="GetCostProviderSummary",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCostModule1.GetCostProviderSummary(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                date=date,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
