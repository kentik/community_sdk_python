from typing import Optional, Union, cast

import kentik_api.gen.audit.services.AuditService as RestAuditModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.audit import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class AuditServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.audit.pb.audit_pb2 as _pb2_1_mod
                import kentik_api.gen.audit.pb.audit_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.AuditServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list_events(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        startTime: Optional[str] = None,
        endTime: Optional[str] = None,
        offset: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> rest_models.ListAuditEventsResponse:
        """
        List Audit Events.

        Returns a list of audit events.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for audit service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListAuditEventsRequest,
                None,
                {
                    "startTime": startTime,
                    "endTime": endTime,
                    "offset": offset,
                    "limit": limit,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListAuditEvents,
                _req,
                api_config=api_config_override,
                error_cls=RestAuditModule1.ListEventsError,
            )
            return parse_grpc_response(
                rest_models.ListAuditEventsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListAuditEvents,
                operation_name="ListAuditEvents",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAuditModule1.ListAuditEvents(
                api_config_override=api_config_override or rest_transport.api_config,
                startTime=startTime,
                endTime=endTime,
                offset=offset,
                limit=limit,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_event(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        ctime: Optional[str] = None,
    ) -> rest_models.GetAuditEventResponse:
        """
        Get an Audit Event

        Return a specific audit event.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for audit service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetAuditEventRequest, None, {"id": id, "ctime": ctime}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetAuditEvent,
                _req,
                api_config=api_config_override,
                error_cls=RestAuditModule1.GetEventError,
            )
            return parse_grpc_response(
                rest_models.GetAuditEventResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetAuditEvent,
                operation_name="GetAuditEvent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAuditModule1.GetAuditEvent(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                ctime=ctime,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_event_by_ctime(
        self, *, api_config_override: Optional[APIConfig] = None, id: str, ctime: str
    ) -> rest_models.GetAuditEventResponse:
        """
        Get an Audit Event

        Return a specific audit event.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for audit service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetAuditEventRequest, None, {"id": id, "ctime": ctime}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetAuditEvent,
                _req,
                api_config=api_config_override,
                error_cls=RestAuditModule1.GetEventByCtimeError,
            )
            return parse_grpc_response(
                rest_models.GetAuditEventResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetAuditEvent,
                operation_name="GetAuditEvent_2",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAuditModule1.GetAuditEvent_2(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                ctime=ctime,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
