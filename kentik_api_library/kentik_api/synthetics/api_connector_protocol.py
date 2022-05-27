from typing import List, Optional

from google.protobuf.timestamp_pb2 import Timestamp
from typing_extensions import Protocol

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb


class APISyntheticsConnectorProtocol(Protocol):
    def get_all_agents(self) -> List[pb.Agent]:
        pass

    def get_agent(self, agent_id: str) -> pb.Agent:
        pass

    def update_agent(self, agent: pb.Agent) -> pb.Agent:
        pass

    def delete_agent(self, agent_id: str) -> None:
        pass

    def get_all_tests(self) -> List[pb.Test]:
        pass

    def get_test(self, test_id: str) -> pb.Test:
        pass

    def create_test(self, test: pb.Test) -> pb.Test:
        pass

    def update_test(self, test: pb.Test) -> pb.Test:
        pass

    def delete_test(self, test_id: str) -> None:
        pass

    def test_status_update(self, test_id: str, status: pb.TestStatus) -> None:
        pass

    def results_for_tests(
        self,
        test_ids: List[str],
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        task_ids: Optional[List[str]] = None,
    ) -> pb.GetResultsForTestsResponse:
        pass

    def trace_for_test(
        self,
        test_id: str,
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        target_ips: Optional[List[str]] = None,
    ) -> pb.GetTraceForTestResponse:
        pass
