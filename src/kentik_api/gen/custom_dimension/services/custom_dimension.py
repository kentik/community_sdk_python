from typing import Optional, Union, cast

import kentik_api.gen.custom_dimension.services.CustomDimensionService as RestCustomDimensionModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.custom_dimension import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CustomDimensionServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.custom_dimension.pb.custom_dimension_pb2 as _pb2_1_mod
                import kentik_api.gen.custom_dimension.pb.custom_dimension_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CustomDimensionServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCustomDimensionsResponse:
        """
        List Custom Dimensions

        Returns an array of custom dimension objects that each contain information about an individual custom dimension.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCustomDimensionsRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCustomDimensions,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListCustomDimensionsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCustomDimensions,
                operation_name="ListCustomDimensions",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.ListCustomDimensions(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_info(
        self, *, api_config_override: Optional[APIConfig] = None, customDimensionId: str
    ) -> rest_models.GetCustomDimensionInfoResponse:
        """
        Custom Dimension Info

        Returns a custom dimension object containing information about an individual custom dimension.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCustomDimensionInfoRequest,
                None,
                {"custom_dimension_id": customDimensionId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCustomDimensionInfo,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.GetInfoError,
            )
            return parse_grpc_response(
                rest_models.GetCustomDimensionInfoResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCustomDimensionInfo,
                operation_name="GetCustomDimensionInfo",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.GetCustomDimensionInfo(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        data: rest_models.CustomDimension,
    ) -> rest_models.UpdateCustomDimensionResponse:
        """
        Update Custom Dimension

        Updates and returns a custom dimension object containing information about an individual custom dimension (see About Custom Dimensions). Populators are not sent back in the response body. To get them use 'Custom Dimension info' API instead.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdateCustomDimensionRequest,
                {"dimension": data.model_dump(by_alias=True, exclude_unset=True)},
                {"custom_dimension_id": customDimensionId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdateCustomDimension,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.UpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateCustomDimensionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdateCustomDimension,
                operation_name="UpdateCustomDimension",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.UpdateCustomDimension(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete(
        self, *, api_config_override: Optional[APIConfig] = None, customDimensionId: str
    ) -> rest_models.DeleteCustomDimensionResponse:
        """
        Delete Custom Dimension

        Deletes a custom dimension.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteCustomDimensionRequest,
                None,
                {"custom_dimension_id": customDimensionId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteCustomDimension,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.DeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteCustomDimensionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteCustomDimension,
                operation_name="DeleteCustomDimension",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.DeleteCustomDimension(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_populator(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        data: rest_models.Populator,
    ) -> rest_models.CreatePopulatorResponse:
        """
        Create Populator

        Creates and returns a populator object containing information about an individual populator.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreatePopulatorRequest,
                {"populator": data.model_dump(by_alias=True, exclude_unset=True)},
                {"custom_dimension_id": customDimensionId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreatePopulator,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.CreatePopulatorError,
            )
            return parse_grpc_response(
                rest_models.CreatePopulatorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreatePopulator,
                operation_name="CreatePopulator",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.CreatePopulator(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_populator(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        populatorId: str,
        fieldLimit: Optional[int] = None,
    ) -> rest_models.GetPopulatorResponse:
        """
        Get Populator

        Get Populator by Dimension and Populator ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetPopulatorRequest,
                None,
                {
                    "custom_dimension_id": customDimensionId,
                    "populator_id": populatorId,
                    "fieldLimit": fieldLimit,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetPopulator,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.GetPopulatorError,
            )
            return parse_grpc_response(
                rest_models.GetPopulatorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetPopulator,
                operation_name="GetPopulator",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.GetPopulator(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                populatorId=populatorId,
                fieldLimit=fieldLimit,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_populator(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        populatorId: str,
        data: rest_models.Populator,
    ) -> rest_models.UpdatePopulatorResponse:
        """
        Update Populator

        Updates and returns a populator object containing information about an individual populator.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdatePopulatorRequest,
                {"populator": data.model_dump(by_alias=True, exclude_unset=True)},
                {"custom_dimension_id": customDimensionId, "populator_id": populatorId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdatePopulator,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.UpdatePopulatorError,
            )
            return parse_grpc_response(
                rest_models.UpdatePopulatorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdatePopulator,
                operation_name="UpdatePopulator",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.UpdatePopulator(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                populatorId=populatorId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_populator(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        populatorId: str,
    ) -> rest_models.DeletePopulatorResponse:
        """
        Delete Populator

        Deletes a populator.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeletePopulatorRequest,
                None,
                {"custom_dimension_id": customDimensionId, "populator_id": populatorId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeletePopulator,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.DeletePopulatorError,
            )
            return parse_grpc_response(
                rest_models.DeletePopulatorResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeletePopulator,
                operation_name="DeletePopulator",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.DeletePopulator(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                populatorId=populatorId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_populator_field(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        customDimensionId: str,
        populatorId: str,
        fieldName: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> rest_models.GetPopulatorFieldResponse:
        """
        Get Populator Field

        Get Populator field by Dimension, Populator ID, and field name.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetPopulatorFieldRequest,
                None,
                {
                    "custom_dimension_id": customDimensionId,
                    "populator_id": populatorId,
                    "field_name": fieldName,
                    "offset": offset,
                    "limit": limit,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetPopulatorField,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.GetPopulatorFieldError,
            )
            return parse_grpc_response(
                rest_models.GetPopulatorFieldResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetPopulatorField,
                operation_name="GetPopulatorField",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.GetPopulatorField(
                api_config_override=api_config_override or rest_transport.api_config,
                customDimensionId=customDimensionId,
                populatorId=populatorId,
                fieldName=fieldName,
                offset=offset,
                limit=limit,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CustomDimension,
    ) -> rest_models.CreateCustomDimensionResponse:
        """
        Create Custom Dimension

        Creates and returns a custom dimension object containing information about an individual custom dimension
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for custom_dimension service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreateCustomDimensionRequest,
                {"dimension": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreateCustomDimension,
                _req,
                api_config=api_config_override,
                error_cls=RestCustomDimensionModule1.CreateError,
            )
            return parse_grpc_response(
                rest_models.CreateCustomDimensionResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreateCustomDimension,
                operation_name="CreateCustomDimension",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCustomDimensionModule1.CreateCustomDimension(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
