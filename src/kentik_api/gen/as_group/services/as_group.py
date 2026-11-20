from typing import Optional, Union, cast

import kentik_api.gen.as_group.services.ASGroupService as RestAsGroupModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.as_group import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class AsGroupServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.as_group.pb.as_group_pb2 as _pb2_1_mod
                import kentik_api.gen.as_group.pb.as_group_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.ASGroupServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListASGroupsResponse:
        """
        List all AS groups.

        Returns list of configured AS groups.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for as_group service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListASGroupsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListASGroups,
                _req,
                api_config=api_config_override,
                error_cls=RestAsGroupModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListASGroupsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListASGroups,
                operation_name="ListASGroups",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAsGroupModule1.ListASGroups(
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
        data: rest_models.CreateASGroupRequest,
    ) -> rest_models.CreateASGroupResponse:
        """
        Configure a new AS group.

        Create configuration for a new AS group. Returns the newly created configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for as_group service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateASGroupRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateASGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestAsGroupModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateASGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateASGroup,
                operation_name="CreateASGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAsGroupModule1.CreateASGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, asGroupid: str
    ) -> rest_models.GetASGroupResponse:
        """
        Retrieve configuration of a AS group.

        Returns configuration of a AS group specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for as_group service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetASGroupRequest, None, {"id": asGroupid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetASGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestAsGroupModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetASGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetASGroup,
                operation_name="GetASGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAsGroupModule1.GetASGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                asGroupid=asGroupid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        asGroupid: str,
        data: rest_models.ASGroupServiceUpdateASGroupBody,
    ) -> rest_models.UpdateASGroupResponse:
        """
        Updates configuration of a AS group.

        Replaces configuration of a AS group with attributes in the request. Returns the updated configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for as_group service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateASGroupRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"as_group.id": asGroupid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateASGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestAsGroupModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateASGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateASGroup,
                operation_name="UpdateASGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAsGroupModule1.UpdateASGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                asGroupid=asGroupid,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, asGroupid: str
    ) -> rest_models.DeleteASGroupResponse:
        """
        Delete configuration of a AS group.

        Deletes configuration of a AS group with specific ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for as_group service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteASGroupRequest, None, {"id": asGroupid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteASGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestAsGroupModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteASGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteASGroup,
                operation_name="DeleteASGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestAsGroupModule1.DeleteASGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                asGroupid=asGroupid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
