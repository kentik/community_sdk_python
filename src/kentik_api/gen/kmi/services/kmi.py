from typing import List, Optional, Union, cast

import kentik_api.gen.kmi.services.KmiService as RestKmiModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.kmi import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class KmiServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kmi.pb.kmi_pb2 as _pb2_1_mod
                import kentik_api.gen.kmi.pb.kmi_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.KmiServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def get_global_insights(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        limit: Optional[int] = None,
        marketId: Optional[str] = None,
        ip: Optional[str] = None,
        lookback: Optional[int] = None,
        types: Optional[List[str]] = None,
        magnitude: Optional[int] = None,
    ) -> rest_models.GetGlobalInsightsResponse:
        """
        List global KMI insights.

        Returns list of global KMI insights.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kmi service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetGlobalInsightsRequest,
                None,
                {
                    "limit": limit,
                    "marketId": marketId,
                    "ip": ip,
                    "lookback": lookback,
                    "types": types,
                    "magnitude": magnitude,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetGlobalInsights,
                _req,
                api_config=api_config_override,
                error_cls=RestKmiModule1.GetGlobalInsightsError,
            )
            return parse_grpc_response(
                rest_models.GetGlobalInsightsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetGlobalInsights,
                operation_name="GetGlobalInsights",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKmiModule1.GetGlobalInsights(
                api_config_override=api_config_override or rest_transport.api_config,
                limit=limit,
                marketId=marketId,
                ip=ip,
                lookback=lookback,
                types=types,
                magnitude=magnitude,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_asn_insights(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        asn: str,
        limit: Optional[int] = None,
        marketId: Optional[str] = None,
        ip: Optional[str] = None,
        lookback: Optional[int] = None,
        types: Optional[List[str]] = None,
        magnitude: Optional[int] = None,
    ) -> rest_models.GetASNInsightsResponse:
        """
        List ASN-specific KMI insights.

        Returns list of KMI insights for a specific Autonomous System.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kmi service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetASNInsightsRequest,
                None,
                {
                    "asn": asn,
                    "limit": limit,
                    "marketId": marketId,
                    "ip": ip,
                    "lookback": lookback,
                    "types": types,
                    "magnitude": magnitude,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetASNInsights,
                _req,
                api_config=api_config_override,
                error_cls=RestKmiModule1.GetAsnInsightsError,
            )
            return parse_grpc_response(
                rest_models.GetASNInsightsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetASNInsights,
                operation_name="GetASNInsights",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKmiModule1.GetASNInsights(
                api_config_override=api_config_override or rest_transport.api_config,
                asn=asn,
                limit=limit,
                marketId=marketId,
                ip=ip,
                lookback=lookback,
                types=types,
                magnitude=magnitude,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_asn_details(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        marketId: str,
        asn: str,
        type: str,
        data: rest_models.KmiServiceGetASNDetailsBody,
    ) -> rest_models.GetASNDetailsResponse:
        """
        List metadata and list of customers, providers, and peers for an Autonomous System.

        Returns metadata and list of customers, providers, and peers for an Autonomous System.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kmi service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetASNDetailsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"market_id": marketId, "asn": asn, "type": type},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetASNDetails,
                _req,
                api_config=api_config_override,
                error_cls=RestKmiModule1.GetAsnDetailsError,
            )
            return parse_grpc_response(
                rest_models.GetASNDetailsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetASNDetails,
                operation_name="GetASNDetails",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKmiModule1.GetASNDetails(
                api_config_override=api_config_override or rest_transport.api_config,
                marketId=marketId,
                asn=asn,
                type=type,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_rankings(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        marketId: str,
        rankType: str,
        ip: str,
        data: rest_models.KmiServiceGetRankingsBody,
    ) -> rest_models.GetRankingsResponse:
        """
        List KMI rankings by geo market and rank type.

        Returns list of KMI rankings.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kmi service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetRankingsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"market_id": marketId, "rank_type": rankType, "ip": ip},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetRankings,
                _req,
                api_config=api_config_override,
                error_cls=RestKmiModule1.GetRankingsError,
            )
            return parse_grpc_response(
                rest_models.GetRankingsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetRankings,
                operation_name="GetRankings",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKmiModule1.GetRankings(
                api_config_override=api_config_override or rest_transport.api_config,
                marketId=marketId,
                rankType=rankType,
                ip=ip,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_markets(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListMarketsResponse:
        """
        List all geo markets for KMI.

        Returns list of geo markets for KMI.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kmi service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListMarketsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListMarkets,
                _req,
                api_config=api_config_override,
                error_cls=RestKmiModule1.ListMarketsError,
            )
            return parse_grpc_response(
                rest_models.ListMarketsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListMarkets,
                operation_name="ListMarkets",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKmiModule1.ListMarkets(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
