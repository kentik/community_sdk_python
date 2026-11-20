from typing import Optional, Union, cast

import kentik_api.gen.site.services.SiteService as RestSiteModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.site import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class SiteServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.site.pb.site_pb2 as _pb2_1_mod
                import kentik_api.gen.site.pb.site_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.SiteServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list_markets(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListSiteMarketsResponse:
        """
        List all site markets.

        Returns list of configured site markets.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListSiteMarketsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListSiteMarkets,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.ListMarketsError,
            )
            return parse_grpc_response(
                rest_models.ListSiteMarketsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListSiteMarkets,
                operation_name="ListSiteMarkets",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.ListSiteMarkets(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_market(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateSiteMarketRequest,
    ) -> rest_models.CreateSiteMarketResponse:
        """
        Configure a new site market.

        Create configuration for a new site market. Returns the newly created configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateSiteMarketRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateSiteMarket,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.CreateMarketError,
            )
            return parse_grpc_response(
                rest_models.CreateSiteMarketResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateSiteMarket,
                operation_name="CreateSiteMarket",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.CreateSiteMarket(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_market(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetSiteMarketResponse:
        """
        Retrieve configuration of a site market.

        Returns configuration of a site market specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetSiteMarketRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetSiteMarket,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.GetMarketError,
            )
            return parse_grpc_response(
                rest_models.GetSiteMarketResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetSiteMarket,
                operation_name="GetSiteMarket",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.GetSiteMarket(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_market(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SiteServiceUpdateSiteMarketBody,
    ) -> rest_models.UpdateSiteMarketResponse:
        """
        Updates configuration of a site market.

        Replaces configuration of a site market with attributes in the request. Returns the updated configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateSiteMarketRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"site_market.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateSiteMarket,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.UpdateMarketError,
            )
            return parse_grpc_response(
                rest_models.UpdateSiteMarketResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateSiteMarket,
                operation_name="UpdateSiteMarket",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.UpdateSiteMarket(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_market(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteSiteMarketResponse:
        """
        Delete configuration of a site market.

        Deletes configuration of a site market with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteSiteMarketRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteSiteMarket,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.DeleteMarketError,
            )
            return parse_grpc_response(
                rest_models.DeleteSiteMarketResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteSiteMarket,
                operation_name="DeleteSiteMarket",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.DeleteSiteMarket(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListSitesResponse:
        """
        List all sites.

        Returns list of configured sites.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListSitesRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListSites,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListSitesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListSites,
                operation_name="ListSites",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.ListSites(
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
        data: rest_models.CreateSiteRequest,
    ) -> rest_models.CreateSiteResponse:
        """
        Configure a new site.

        Create configuration for a new site. Returns the newly created configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateSiteRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateSite,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateSiteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateSite,
                operation_name="CreateSite",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.CreateSite(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetSiteResponse:
        """
        Retrieve configuration of a site.

        Returns configuration of a site specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.GetSiteRequest, None, {"id": id})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetSite,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetSiteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetSite,
                operation_name="GetSite",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.GetSite(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SiteServiceUpdateSiteBody,
    ) -> rest_models.UpdateSiteResponse:
        """
        Updates configuration of a site.

        Replaces configuration of a site with attributes in the request. Returns the updated configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateSiteRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"site.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateSite,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateSiteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateSite,
                operation_name="UpdateSite",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.UpdateSite(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteSiteResponse:
        """
        Delete configuration of a site.

        Deletes configuration of a site with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for site service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteSiteRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteSite,
                _req,
                api_config=api_config_override,
                error_cls=RestSiteModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteSiteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteSite,
                operation_name="DeleteSite",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSiteModule1.DeleteSite(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
