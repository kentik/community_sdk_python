from typing import Optional, Union, cast

import kentik_api.gen.capacity_plan.services.CapacityPlanService as RestCapacityPlanModule1
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.capacity_plan import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class CapacityPlanServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.capacity_plan.pb.capacity_plan_pb2 as _pb2_1_mod
                import kentik_api.gen.capacity_plan.pb.capacity_plan_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.CapacityPlanServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc

    def list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCapacityPlansResponse:
        """
        List all capacity plans.

        Returns list of capacity plans.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for capacity_plan service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCapacityPlansRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCapacityPlans,
                _req,
                api_config=api_config_override,
                error_cls=RestCapacityPlanModule1.ListError,
            )
            return parse_grpc_response(
                rest_models.ListCapacityPlansResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCapacityPlans,
                operation_name="ListCapacityPlans",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCapacityPlanModule1.ListCapacityPlans(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_capacity_summaries(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCapacitySummariesResponse:
        """
        List all capacity summaries.

        Returns list of capacity summaries.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for capacity_plan service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListCapacitySummariesRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListCapacitySummaries,
                _req,
                api_config=api_config_override,
                error_cls=RestCapacityPlanModule1.ListCapacitySummariesError,
            )
            return parse_grpc_response(
                rest_models.ListCapacitySummariesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListCapacitySummaries,
                operation_name="ListCapacitySummaries",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCapacityPlanModule1.ListCapacitySummaries(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetCapacityPlanResponse:
        """
        Retrieve capacity plan.

        Returns capacity plan specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for capacity_plan service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCapacityPlanRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCapacityPlan,
                _req,
                api_config=api_config_override,
                error_cls=RestCapacityPlanModule1.GetError,
            )
            return parse_grpc_response(
                rest_models.GetCapacityPlanResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCapacityPlan,
                operation_name="GetCapacityPlan",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCapacityPlanModule1.GetCapacityPlan(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_capacity_summary(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetCapacitySummaryResponse:
        """
        Retrieve capacity plan summary.

        Returns capacity plan summary specified by ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for capacity_plan service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetCapacitySummaryRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetCapacitySummary,
                _req,
                api_config=api_config_override,
                error_cls=RestCapacityPlanModule1.GetCapacitySummaryError,
            )
            return parse_grpc_response(
                rest_models.GetCapacitySummaryResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetCapacitySummary,
                operation_name="GetCapacitySummary",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestCapacityPlanModule1.GetCapacitySummary(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
