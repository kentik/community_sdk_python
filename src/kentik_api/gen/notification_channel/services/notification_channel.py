from typing import Optional, Union, cast

import kentik_api.gen.notification_channel.services.NotificationChannelService as RestNotificationChannelModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.notification_channel import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class NotificationChannelServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.notification_channel.pb.notification_channel_pb2 as _pb2_1_mod
                import kentik_api.gen.notification_channel.pb.notification_channel_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.NotificationChannelServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListNotificationChannelsResponse:
        """
        List available notification channels

        Returns list of all configured notification channels.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for notification_channel service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListNotificationChannelsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListNotificationChannels,
                _req,
                api_config=api_config_override,
                error_cls=RestNotificationChannelModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListNotificationChannelsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListNotificationChannels,
                operation_name="ListNotificationChannels",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestNotificationChannelModule1.ListNotificationChannels(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def search(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.SearchNotificationChannelsRequest,
    ) -> rest_models.SearchNotificationChannelsResponse:
        """
        Retrieve notification channels matching criteria.

        Returns list of all notification channels matching request criteria. Match criteria are treated as a logical AND, i.e. all provided criteria must match in order for an entry to be included in the response.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for notification_channel service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.SearchNotificationChannelsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.SearchNotificationChannels,
                _req,
                api_config=api_config_override,
                error_cls=RestNotificationChannelModule1.SearchError,
            )
            return parse_grpc_response(
                rest_models.SearchNotificationChannelsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.SearchNotificationChannels,
                operation_name="SearchNotificationChannels",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestNotificationChannelModule1.SearchNotificationChannels(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetNotificationChannelResponse:
        """
        Get information about a notification channel

        Returns information about a notification channel with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for notification_channel service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetNotificationChannelRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetNotificationChannel,
                _req,
                api_config=api_config_override,
                error_cls=RestNotificationChannelModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetNotificationChannelResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetNotificationChannel,
                operation_name="GetNotificationChannel",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestNotificationChannelModule1.GetNotificationChannel(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
