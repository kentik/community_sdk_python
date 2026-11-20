from typing import List, Optional, Union, cast

import kentik_api.gen.alerting.services.AlertAutoAckService as RestAlertingModule1
import kentik_api.gen.alerting.services.AlertService as RestAlertingModule2
import kentik_api.gen.alerting.services.AlertSilenceNotificationsService as RestAlertingModule3
import kentik_api.gen.alerting.services.MitigationMethodsService as RestAlertingModule4
import kentik_api.gen.alerting.services.MitigationPlatformsService as RestAlertingModule5
import kentik_api.gen.alerting.services.MitigationsService as RestAlertingModule6
import kentik_api.gen.alerting.services.PolicyService as RestAlertingModule7
import kentik_api.gen.alerting.services.SuppressionService as RestAlertingModule8
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.alerting import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class AlertingServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.alert_pb2 as _pb2_1_mod
                import kentik_api.gen.alerting.pb.alert_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.AlertServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.auto_ack_pb2 as _pb2_2_mod
                import kentik_api.gen.alerting.pb.auto_ack_pb2_grpc as _pb2_grpc_2_mod

                self._grpc_pb2_2 = _pb2_2_mod
                self._grpc_stub_2 = _pb2_grpc_2_mod.AlertAutoAckServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_2 = None
                self._grpc_stub_2 = None
                self._grpc_import_error_2 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.mitigation_method_pb2 as _pb2_3_mod
                import kentik_api.gen.alerting.pb.mitigation_method_pb2_grpc as _pb2_grpc_3_mod

                self._grpc_pb2_3 = _pb2_3_mod
                self._grpc_stub_3 = _pb2_grpc_3_mod.MitigationMethodsServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_3 = None
                self._grpc_stub_3 = None
                self._grpc_import_error_3 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.mitigation_platform_pb2 as _pb2_4_mod
                import kentik_api.gen.alerting.pb.mitigation_platform_pb2_grpc as _pb2_grpc_4_mod

                self._grpc_pb2_4 = _pb2_4_mod
                self._grpc_stub_4 = _pb2_grpc_4_mod.MitigationPlatformsServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_4 = None
                self._grpc_stub_4 = None
                self._grpc_import_error_4 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.mitigation_public_v202505_pb2 as _pb2_5_mod
                import kentik_api.gen.alerting.pb.mitigation_public_v202505_pb2_grpc as _pb2_grpc_5_mod

                self._grpc_pb2_5 = _pb2_5_mod
                self._grpc_stub_5 = _pb2_grpc_5_mod.MitigationsServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_5 = None
                self._grpc_stub_5 = None
                self._grpc_import_error_5 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.policy_pb2 as _pb2_6_mod
                import kentik_api.gen.alerting.pb.policy_pb2_grpc as _pb2_grpc_6_mod

                self._grpc_pb2_6 = _pb2_6_mod
                self._grpc_stub_6 = _pb2_grpc_6_mod.PolicyServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_6 = None
                self._grpc_stub_6 = None
                self._grpc_import_error_6 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.silencing_pb2 as _pb2_7_mod
                import kentik_api.gen.alerting.pb.silencing_pb2_grpc as _pb2_grpc_7_mod

                self._grpc_pb2_7 = _pb2_7_mod
                self._grpc_stub_7 = (
                    _pb2_grpc_7_mod.AlertSilenceNotificationsServiceStub(
                        self._transport.channel
                    )
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_7 = None
                self._grpc_stub_7 = None
                self._grpc_import_error_7 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.suppressions_public_v202505_pb2 as _pb2_8_mod
                import kentik_api.gen.alerting.pb.suppressions_public_v202505_pb2_grpc as _pb2_grpc_8_mod

                self._grpc_pb2_8 = _pb2_8_mod
                self._grpc_stub_8 = _pb2_grpc_8_mod.SuppressionServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_8 = None
                self._grpc_stub_8 = None
                self._grpc_import_error_8 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.alerting.pb.suppressions_public_v202611_pb2 as _pb2_9_mod
                import kentik_api.gen.alerting.pb.suppressions_public_v202611_pb2_grpc as _pb2_grpc_9_mod

                self._grpc_pb2_9 = _pb2_9_mod
                self._grpc_stub_9 = _pb2_grpc_9_mod.SuppressionServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_9 = None
                self._grpc_stub_9 = None
                self._grpc_import_error_9 = exc

    def auto_ack_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertAutoAckServiceCreateRequest,
    ) -> rest_models.AlertAutoAckServiceCreateResponse:
        """
        Create Auto-Ack

        Creates a new auto-ack configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AlertAutoAckServiceCreateRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.Create,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule1.AutoAckCreateError,
            )
            return parse_grpc_response(
                rest_models.AlertAutoAckServiceCreateResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.Create,
                operation_name="Create",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule1.Create(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def auto_ack_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertAutoAckServiceListRequest,
    ) -> rest_models.AlertAutoAckServiceListResponse:
        """
        List Auto-Acks

        Returns a list of auto-ack configurations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AlertAutoAckServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule1.AutoAckListError,
            )
            return parse_grpc_response(
                rest_models.AlertAutoAckServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule1.List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def auto_ack_get(
        self, *, api_config_override: Optional[APIConfig] = None, autoAckid: str
    ) -> rest_models.AlertAutoAckServiceGetResponse:
        """
        Get Auto-Ack

        Returns an auto-ack configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AlertAutoAckServiceGetRequest, None, {"id": autoAckid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule1.AutoAckGetError,
            )
            return parse_grpc_response(
                rest_models.AlertAutoAckServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule1.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                autoAckid=autoAckid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def auto_ack_delete(
        self, *, api_config_override: Optional[APIConfig] = None, autoAckid: str
    ) -> rest_models.AlertAutoAckServiceDeleteResponse:
        """
        Delete Auto-Ack

        Deletes an auto-ack configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AlertAutoAckServiceDeleteRequest,
                None,
                {"id": autoAckid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.Delete,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule1.AutoAckDeleteError,
            )
            return parse_grpc_response(
                rest_models.AlertAutoAckServiceDeleteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.Delete,
                operation_name="Delete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule1.Delete(
                api_config_override=api_config_override or rest_transport.api_config,
                autoAckid=autoAckid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def auto_ack_replace(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        autoAckid: str,
        data: rest_models.AlertAutoAckServiceReplaceBody,
    ) -> rest_models.AlertAutoAckServiceReplaceResponse:
        """
        Replace Auto-Ack

        Replaces an auto-ack configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AlertAutoAckServiceReplaceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"auto_ack.id": autoAckid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.Replace,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule1.AutoAckReplaceError,
            )
            return parse_grpc_response(
                rest_models.AlertAutoAckServiceReplaceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.Replace,
                operation_name="Replace",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule1.Replace(
                api_config_override=api_config_override or rest_transport.api_config,
                autoAckid=autoAckid,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertServiceListRequest,
    ) -> rest_models.AlertServiceListResponse:
        """
        List Alerts

        Returns an array of alert objects that contain information about individual alerts.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.ListError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def clear(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertServiceClearRequest,
    ) -> rest_models.AlertServiceClearResponse:
        """
        Clear Alerts

        Clears alerts.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceClearRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.Clear,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.ClearError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceClearResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.Clear,
                operation_name="Clear",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.Clear(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_comments(
        self, *, api_config_override: Optional[APIConfig] = None, alertId: str
    ) -> rest_models.AlertServiceListCommentsResponse:
        """
        List Alert Comments

        Returns all comments for an alert.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceListCommentsRequest,
                None,
                {"alert_id": alertId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListComments,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.ListCommentsError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceListCommentsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListComments,
                operation_name="ListComments",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.ListComments(
                api_config_override=api_config_override or rest_transport.api_config,
                alertId=alertId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def add_comment(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        alertId: str,
        data: rest_models.AlertServiceAddCommentBody,
    ) -> rest_models.AlertServiceAddCommentResponse:
        """
        Add Alert Comment

        Adds a comment to an alert.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceAddCommentRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"alert_id": alertId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.AddComment,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.AddCommentError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceAddCommentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.AddComment,
                operation_name="AddComment",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.AddComment(
                api_config_override=api_config_override or rest_transport.api_config,
                alertId=alertId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def set_external_context(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        alertId: str,
        data: rest_models.AlertServiceSetExternalContextBody,
    ) -> rest_models.AlertServiceSetExternalContextResponse:
        """
        Set External Context for Alert

        Add or replace external context
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceSetExternalContextRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"alert_id": alertId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.SetExternalContext,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.SetExternalContextError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceSetExternalContextResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.SetExternalContext,
                operation_name="SetExternalContext",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.SetExternalContext(
                api_config_override=api_config_override or rest_transport.api_config,
                alertId=alertId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.AlertServiceGetResponse:
        """
        Get Alert

        Returns an alert object that contains information about an individual alert.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceGetRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.GetError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def ack(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.AlertServiceAckBody,
    ) -> rest_models.AlertServiceAckResponse:
        """
        Ack Alert

        Acknowledges an alert.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceAckRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.Ack,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.AckError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceAckResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.Ack,
                operation_name="Ack",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.Ack(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def un_ack(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.AlertServiceUnAckBody,
    ) -> rest_models.AlertServiceUnAckResponse:
        """
        UnAck Alert

        Unacknowledges an alert (removes the acknowledgement).
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AlertServiceUnAckRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UnAck,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule2.UnAckError,
            )
            return parse_grpc_response(
                rest_models.AlertServiceUnAckResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UnAck,
                operation_name="UnAck",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule2.UnAck(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def silence_notifications_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertSilenceNotificationsServiceCreateRequest,
    ) -> rest_models.AlertSilenceNotificationsServiceCreateResponse:
        """
        Create Alert Silence Notifications

        Creates a new alert silence notifications configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_7 is None or self._grpc_stub_7 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_7!r}"
                ) from self._grpc_import_error_7
            _req = build_grpc_request(
                self._grpc_pb2_7.AlertSilenceNotificationsServiceCreateRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_7.Create,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule3.SilenceNotificationsCreateError,
            )
            return parse_grpc_response(
                rest_models.AlertSilenceNotificationsServiceCreateResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_7.Create,
                operation_name="Create",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule3.Create(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def silence_notifications_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.AlertSilenceNotificationsServiceListRequest,
    ) -> rest_models.AlertSilenceNotificationsServiceListResponse:
        """
        List Alert Notification Silences

        Returns a list of alert silence notifications configurations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_7 is None or self._grpc_stub_7 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_7!r}"
                ) from self._grpc_import_error_7
            _req = build_grpc_request(
                self._grpc_pb2_7.AlertSilenceNotificationsServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_7.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule3.SilenceNotificationsListError,
            )
            return parse_grpc_response(
                rest_models.AlertSilenceNotificationsServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_7.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule3.List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def silence_notifications_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.AlertSilenceNotificationsServiceGetResponse:
        """
        Get Alert Silence Notifications

        Returns an alert silence notifications configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_7 is None or self._grpc_stub_7 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_7!r}"
                ) from self._grpc_import_error_7
            _req = build_grpc_request(
                self._grpc_pb2_7.AlertSilenceNotificationsServiceGetRequest,
                None,
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_7.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule3.SilenceNotificationsGetError,
            )
            return parse_grpc_response(
                rest_models.AlertSilenceNotificationsServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_7.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule3.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def silence_notifications_delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.AlertSilenceNotificationsServiceDeleteResponse:
        """
        Delete Alert Notification Silence

        Deletes an alert silence notifications configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_7 is None or self._grpc_stub_7 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_7!r}"
                ) from self._grpc_import_error_7
            _req = build_grpc_request(
                self._grpc_pb2_7.AlertSilenceNotificationsServiceDeleteRequest,
                None,
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_7.Delete,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule3.SilenceNotificationsDeleteError,
            )
            return parse_grpc_response(
                rest_models.AlertSilenceNotificationsServiceDeleteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_7.Delete,
                operation_name="Delete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule3.Delete(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def silence_notifications_replace(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.AlertSilenceNotificationsServiceReplaceBody,
    ) -> rest_models.AlertSilenceNotificationsServiceReplaceResponse:
        """
        Replace Alert Notification Silence

        Replaces an alert silence notifications configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_7 is None or self._grpc_stub_7 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_7!r}"
                ) from self._grpc_import_error_7
            _req = build_grpc_request(
                self._grpc_pb2_7.AlertSilenceNotificationsServiceReplaceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"silence.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_7.Replace,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule3.SilenceNotificationsReplaceError,
            )
            return parse_grpc_response(
                rest_models.AlertSilenceNotificationsServiceReplaceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_7.Replace,
                operation_name="Replace",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule3.Replace(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigation_methods_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        paginationlimit: Optional[str] = None,
        paginationoffset: Optional[str] = None,
        paginationincludeTotalCount: Optional[bool] = None,
        filtersmethodIds: Optional[List[str]] = None,
        filtersplatformTypes: Optional[List[str]] = None,
        filterscreatedAtstart: Optional[str] = None,
        filterscreatedAtend: Optional[str] = None,
        filtersmodifiedAtstart: Optional[str] = None,
        filtersmodifiedAtend: Optional[str] = None,
    ) -> rest_models.MitigationMethodsServiceListResponse:
        """
        List Mitigation Methods

        Returns a list of mitigation methods.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.MitigationMethodsServiceListRequest,
                None,
                {
                    "pagination.limit": paginationlimit,
                    "pagination.offset": paginationoffset,
                    "pagination.includeTotalCount": paginationincludeTotalCount,
                    "filters.methodIds": filtersmethodIds,
                    "filters.platformTypes": filtersplatformTypes,
                    "filters.createdAt.start": filterscreatedAtstart,
                    "filters.createdAt.end": filterscreatedAtend,
                    "filters.modifiedAt.start": filtersmodifiedAtstart,
                    "filters.modifiedAt.end": filtersmodifiedAtend,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule4.MitigationMethodsListError,
            )
            return parse_grpc_response(
                rest_models.MitigationMethodsServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule4.List(
                api_config_override=api_config_override or rest_transport.api_config,
                paginationlimit=paginationlimit,
                paginationoffset=paginationoffset,
                paginationincludeTotalCount=paginationincludeTotalCount,
                filtersmethodIds=filtersmethodIds,
                filtersplatformTypes=filtersplatformTypes,
                filterscreatedAtstart=filterscreatedAtstart,
                filterscreatedAtend=filterscreatedAtend,
                filtersmodifiedAtstart=filtersmodifiedAtstart,
                filtersmodifiedAtend=filtersmodifiedAtend,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigation_methods_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.MitigationMethodsServiceGetResponse:
        """
        Get Mitigation Method

        Returns a mitigation method.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.MitigationMethodsServiceGetRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule4.MitigationMethodsGetError,
            )
            return parse_grpc_response(
                rest_models.MitigationMethodsServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule4.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigation_platforms_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        paginationlimit: Optional[str] = None,
        paginationoffset: Optional[str] = None,
        paginationincludeTotalCount: Optional[bool] = None,
        filtersplatformIds: Optional[List[str]] = None,
        filtersplatformTypes: Optional[List[str]] = None,
        filterscreatedAtstart: Optional[str] = None,
        filterscreatedAtend: Optional[str] = None,
        filtersmodifiedAtstart: Optional[str] = None,
        filtersmodifiedAtend: Optional[str] = None,
    ) -> rest_models.MitigationPlatformsServiceListResponse:
        """
        List Mitigation Platforms

        Returns a list of mitigation platforms.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.MitigationPlatformsServiceListRequest,
                None,
                {
                    "pagination.limit": paginationlimit,
                    "pagination.offset": paginationoffset,
                    "pagination.includeTotalCount": paginationincludeTotalCount,
                    "filters.platformIds": filtersplatformIds,
                    "filters.platformTypes": filtersplatformTypes,
                    "filters.createdAt.start": filterscreatedAtstart,
                    "filters.createdAt.end": filterscreatedAtend,
                    "filters.modifiedAt.start": filtersmodifiedAtstart,
                    "filters.modifiedAt.end": filtersmodifiedAtend,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule5.MitigationPlatformsListError,
            )
            return parse_grpc_response(
                rest_models.MitigationPlatformsServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule5.List(
                api_config_override=api_config_override or rest_transport.api_config,
                paginationlimit=paginationlimit,
                paginationoffset=paginationoffset,
                paginationincludeTotalCount=paginationincludeTotalCount,
                filtersplatformIds=filtersplatformIds,
                filtersplatformTypes=filtersplatformTypes,
                filterscreatedAtstart=filterscreatedAtstart,
                filterscreatedAtend=filterscreatedAtend,
                filtersmodifiedAtstart=filtersmodifiedAtstart,
                filtersmodifiedAtend=filtersmodifiedAtend,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigation_platforms_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.MitigationPlatformsServiceGetResponse:
        """
        Get Mitigation Platform

        Returns a mitigation platform.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.MitigationPlatformsServiceGetRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule5.MitigationPlatformsGetError,
            )
            return parse_grpc_response(
                rest_models.MitigationPlatformsServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule5.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigations_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        paginationlimit: Optional[str] = None,
        paginationoffset: Optional[str] = None,
        paginationincludeTotalCount: Optional[bool] = None,
        filterscreatedAtstart: Optional[str] = None,
        filterscreatedAtend: Optional[str] = None,
        filtersmitigationIds: Optional[List[str]] = None,
        filtersalarmIds: Optional[List[str]] = None,
        filtersstates: Optional[List[str]] = None,
        filtersplatformIds: Optional[List[str]] = None,
        filtersmethodIds: Optional[List[str]] = None,
        filtersipCidrs: Optional[List[str]] = None,
        filtersipCidrPattern: Optional[str] = None,
        filterstypes: Optional[List[str]] = None,
    ) -> rest_models.MitigationsServiceListResponse:
        """
        List Mitigations

        Returns a list of mitigations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceListRequest,
                None,
                {
                    "pagination.limit": paginationlimit,
                    "pagination.offset": paginationoffset,
                    "pagination.includeTotalCount": paginationincludeTotalCount,
                    "filters.createdAt.start": filterscreatedAtstart,
                    "filters.createdAt.end": filterscreatedAtend,
                    "filters.mitigationIds": filtersmitigationIds,
                    "filters.alarmIds": filtersalarmIds,
                    "filters.states": filtersstates,
                    "filters.platformIds": filtersplatformIds,
                    "filters.methodIds": filtersmethodIds,
                    "filters.ipCidrs": filtersipCidrs,
                    "filters.ipCidrPattern": filtersipCidrPattern,
                    "filters.types": filterstypes,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.MitigationsListError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.List(
                api_config_override=api_config_override or rest_transport.api_config,
                paginationlimit=paginationlimit,
                paginationoffset=paginationoffset,
                paginationincludeTotalCount=paginationincludeTotalCount,
                filterscreatedAtstart=filterscreatedAtstart,
                filterscreatedAtend=filterscreatedAtend,
                filtersmitigationIds=filtersmitigationIds,
                filtersalarmIds=filtersalarmIds,
                filtersstates=filtersstates,
                filtersplatformIds=filtersplatformIds,
                filtersmethodIds=filtersmethodIds,
                filtersipCidrs=filtersipCidrs,
                filtersipCidrPattern=filtersipCidrPattern,
                filterstypes=filterstypes,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigations_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.MitigationsServiceCreateRequest,
    ) -> rest_models.MitigationsServiceCreateResponse:
        """
        Create Mitigation

        Creates a new manual mitigation.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceCreateRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.Create,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.MitigationsCreateError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceCreateResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.Create,
                operation_name="Create",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.Create(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def available_actions(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.MitigationsServiceAvailableActionsResponse:
        """
        Get Available Actions

        Returns available actions for mitigations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceAvailableActionsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.AvailableActions,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.AvailableActionsError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceAvailableActionsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.AvailableActions,
                operation_name="AvailableActions",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.AvailableActions(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def mitigations_get(
        self, *, api_config_override: Optional[APIConfig] = None, action: str
    ) -> rest_models.MitigationsServiceGetResponse:
        """
        Get Mitigation

        Returns a mitigation.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceGetRequest, None, {"id": action}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.MitigationsGetError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                action=action,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def act(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        action: str,
        data: rest_models.MitigationsServiceActBody,
    ) -> rest_models.MitigationsServiceActResponse:
        """
        Act on Mitigation

        Performs an action on one or more mitigations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceActRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"action": action},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.Act,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.ActError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceActResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.Act,
                operation_name="Act",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.Act(
                api_config_override=api_config_override or rest_transport.api_config,
                action=action,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def available_actions_for_mitigation(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.MitigationsServiceAvailableActionsForMitigationResponse:
        """
        Get Available Actions for Mitigation

        Returns available actions for a specific mitigation.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.MitigationsServiceAvailableActionsForMitigationRequest,
                None,
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.AvailableActionsForMitigation,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule6.AvailableActionsForMitigationError,
            )
            return parse_grpc_response(
                rest_models.MitigationsServiceAvailableActionsForMitigationResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.AvailableActionsForMitigation,
                operation_name="AvailableActionsForMitigation",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule6.AvailableActionsForMitigation(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def policy_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.PolicyServiceListRequest,
    ) -> rest_models.PolicyServiceListResponse:
        """
        List Policies

        Returns a list of alerting policies.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.PolicyServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule7.PolicyListError,
            )
            return parse_grpc_response(
                rest_models.PolicyServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule7.List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def policy_get(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        policyType: str,
        id: str,
    ) -> rest_models.PolicyServiceGetResponse:
        """
        Get Policy

        Returns an alerting policy.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.PolicyServiceGetRequest,
                None,
                {"policy_type": policyType, "id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule7.PolicyGetError,
            )
            return parse_grpc_response(
                rest_models.PolicyServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule7.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                policyType=policyType,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def disable(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        policyType: str,
        id: str,
        data: rest_models.PolicyServiceDisableBody,
    ) -> rest_models.PolicyServiceDisableResponse:
        """
        Disable Policy

        Disables an alerting policy.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.PolicyServiceDisableRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"policy_type": policyType, "id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.Disable,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule7.DisableError,
            )
            return parse_grpc_response(
                rest_models.PolicyServiceDisableResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.Disable,
                operation_name="Disable",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule7.Disable(
                api_config_override=api_config_override or rest_transport.api_config,
                policyType=policyType,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def enable(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        policyType: str,
        id: str,
        data: rest_models.PolicyServiceEnableBody,
    ) -> rest_models.PolicyServiceEnableResponse:
        """
        Enable Policy

        Enables an alerting policy.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.PolicyServiceEnableRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"policy_type": policyType, "id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.Enable,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule7.EnableError,
            )
            return parse_grpc_response(
                rest_models.PolicyServiceEnableResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.Enable,
                operation_name="Enable",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule7.Enable(
                api_config_override=api_config_override or rest_transport.api_config,
                policyType=policyType,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def suppression_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.SuppressionServiceCreateRequest,
    ) -> rest_models.SuppressionServiceCreateResponse:
        """
        Create Suppression

        Creates a suppression configuration. At least one source, severity, key filter condition, or context filter condition is required.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_9 is None or self._grpc_stub_9 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_9!r}"
                ) from self._grpc_import_error_9
            _req = build_grpc_request(
                self._grpc_pb2_9.SuppressionServiceCreateRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_9.Create,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule8.SuppressionCreateError,
            )
            return parse_grpc_response(
                rest_models.SuppressionServiceCreateResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_9.Create,
                operation_name="Create",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule8.Create(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def suppression_list(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.SuppressionServiceListRequest,
    ) -> rest_models.SuppressionServiceListResponse:
        """
        List Suppressions

        Returns suppression configurations, including all matching constraints and resolved timestamps. Timestamp commands are not returned.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_9 is None or self._grpc_stub_9 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_9!r}"
                ) from self._grpc_import_error_9
            _req = build_grpc_request(
                self._grpc_pb2_9.SuppressionServiceListRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_9.List,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule8.SuppressionListError,
            )
            return parse_grpc_response(
                rest_models.SuppressionServiceListResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_9.List,
                operation_name="List",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule8.List(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def suppression_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.SuppressionServiceGetResponse:
        """
        Get Suppression

        Returns a suppression configuration, including all matching constraints and resolved timestamps. Timestamp commands are not returned.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_9 is None or self._grpc_stub_9 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_9!r}"
                ) from self._grpc_import_error_9
            _req = build_grpc_request(
                self._grpc_pb2_9.SuppressionServiceGetRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_9.Get,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule8.SuppressionGetError,
            )
            return parse_grpc_response(
                rest_models.SuppressionServiceGetResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_9.Get,
                operation_name="Get",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule8.Get(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def suppression_delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.SuppressionServiceDeleteResponse:
        """
        Delete Suppression

        Deletes a suppression configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_9 is None or self._grpc_stub_9 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_9!r}"
                ) from self._grpc_import_error_9
            _req = build_grpc_request(
                self._grpc_pb2_9.SuppressionServiceDeleteRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_9.Delete,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule8.SuppressionDeleteError,
            )
            return parse_grpc_response(
                rest_models.SuppressionServiceDeleteResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_9.Delete,
                operation_name="Delete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule8.Delete(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def suppression_replace(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SuppressionServiceReplaceBody,
    ) -> rest_models.SuppressionServiceReplaceResponse:
        """
        Replace Suppression

        Replaces the complete writable suppression configuration; this is not a partial update despite the PATCH HTTP method. Omitted matching constraints, display name, and comment are cleared. Output-only fields and server-managed metadata are not replaced. Use timestamp commands to preserve existing start or end times. Once active or starting too soon for changes to propagate, a suppression's start time and matching constraints cannot change; its end time, display name, and comment can change. Suppressions that have ended or are ending too soon cannot be replaced. Timing constraints still apply.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_9 is None or self._grpc_stub_9 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for alerting service failed to import: {self._grpc_import_error_9!r}"
                ) from self._grpc_import_error_9
            _req = build_grpc_request(
                self._grpc_pb2_9.SuppressionServiceReplaceRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"suppression.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_9.Replace,
                _req,
                api_config=api_config_override,
                error_cls=RestAlertingModule8.SuppressionReplaceError,
            )
            return parse_grpc_response(
                rest_models.SuppressionServiceReplaceResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_9.Replace,
                operation_name="Replace",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAlertingModule8.Replace(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
