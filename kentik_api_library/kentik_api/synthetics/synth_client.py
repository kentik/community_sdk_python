import logging
from datetime import datetime
from typing import Any, List, Optional

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.errors import KentikAPIError
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.agent import Agent, AgentOwnershipType
from kentik_api.synthetics.api_connector_protocol import APISyntheticsConnectorProtocol
from kentik_api.synthetics.synth_tests import (
    AgentTest,
    DNSGridTest,
    DNSTest,
    FlowTest,
    HostnameTest,
    IPTest,
    NetworkGridTest,
    NetworkMeshTest,
    PageLoadTest,
    SynTest,
    TestResults,
    TraceResponse,
    UrlTest,
)
from kentik_api.synthetics.synth_tests.base import DateTime
from kentik_api.synthetics.types import TestStatus, TestType

log = logging.getLogger("synth_tests")


class KentikSynthClient:
    IGNORED_TEST_TYPES = [TestType.BGP_MONITOR.value, TestType.TRANSACTION.value]

    def __init__(self, connector: APISyntheticsConnectorProtocol):
        self._connector = connector

    def get_all_agents(self, private_only=False) -> List[Agent]:
        pb_agents = self._connector.get_all_agents()
        return [Agent.from_pb(agent) for agent in pb_agents if not private_only or agent.type == "private"]

    def get_agent(self, agent_id: ID) -> Agent:
        pb_agent = self._connector.get_agent(str(agent_id))
        return Agent.from_pb(pb_agent)

    def update_agent(self, agent: Agent) -> Agent:
        if agent.type != AgentOwnershipType.PRIVATE:
            raise KentikAPIError("Only agents of type 'private' can be modified")
        pb_input_agent = agent.to_pb()
        pb_output_agent = self._connector.update_agent(pb_input_agent)
        return Agent.from_pb(pb_output_agent)

    def delete_agent(self, agent_id: ID) -> None:
        self._connector.delete_agent(str(agent_id))

    def get_all_tests(self) -> List[SynTest]:
        pb_tests = self._connector.get_all_tests()
        return [make_synth_test(pb_test) for pb_test in pb_tests if str(pb_test.type) not in self.IGNORED_TEST_TYPES]

    def get_test(self, test_id: ID) -> SynTest:
        pb_test = self._connector.get_test(str(test_id))
        if str(pb_test.type) in self.IGNORED_TEST_TYPES:
            raise KentikAPIError(f"Unsupported test type: {str(pb_test.type)}")

        return make_synth_test(pb_test)

    def create_test(self, test: SynTest) -> SynTest:
        pb_input_test = test.to_pb()
        pb_output_test = self._connector.create_test(pb_input_test)
        return make_synth_test(pb_output_test)

    def update_test(self, test: SynTest) -> SynTest:
        pb_input_test = test.to_pb()
        pb_output_test = self._connector.update_test(pb_input_test)
        return make_synth_test(pb_output_test)

    def delete_test(self, test_id: ID) -> None:
        self._connector.delete_test(str(test_id))

    def set_test_status(self, test_id: ID, status: TestStatus) -> None:
        self._connector.test_status_update(str(test_id), status.value)

    def results_for_tests(
        self,
        test_ids: List[ID],
        start: datetime,
        end: datetime,
        agent_ids: Optional[List[ID]] = None,
        task_ids: Optional[List[ID]] = None,
    ) -> List[TestResults]:
        ids = [str(id) for id in test_ids]
        agents = [str(id) for id in agent_ids] if agent_ids else []
        tasks = [str(id) for id in task_ids] if task_ids else []
        response = self._connector.results_for_tests(
            test_ids=ids,
            start=DateTime.fromtimestamp(start.timestamp(), start.tzinfo).to_pb(),
            end=DateTime.fromtimestamp(end.timestamp(), end.tzinfo).to_pb(),
            agent_ids=agents,
            task_ids=tasks,
        )
        return [TestResults.from_pb(tr) for tr in response.results]

    def trace_for_test(
        self,
        test_id: ID,
        start: datetime,
        end: datetime,
        agent_ids: Optional[List[ID]] = None,
        target_ips: Optional[List[IP]] = None,
    ) -> TraceResponse:
        agents = [str(id) for id in agent_ids] if agent_ids else []
        targets = [str(ip) for ip in target_ips] if target_ips else []
        response = self._connector.trace_for_test(
            test_id=str(test_id),
            start=DateTime.fromtimestamp(start.timestamp(), start.tzinfo).to_pb(),
            end=DateTime.fromtimestamp(end.timestamp(), end.tzinfo).to_pb(),
            agent_ids=agents,
            target_ips=targets,
        )
        return TraceResponse.from_pb(response)


def make_synth_test(pb_object: pb.Test) -> SynTest:
    def _cls_from_type(test_type: TestType) -> Any:
        return {
            TestType.IP: IPTest,
            TestType.AGENT: AgentTest,
            TestType.HOSTNAME: HostnameTest,
            TestType.URL: UrlTest,
            TestType.DNS: DNSTest,
            TestType.DNS_GRID: DNSGridTest,
            TestType.NETWORK_MESH: NetworkMeshTest,
            TestType.NETWORK_GRID: NetworkGridTest,
            TestType.PAGE_LOAD: PageLoadTest,
            TestType.FLOW: FlowTest,
        }.get(test_type)

    test_type = str(pb_object.type)
    cls = _cls_from_type(TestType(test_type))
    if cls is None:
        raise KentikAPIError(f"Unsupported test type: {test_type}")
    return cls.from_pb(pb_object)
