from typing import Optional, Union, cast

import kentik_api.gen.rbux.services.ScopeService as RestRbuxModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.rbux import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class RbuxServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.rbux.pb.scope_pb2 as _pb2_1_mod
                import kentik_api.gen.rbux.pb.scope_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.ScopeServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list_scopes(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListScopesResponse:
        """
        List Focus Scopes

        Returns all Focus Scopes for the user's company.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for rbux service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListScopesRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListScopes,
                _req,
                api_config=api_config_override,
                error_cls=RestRbuxModule1.ListScopesError,
            )
            return parse_grpc_response(
                rest_models.ListScopesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListScopes,
                operation_name="ListScopes",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestRbuxModule1.ListScopes(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_scope(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.Scope,
    ) -> rest_models.CreateScopeResponse:
        """
        Create Focus Scope

        Creates and returns a new Focus Scope.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for rbux service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateScopeRequest,
                {"scope": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateScope,
                _req,
                api_config=api_config_override,
                error_cls=RestRbuxModule1.CreateScopeError,
            )
            return parse_grpc_response(
                rest_models.CreateScopeResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateScope,
                operation_name="CreateScope",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestRbuxModule1.CreateScope(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_scope(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetScopeResponse:
        """
        Get Focus Scope

        Returns a single Focus Scope by id.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for rbux service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetScopeRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetScope,
                _req,
                api_config=api_config_override,
                error_cls=RestRbuxModule1.GetScopeError,
            )
            return parse_grpc_response(
                rest_models.GetScopeResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetScope,
                operation_name="GetScope",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestRbuxModule1.GetScope(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_scope(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.ScopeServiceUpdateScopeBody,
    ) -> rest_models.UpdateScopeResponse:
        """
        Update Focus Scope

        Updates and returns an existing Focus Scope.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for rbux service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateScopeRequest,
                {"scope": data.model_dump(by_alias=True, exclude_unset=True)},
                {"scope.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateScope,
                _req,
                api_config=api_config_override,
                error_cls=RestRbuxModule1.UpdateScopeError,
            )
            return parse_grpc_response(
                rest_models.UpdateScopeResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateScope,
                operation_name="UpdateScope",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestRbuxModule1.UpdateScope(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_scope(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteScopeResponse:
        """
        Delete Focus Scope

        Deletes a Focus Scope.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for rbux service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteScopeRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteScope,
                _req,
                api_config=api_config_override,
                error_cls=RestRbuxModule1.DeleteScopeError,
            )
            return parse_grpc_response(
                rest_models.DeleteScopeResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteScope,
                operation_name="DeleteScope",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestRbuxModule1.DeleteScope(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
