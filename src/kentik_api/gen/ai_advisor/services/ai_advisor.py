from typing import Optional, Union, cast

import kentik_api.gen.ai_advisor.services.AiAdvisorDataService as RestAiAdvisorModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.ai_advisor import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class AiAdvisorServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.ai_advisor.pb.ai_advisor_pb2 as _pb2_1_mod
                import kentik_api.gen.ai_advisor.pb.ai_advisor_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.AiAdvisorDataServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def create_chat_session(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateChatSessionRequest,
    ) -> rest_models.CreateChatSessionResponse:
        """
        Create AI Advisor Chat Session

        Create a new AI Advisor Chat session with a prompt
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ai_advisor service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateChatSessionRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateChatSession,
                _req,
                api_config=api_config_override,
                error_cls=RestAiAdvisorModule1.CreateChatSessionError,
            )
            return parse_grpc_response(
                rest_models.CreateChatSessionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateChatSession,
                operation_name="CreateChatSession",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAiAdvisorModule1.CreateChatSession(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_chat_session(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.UpdateChatSessionRequest,
    ) -> rest_models.UpdateChatSessionResponse:
        """
        Update AI Advisor Chat Session

        Update AI Advisor Chat session with a prompt
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ai_advisor service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateChatSessionRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateChatSession,
                _req,
                api_config=api_config_override,
                error_cls=RestAiAdvisorModule1.UpdateChatSessionError,
            )
            return parse_grpc_response(
                rest_models.UpdateChatSessionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateChatSession,
                operation_name="UpdateChatSession",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAiAdvisorModule1.UpdateChatSession(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_chat_session(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetChatSessionResponse:
        """
        Get AI Advisor Chat Session

        Retrieve the status and results of an AI Advisor chat session
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for ai_advisor service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetChatSessionRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetChatSession,
                _req,
                api_config=api_config_override,
                error_cls=RestAiAdvisorModule1.GetChatSessionError,
            )
            return parse_grpc_response(
                rest_models.GetChatSessionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetChatSession,
                operation_name="GetChatSession",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAiAdvisorModule1.GetChatSession(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
