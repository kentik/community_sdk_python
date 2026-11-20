from typing import List, Optional, Union, cast

import kentik_api.gen.synthetics.services.SyntheticsAdminService as RestSyntheticsModule1
import kentik_api.gen.synthetics.services.SyntheticsBulkActionService as RestSyntheticsModule2
import kentik_api.gen.synthetics.services.SyntheticsDataService as RestSyntheticsModule3
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.synthetics import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class SyntheticsServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.synthetics.pb.bulk_action_pb2 as _pb2_1_mod
                import kentik_api.gen.synthetics.pb.bulk_action_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.SyntheticsBulkActionServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.synthetics.pb.synthetics_pb2 as _pb2_2_mod
                import kentik_api.gen.synthetics.pb.synthetics_pb2_grpc as _pb2_grpc_2_mod

                self._grpc_pb2_2 = _pb2_2_mod
                self._grpc_stub_2 = _pb2_grpc_2_mod.SyntheticsDataServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_2 = None
                self._grpc_stub_2 = None
                self._grpc_import_error_2 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.synthetics.pb.synthetics_pb2 as _pb2_3_mod
                import kentik_api.gen.synthetics.pb.synthetics_pb2_grpc as _pb2_grpc_3_mod

                self._grpc_pb2_3 = _pb2_3_mod
                self._grpc_stub_3 = _pb2_grpc_3_mod.SyntheticsAdminServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_3 = None
                self._grpc_stub_3 = None
                self._grpc_import_error_3 = exc

    def list_agent_alerts(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentIds: Optional[List[str]] = None,
    ) -> rest_models.ListAgentAlertsResponse:
        """
        List agent alert configurations

        Lists all agent alert configurations, optionally filtered by a list of agent ids.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.ListAgentAlertsRequest, None, {"agentIds": agentIds}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.ListAgentAlerts,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.ListAgentAlertsError,
            )
            return parse_grpc_response(
                rest_models.ListAgentAlertsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.ListAgentAlerts,
                operation_name="ListAgentAlerts",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.ListAgentAlerts(
                api_config_override=api_config_override or rest_transport.api_config,
                agentIds=agentIds,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_agent_alert(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateAgentAlertRequest,
    ) -> rest_models.CreateAgentAlertResponse:
        """
        Create an agent alert configuration

        Creates a new agent alert configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.CreateAgentAlertRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.CreateAgentAlert,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.CreateAgentAlertError,
            )
            return parse_grpc_response(
                rest_models.CreateAgentAlertResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.CreateAgentAlert,
                operation_name="CreateAgentAlert",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.CreateAgentAlert(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_agent_alert(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetAgentAlertResponse:
        """
        Get an agent alert configuration

        Retrieves an existing agent alert configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.GetAgentAlertRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetAgentAlert,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.GetAgentAlertError,
            )
            return parse_grpc_response(
                rest_models.GetAgentAlertResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetAgentAlert,
                operation_name="GetAgentAlert",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.GetAgentAlert(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_agent_alert(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SyntheticsAdminServiceUpdateAgentAlertBody,
    ) -> rest_models.UpdateAgentAlertResponse:
        """
        Update an agent alert configuration

        Updates an existing agent alert configuration with the time threshold and notification channels provided.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.UpdateAgentAlertRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.UpdateAgentAlert,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.UpdateAgentAlertError,
            )
            return parse_grpc_response(
                rest_models.UpdateAgentAlertResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.UpdateAgentAlert,
                operation_name="UpdateAgentAlert",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.UpdateAgentAlert(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_agent_alert(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteAgentAlertResponse:
        """
        Delete an agent alert configuration

        Deletes an existing agent alert configuration.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.DeleteAgentAlertRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.DeleteAgentAlert,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.DeleteAgentAlertError,
            )
            return parse_grpc_response(
                rest_models.DeleteAgentAlertResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.DeleteAgentAlert,
                operation_name="DeleteAgentAlert",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.DeleteAgentAlert(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_agents(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListAgentsResponse:
        """
        List available agents

        Returns list of all synthetic agents available in the account.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(self._grpc_pb2_3.ListAgentsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.ListAgents,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.ListAgentsError,
            )
            return parse_grpc_response(
                rest_models.ListAgentsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.ListAgents,
                operation_name="ListAgents",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.ListAgents(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_agent(
        self, *, api_config_override: Optional[APIConfig] = None, agentid: str
    ) -> rest_models.GetAgentResponse:
        """
        Get information about an agent

        Returns information about the requested synthetic agent.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.GetAgentRequest, None, {"id": agentid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.GetAgentError,
            )
            return parse_grpc_response(
                rest_models.GetAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetAgent,
                operation_name="GetAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.GetAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_agent(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentid: str,
        data: rest_models.SyntheticsAdminServiceUpdateAgentBody,
    ) -> rest_models.UpdateAgentResponse:
        """
        Update configuration of an agent

        Update configuration of a synthetic agent.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.UpdateAgentRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"agent.id": agentid},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.UpdateAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.UpdateAgentError,
            )
            return parse_grpc_response(
                rest_models.UpdateAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.UpdateAgent,
                operation_name="UpdateAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.UpdateAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_agent(
        self, *, api_config_override: Optional[APIConfig] = None, agentid: str
    ) -> rest_models.DeleteAgentResponse:
        """
        Delete an agent

        Deletes the requested agent. The deleted agent is removed from configuration of all tests.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.DeleteAgentRequest, None, {"id": agentid}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.DeleteAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.DeleteAgentError,
            )
            return parse_grpc_response(
                rest_models.DeleteAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.DeleteAgent,
                operation_name="DeleteAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.DeleteAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_tests(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListTestsResponse:
        """
        List all tests

        Returns a list of all configured active and paused synthetic tests.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(self._grpc_pb2_3.ListTestsRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.ListTests,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.ListTestsError,
            )
            return parse_grpc_response(
                rest_models.ListTestsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.ListTests,
                operation_name="ListTests",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.ListTests(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_test(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateTestRequest,
    ) -> rest_models.CreateTestResponse:
        """
        Create a test

        Create synthetic test based on configuration provided in the request.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.CreateTestRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.CreateTest,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.CreateTestError,
            )
            return parse_grpc_response(
                rest_models.CreateTestResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.CreateTest,
                operation_name="CreateTest",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.CreateTest(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_test(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetTestResponse:
        """
        Get information about a test

        Returns configuration and status for the requested synthetic test.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(self._grpc_pb2_3.GetTestRequest, None, {"id": id})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetTest,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.GetTestError,
            )
            return parse_grpc_response(
                rest_models.GetTestResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetTest,
                operation_name="GetTest",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.GetTest(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_test(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SyntheticsAdminServiceUpdateTestBody,
    ) -> rest_models.UpdateTestResponse:
        """
        Update configuration of a test

        Updates configuration of a synthetic test.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.UpdateTestRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"test.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.UpdateTest,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.UpdateTestError,
            )
            return parse_grpc_response(
                rest_models.UpdateTestResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.UpdateTest,
                operation_name="UpdateTest",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.UpdateTest(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_test(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteTestResponse:
        """
        Delete a synthetic test.

        Deletes the synthetics test. All accumulated results for the test cease to be accessible.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.DeleteTestRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.DeleteTest,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.DeleteTestError,
            )
            return parse_grpc_response(
                rest_models.DeleteTestResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.DeleteTest,
                operation_name="DeleteTest",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.DeleteTest(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def set_test_status(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.SyntheticsAdminServiceSetTestStatusBody,
    ) -> rest_models.SetTestStatusResponse:
        """
        Update status of a synthetic test
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.SetTestStatusRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.SetTestStatus,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule1.SetTestStatusError,
            )
            return parse_grpc_response(
                rest_models.SetTestStatusResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.SetTestStatus,
                operation_name="SetTestStatus",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule1.SetTestStatus(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def bulk_update_tests(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.BulkUpdateTestsRequest,
    ) -> rest_models.BulkUpdateTestsResponse:
        """
        Update multiple synthetic tests

        Applies the same attribute changes to up to 50 synthetic tests. Only some attributes can be bulk-updated, and some can be changed only on certain test types or only together with another attribute. Tests are validated first; by default, if any test fails validation no test is updated (see `allow_partial_batch`). Tests that pass are then updated asynchronously: the reply carries the initial status and, if anything was started, a `workflow_id` to pass to GetBulkUpdateTestsStatus. Fails with INVALID_ARGUMENT (HTTP 400) if the request is malformed, such as no IDs, more than 50 IDs, no attributes to update, an attribute that cannot be bulk-updated, or an attribute that does not apply to every selected test's type; RESOURCE_EXHAUSTED (HTTP 429) if the company lacks the synthetics credits for the change; and UNKNOWN (HTTP 500) if the update could not be confirmed as started. After UNKNOWN the update may still run, so check the tests before retrying.

        ### Bulk-updatable attributes
        Paths are relative to `test` and shown in JSON (camelCase) form. snake_case is also accepted, and error messages report paths in snake_case.

        | Path | Notes |
        |------|-------|
        | `name` | |
        | `status` | `TEST_STATUS_ACTIVE` or `TEST_STATUS_PAUSED` |
        | `settings.period` | |
        | `settings.agentIds` | supports ADD and REMOVE |
        | `settings.healthSettings.activation.times` | |
        | `settings.healthSettings.activation.timeWindow` | |
        | `settings.healthSettings.activation.gracePeriod` | |
        | `settings.healthSettings.latencyCritical`, `latencyWarning` | set together |
        | `settings.healthSettings.latencyCriticalStddev`, `latencyWarningStddev` | set together; also sets `latencyCritical` and `latencyWarning` to 0 |
        | `settings.healthSettings.jitterCritical`, `jitterWarning` | set together |
        | `settings.healthSettings.jitterCriticalStddev`, `jitterWarningStddev` | set together; also sets `jitterCritical` and `jitterWarning` to 0 |
        | `settings.healthSettings.packetLossCritical`, `packetLossWarning` | set together |
        | `settings.ip.targets` | supports ADD and REMOVE |
        | `settings.networkGrid.targets` | supports ADD and REMOVE |
        | `settings.dns.servers` | supports ADD and REMOVE |
        | `settings.dns.target` | |
        | `settings.dnsGrid.servers` | supports ADD and REMOVE |
        | `settings.dnsGrid.target` | |
        | `settings.hostname.target` | |
        | `settings.url.target` | |
        | `settings.pageLoad.target` | |
        | `settings.agent.target` | |

        A threshold pair and its Stddev pair cannot be set in the same request.

        ### Examples
        Change the period of several tests:
        ```json
        {"ids": ["101", "102"], "test": {"settings": {"period": 300}}}
        ```
        Add an agent to each test, keeping the agents already assigned. In JSON, a field mask is a single comma-separated string:
        ```json
        {"ids": ["101", "102"], "test": {"settings": {"agentIds": ["55"]}},
        "ops": [{"mask": "settings.agentIds", "op": "BULK_FIELD_OP_ADD"}]}
        ```
        Set attributes to zero. A zero value cannot be told apart from an unset one, so `mask` must name it:
        ```json
        {"ids": ["101"], "test": {"settings": {"healthSettings": {"jitterCritical": 0, "jitterWarning": 0}}},
        "mask": "settings.healthSettings.jitterCritical,settings.healthSettings.jitterWarning"}
        ```
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.BulkUpdateTestsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.BulkUpdateTests,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule2.BulkUpdateTestsError,
            )
            return parse_grpc_response(
                rest_models.BulkUpdateTestsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.BulkUpdateTests,
                operation_name="BulkUpdateTests",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule2.BulkUpdateTests(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_bulk_update_tests_status(
        self, *, api_config_override: Optional[APIConfig] = None, workflowId: str
    ) -> rest_models.GetBulkUpdateTestsStatusResponse:
        """
        Get status of a bulk test update

        Returns the current state and per-test outcome of a bulk update started by BulkUpdateTests. When `end_time` is set, the bulk update has finished and its status will not change. Items skipped before the update started are reported only in the BulkUpdateTests reply. Status is kept for a limited time after a bulk update finishes, so read it soon after `end_time` is set. Fails with NOT_FOUND (HTTP 404) if the workflow ID is unknown, the bulk update was started by a different user, or its status is no longer kept.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetBulkUpdateTestsStatusRequest,
                None,
                {"workflow_id": workflowId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetBulkUpdateTestsStatus,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule2.GetBulkUpdateTestsStatusError,
            )
            return parse_grpc_response(
                rest_models.GetBulkUpdateTestsStatusResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetBulkUpdateTestsStatus,
                operation_name="GetBulkUpdateTestsStatus",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule2.GetBulkUpdateTestsStatus(
                api_config_override=api_config_override or rest_transport.api_config,
                workflowId=workflowId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_results_for_tests(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GetResultsForTestsRequest,
    ) -> rest_models.GetResultsForTestsResponse:
        """
        Get results for tests

        Returns probe results for a set of tests for specified period of time.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetResultsForTestsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetResultsForTests,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule3.GetResultsForTestsError,
            )
            return parse_grpc_response(
                rest_models.GetResultsForTestsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetResultsForTests,
                operation_name="GetResultsForTests",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule3.GetResultsForTests(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_results_for_tests_csv(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GetResultsForTestsCsvRequest,
    ) -> rest_models.GetResultsForTestsCsvResponse:
        """
        Get test results in CSV format

        Returns probe results for tests in CSV format.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetResultsForTestsCsvRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetResultsForTestsCsv,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule3.GetResultsForTestsCsvError,
            )
            return parse_grpc_response(
                rest_models.GetResultsForTestsCsvResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetResultsForTestsCsv,
                operation_name="GetResultsForTestsCsv",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule3.GetResultsForTestsCsv(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_trace_for_test(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GetTraceForTestRequest,
    ) -> rest_models.GetTraceForTestResponse:
        """
        Get network trace data for a test

        Get network trace data for a specific synthetic test. The test must have traceroute task configured.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for synthetics service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetTraceForTestRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetTraceForTest,
                _req,
                api_config=api_config_override,
                error_cls=RestSyntheticsModule3.GetTraceForTestError,
            )
            return parse_grpc_response(
                rest_models.GetTraceForTestResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetTraceForTest,
                operation_name="GetTraceForTest",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestSyntheticsModule3.GetTraceForTest(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
