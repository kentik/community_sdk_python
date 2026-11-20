from typing import Optional, Union, cast

import kentik_api.gen.custom_application.services.CustomApplicationService as RestCustomApplicationModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.custom_application import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CustomApplicationServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.custom_application.pb.custom_application_pb2 as _pb2_1_mod
                import kentik_api.gen.custom_application.pb.custom_application_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CustomApplicationServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCustomApplicationsResponse:
        """
        List Custom Applications

        Returns an array of custom application objects that each contain information about an individual custom application.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_application service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCustomApplicationsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCustomApplications,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomApplicationModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListCustomApplicationsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCustomApplications,
                operation_name="ListCustomApplications",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomApplicationModule1.ListCustomApplications(
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
        data: rest_models.CustomApplication,
    ) -> rest_models.CreateCustomApplicationResponse:
        """
        Create Custom Application

        Creates and returns a custom application object containing information about an individual custom application.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_application service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateCustomApplicationRequest,
                {"application": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateCustomApplication,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomApplicationModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateCustomApplicationResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateCustomApplication,
                operation_name="CreateCustomApplication",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomApplicationModule1.CreateCustomApplication(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customApplicationId: str,
    ) -> rest_models.GetCustomApplicationResponse:
        """
        Custom Application Info

        Returns a custom application object containing information about an individual custom application.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_application service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCustomApplicationRequest,
                None,
                {"custom_application_id": customApplicationId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCustomApplication,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomApplicationModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetCustomApplicationResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCustomApplication,
                operation_name="GetCustomApplication",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomApplicationModule1.GetCustomApplication(
                api_config_override=api_config_override or rest_transport.api_config,
                customApplicationId=customApplicationId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customApplicationId: str,
        data: rest_models.CustomApplication,
    ) -> rest_models.UpdateCustomApplicationResponse:
        """
        Update Custom Application

        Updates and returns a custom application object containing information about an individual custom application.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_application service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateCustomApplicationRequest,
                {"application": data.model_dump(by_alias=True, exclude_unset=True)},
                {"custom_application_id": customApplicationId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateCustomApplication,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomApplicationModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateCustomApplicationResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateCustomApplication,
                operation_name="UpdateCustomApplication",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomApplicationModule1.UpdateCustomApplication(
                api_config_override=api_config_override or rest_transport.api_config,
                customApplicationId=customApplicationId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customApplicationId: str,
    ) -> rest_models.DeleteCustomApplicationResponse:
        """
        Delete Custom Application

        Deletes a custom application.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_application service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteCustomApplicationRequest,
                None,
                {"custom_application_id": customApplicationId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteCustomApplication,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomApplicationModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteCustomApplicationResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteCustomApplication,
                operation_name="DeleteCustomApplication",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomApplicationModule1.DeleteCustomApplication(
                api_config_override=api_config_override or rest_transport.api_config,
                customApplicationId=customApplicationId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
