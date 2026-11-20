from typing import Optional, Union, cast

import kentik_api.gen.credential.services.CredentialService as RestCredentialModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.credential import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CredentialServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.credential.pb.credential_pb2 as _pb2_1_mod
                import kentik_api.gen.credential.pb.credential_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CredentialServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCredentialsResponse:
        """
        List credentials.

        Returns the latest version of every credential.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListCredentialsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCredentials,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListCredentialsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCredentials,
                operation_name="ListCredentials",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.ListCredentials(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        name: str,
        version: Optional[int] = None,
        allVersions: Optional[bool] = None,
    ) -> rest_models.GetCredentialResponse:
        """
        Get a credential by name.

        Returns the latest, a specific, or every version of a credential.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCredentialRequest,
                None,
                {"name": name, "version": version, "allVersions": allVersions},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCredential,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetCredentialResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCredential,
                operation_name="GetCredential",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.GetCredential(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
                version=version,
                allVersions=allVersions,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        name: str,
        version: int,
    ) -> rest_models.DeleteCredentialResponse:
        """
        Delete a credential version.

        Deletes a single version of a credential. Version Requires. Fails if the credential has consumers.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteCredentialRequest,
                None,
                {"name": name, "version": version},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteCredential,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteCredentialResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteCredential,
                operation_name="DeleteCredential",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.DeleteCredential(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
                version=version,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def assign_consumer(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        name: str,
        data: rest_models.CredentialServiceAssignConsumerBody,
    ) -> rest_models.AssignConsumerResponse:
        """
        Assign a consumer to a credential.

        Records that an entity (synthetic test, device, etc.) uses the credential.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.AssignConsumerRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"name": name},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.AssignConsumer,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.AssignConsumerError,
            )
            return parse_grpc_response(
                rest_models.AssignConsumerResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.AssignConsumer,
                operation_name="AssignConsumer",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.AssignConsumer(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_group(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCredentialGroupResponse:
        """
        List credential groups.

        Returns every credential group with the latest version of its credentials.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCredentialGroupsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCredentialGroups,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.ListGroupError,
            )
            return parse_grpc_response(
                rest_models.ListCredentialGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCredentialGroups,
                operation_name="ListCredentialGroups",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.ListCredentialGroups(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_group(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateCredentialGroupRequest,
    ) -> rest_models.CreateCredentialGroupResponse:
        """
        Create a credential group.

        Creates one credential per token and returns the created group.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateCredentialGroupRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateCredentialGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.CreateGroupError,
            )
            return parse_grpc_response(
                rest_models.CreateCredentialGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateCredentialGroup,
                operation_name="CreateCredentialGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.CreateCredentialGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_group(
        self, *, api_config_override: Optional[APIConfig] = None, name: str
    ) -> rest_models.GetCredentialGroupResponse:
        """
        Get a credential group by name.

        Returns a single credential group.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCredentialGroupRequest, None, {"name": name}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCredentialGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.GetGroupError,
            )
            return parse_grpc_response(
                rest_models.GetCredentialGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCredentialGroup,
                operation_name="GetCredentialGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.GetCredentialGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_group(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        name: str,
        data: rest_models.CredentialServiceUpdateCredentialGroupBody,
    ) -> rest_models.UpdateCredentialGroupResponse:
        """
        Update a credential group.

        Tokens with a value create a new credential version; tokens without one only update metadata.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateCredentialGroupRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"name": name},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateCredentialGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.UpdateGroupError,
            )
            return parse_grpc_response(
                rest_models.UpdateCredentialGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateCredentialGroup,
                operation_name="UpdateCredentialGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.UpdateCredentialGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_group(
        self, *, api_config_override: Optional[APIConfig] = None, name: str
    ) -> rest_models.DeleteCredentialGroupResponse:
        """
        Delete a credential group.

        Deletes every version of every credential in the group. Fails if any credential has consumers.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteCredentialGroupRequest, None, {"name": name}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteCredentialGroup,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.DeleteGroupError,
            )
            return parse_grpc_response(
                rest_models.DeleteCredentialGroupResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteCredentialGroup,
                operation_name="DeleteCredentialGroup",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.DeleteCredentialGroup(
                api_config_override=api_config_override or rest_transport.api_config,
                name=name,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_overviews(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCredentialOverviewsResponse:
        """
        List credential group names and types.

        Returns a lightweight name and type listing of every credential group, for lookups.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for credential service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCredentialOverviewsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCredentialOverviews,
                _req,
                api_config=api_config_override,
                error_cls=RestCredentialModule1.ListOverviewsError,
            )
            return parse_grpc_response(
                rest_models.ListCredentialOverviewsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCredentialOverviews,
                operation_name="ListCredentialOverviews",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCredentialModule1.ListCredentialOverviews(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
