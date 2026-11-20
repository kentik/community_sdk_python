from typing import List, Optional, Union, cast

import kentik_api.gen.vault.services.VaultService as RestVaultModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.vault import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class VaultServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.vault.pb.vault_pb2 as _pb2_1_mod
                import kentik_api.gen.vault.pb.vault_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.VaultServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list_secret(
        self, *, api_config_override: Optional[APIConfig] = None, names: List[str]
    ) -> rest_models.ListSecretResponse:
        """
        List secrets.

        Returns list of secret values stored in Kentik vault.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for vault service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListSecretRequest, None, {"names": names}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListSecret,
                _req,
                api_config=api_config_override,
                error_cls=RestVaultModule1.ListSecretError,
            )
            return parse_grpc_response(
                rest_models.ListSecretResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListSecret,
                operation_name="ListSecret",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestVaultModule1.ListSecret(
                api_config_override=api_config_override or rest_transport.api_config,
                names=names,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_secret(
        self, *, api_config_override: Optional[APIConfig] = None, name: str
    ) -> rest_models.GetSecretResponse:
        """
        Get a secret by name.

        Returns a secret value stored in Kentik vault.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for vault service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetSecretRequest, None, {"name": name}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetSecret,
                _req,
                api_config=api_config_override,
                error_cls=RestVaultModule1.GetSecretError,
            )
            return parse_grpc_response(
                rest_models.GetSecretResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetSecret,
                operation_name="GetSecret",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestVaultModule1.GetSecret(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
