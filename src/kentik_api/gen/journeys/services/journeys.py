from typing import Optional, Union, cast

import kentik_api.gen.journeys.services.JourneysDataService as RestJourneysModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.journeys import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class JourneysServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.journeys.pb.journeys_pb2 as _pb2_1_mod
                import kentik_api.gen.journeys.pb.journeys_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.JourneysDataServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def get_nlq(
        self, *, api_config_override: Optional[APIConfig] = None, prompt: str
    ) -> rest_models.GetJourneysNlqResponse:
        """
        Journeys AI NLQ Service

        Perform Natural Language (NLQ) to query object translation
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for journeys service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetJourneysNlqRequest, None, {"prompt": prompt}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetJourneysNlq,
                _req,
                api_config=api_config_override,
                error_cls=RestJourneysModule1.GetNlqError,
            )
            return parse_grpc_response(
                rest_models.GetJourneysNlqResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetJourneysNlq,
                operation_name="GetJourneysNlq",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestJourneysModule1.GetJourneysNlq(
                api_config_override=api_config_override or rest_transport.api_config,
                prompt=prompt,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
