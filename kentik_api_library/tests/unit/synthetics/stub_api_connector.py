from typing import List, Optional, Union

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb

# This class implements APISyntheticsConnectorProtocol protocol, but doesn't use most of it's arguments
# pragma pylint: disable=unused-argument


class StubAPISyntheticsConnector:
    """
    StubAPISyntheticsConnector implements APISyntheticsConnectorProtocol.
    Allows for recording the requests and returning stubbed API responses.
    """

    def __init__(
        self,
        agents_response: Union[pb.Agent, List[pb.Agent], None] = None,
        tests_response: Union[pb.Test, List[pb.Test], None] = None,
        results_response: pb.GetResultsForTestsResponse = pb.GetResultsForTestsResponse(),
        traces_response: pb.GetTraceForTestResponse = pb.GetTraceForTestResponse(),
    ):
        self._agents_response = agents_response if isinstance(agents_response, list) else [agents_response]
        self._tests_response = tests_response if isinstance(tests_response, list) else [tests_response]
        self._results_response = results_response
        self._traces_response = traces_response
        self.last_payload: Union[pb.Test, pb.Agent, None] = None

    def get_all_agents(self) -> List[pb.Agent]:
        return self._agents_response

    def get_agent(self, agent_id: str) -> pb.Agent:
        return self._agents_response.pop(0)

    def update_agent(self, agent: pb.Agent) -> pb.Agent:
        self.last_payload = agent
        return agent

    def delete_agent(self, agent_id: str) -> None:
        pass

    def get_all_tests(self) -> List[pb.Test]:
        return self._tests_response

    def get_test(self, test_id: str) -> pb.Test:
        return self._tests_response.pop(0)

    def create_test(self, test: pb.Test) -> pb.Test:
        self.last_payload = test
        return test

    def delete_test(self, test_id: str) -> None:
        pass

    def test_status_update(self, test_id: str, status: pb.TestStatus) -> None:
        pass

    def update_test(self, test: pb.Test) -> pb.Test:
        self.last_payload = test
        return test

    def results_for_tests(
        self,
        test_ids: List[str],
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        task_ids: Optional[List[str]] = None,
    ) -> pb.GetResultsForTestsResponse:
        return self._results_response

    def trace_for_test(
        self,
        test_id: str,
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        target_ips: Optional[List[str]] = None,
    ) -> pb.GetTraceForTestResponse:
        return self._traces_response


# pragma pylint: enable=unused-argument
