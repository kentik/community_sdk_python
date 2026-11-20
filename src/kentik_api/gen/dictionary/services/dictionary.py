from typing import Optional, Union, cast

import kentik_api.gen.dictionary.services.DictionaryService as RestDictionaryModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.dictionary import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class DictionaryServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.dictionary.pb.dictionary_pb2 as _pb2_1_mod
                import kentik_api.gen.dictionary.pb.dictionary_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.DictionaryServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def get(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.GetDictionaryResponse:
        """
        Get Dictionary

        Returns the full UDE dictionary for the authenticated company, including all measurements with their dimension and metric fields, operator sets, and metric family definitions.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for dictionary service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.GetDictionaryRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetDictionary,
                _req,
                api_config=api_config_override,
                error_cls=RestDictionaryModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetDictionaryResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetDictionary,
                operation_name="GetDictionary",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestDictionaryModule1.GetDictionary(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
