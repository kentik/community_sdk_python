from typing import Any, List, Optional, Tuple

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2_grpc import (
    SyntheticsAdminService,
    SyntheticsDataService,
)
from kentik_api.internal.grpc import wrap_grpc_errors
from kentik_api.version import get_user_agent


class APISyntheticsConnector:
    """
    APISyntheticsConnector implements APISyntheticsConnectorProtocol.
    Allows sending authorized gRPC requests to Kentik Synthetics API
    """

    def __init__(
        self,
        api_url: str,
        auth_email: str,
        auth_token: str,
        options: List[Tuple[str, Any]] = [],
    ):
        self._url = api_url
        self._options = tuple(options)
        self._admin = SyntheticsAdminService()
        self._data = SyntheticsDataService()
        self._metadata = [
            ("x-ch-auth-email", auth_email),
            ("x-ch-auth-api-token", auth_token),
            ("user-agent", get_user_agent()),
        ]

    @wrap_grpc_errors
    def get_all_agents(self) -> List[pb.Agent]:
        request = pb.ListAgentsRequest()
        agents = self._admin.ListAgents(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).agents
        return list(agents)

    @wrap_grpc_errors
    def get_agent(self, agent_id: str) -> pb.Agent:
        request = pb.GetAgentRequest(id=agent_id)
        return self._admin.GetAgent(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).agent

    @wrap_grpc_errors
    def update_agent(self, agent: pb.Agent) -> pb.Agent:
        request = pb.UpdateAgentRequest(agent=agent)
        return self._admin.UpdateAgent(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).agent

    @wrap_grpc_errors
    def delete_agent(self, agent_id: str) -> None:
        request = pb.DeleteAgentRequest(id=agent_id)
        self._admin.DeleteAgent(request=request, metadata=self._metadata, target=self._url, options=self._options)

    @wrap_grpc_errors
    def get_all_tests(self) -> List[pb.Test]:
        request = pb.ListTestsRequest()
        tests = self._admin.ListTests(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).tests
        return list(tests)

    @wrap_grpc_errors
    def get_test(self, test_id: str) -> pb.Test:
        request = pb.GetTestRequest(id=test_id)
        return self._admin.GetTest(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).test

    @wrap_grpc_errors
    def create_test(self, test: pb.Test) -> pb.Test:
        test.ClearField("id")  # CreateTestRequest doesn't accept id
        request = pb.CreateTestRequest(test=test)
        return self._admin.CreateTest(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).test

    @wrap_grpc_errors
    def update_test(self, test: pb.Test) -> pb.Test:
        request = pb.UpdateTestRequest(test=test)
        return self._admin.UpdateTest(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        ).test

    @wrap_grpc_errors
    def delete_test(self, test_id: str) -> None:
        request = pb.DeleteTestRequest(id=test_id)
        self._admin.DeleteTest(request=request, metadata=self._metadata, target=self._url, options=self._options)

    @wrap_grpc_errors
    def test_status_update(self, test_id: str, status: pb.TestStatus) -> None:
        request = pb.SetTestStatusRequest(id=test_id, status=status)
        self._admin.SetTestStatus(request=request, metadata=self._metadata, target=self._url, options=self._options)

    @wrap_grpc_errors
    def results_for_tests(
        self,
        test_ids: List[str],
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        task_ids: Optional[List[str]] = None,
    ) -> pb.GetResultsForTestsResponse:
        request = pb.GetResultsForTestsRequest(
            ids=test_ids,
            start_time=start,
            end_time=end,
            agent_ids=agent_ids or [],
            targets=task_ids or [],
        )
        return self._data.GetResultsForTests(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        )

    @wrap_grpc_errors
    def trace_for_test(
        self,
        test_id: str,
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        target_ips: Optional[List[str]] = None,
    ) -> pb.GetTraceForTestResponse:
        request = pb.GetTraceForTestRequest(
            id=test_id,
            start_time=start,
            end_time=end,
            agent_ids=agent_ids or [],
            target_ips=target_ips or [],
        )
        return self._data.GetTraceForTest(
            request=request, metadata=self._metadata, target=self._url, options=self._options
        )
