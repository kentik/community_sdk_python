from typing import Optional, Union, cast

import kentik_api.gen.user.services.UserService as RestUserModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.user import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class UserServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.user.pb.user_pb2 as _pb2_1_mod
                import kentik_api.gen.user.pb.user_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.UserServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListUsersResponse:
        """
        List all users.

        Returns a list of all user accounts in the company.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListUsersRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListUsers,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListUsersResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListUsers,
                operation_name="ListUsers",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.ListUsers(
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
        data: rest_models.CreateUserRequest,
    ) -> rest_models.CreateUserResponse:
        """
        Create new user account.

        Creates new user account based on attributes in the request. Returns attributes of the newly created account.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateUserRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateUser,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateUser,
                operation_name="CreateUser",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.CreateUser(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetUserResponse:
        """
        Get attributes of a user account.

        Returns attributes of a user account specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.GetUserRequest, None, {"id": id})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetUser,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetUser,
                operation_name="GetUser",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.GetUser(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.UserServiceUpdateUserBody,
    ) -> rest_models.UpdateUserResponse:
        """
        Update attributes of a user account.

        Replaces all attributes of a user account specified by ID with attributes in the request. Returns updated attributes.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateUserRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"user.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateUser,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateUser,
                operation_name="UpdateUser",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.UpdateUser(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteUserResponse:
        """
        Delete a user account.

        Deletes user account specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteUserRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteUser,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteUser,
                operation_name="DeleteUser",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.DeleteUser(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def reset_active_sessions(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.ResetActiveSessionsResponse:
        """
        Resets active sessions for a user.

        Resets active sessions for a user specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ResetActiveSessionsRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ResetActiveSessions,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.ResetActiveSessionsError,
            )
            return parse_grpc_response(
                rest_models.ResetActiveSessionsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ResetActiveSessions,
                operation_name="ResetActiveSessions",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.ResetActiveSessions(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def reset_api_token(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.ResetApiTokenResponse:
        """
        Reset API token for a user.

        Resets API token for a user specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for user service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ResetApiTokenRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ResetApiToken,
                _req,
                api_config=api_config_override,
                error_cls=RestUserModule1.ResetApiTokenError,
            )
            return parse_grpc_response(
                rest_models.ResetApiTokenResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ResetApiToken,
                operation_name="ResetApiToken",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestUserModule1.ResetApiToken(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
