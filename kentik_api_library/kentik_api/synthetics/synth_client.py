import logging
from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional, Tuple, Type, Union
from urllib.parse import urlparse

from kentik_api.public.types import ID

from .agent import Agent
from .api_transport_grpc import SynthGRPCTransport
from .synth_tests import SynTest, TestStatus

log = logging.getLogger("synth_client")


class KentikSynthClient:
    def __init__(self, credentials: Tuple[str, str], url: str = "https://synthetics.api.kentik.com"):
        self._transport = SynthGRPCTransport(credentials=credentials, url=url)

    @property
    def agents(self) -> List[Agent]:
        return self._transport.req("AgentsList")

    def agent(self, agent_id: ID) -> Agent:
        return self._transport.req("AgentGet", id=agent_id)

    def patch_agent(self, agent: Agent, modified: str) -> Agent:
        return self._transport.req("AgentPatch", agent=agent, mask=modified)

    def delete_agent(self, agent_id: ID) -> None:
        self._transport.req("AgentDelete", id=agent_id)

    @property
    def tests(self) -> List[SynTest]:
        return self._transport.req("TestsList")

    def test(self, test: Union[ID, SynTest]) -> SynTest:
        if isinstance(test, SynTest):
            test_id = test.id
        else:
            test_id = test

        return self._transport.req("TestGet", id=test_id)

    def create_test(self, test: SynTest) -> SynTest:
        return self._transport.req("TestCreate", test=test)

    def patch_test(self, test: SynTest, modified: str) -> SynTest:
        if test.id == ID("0"):
            raise RuntimeError(f"test '{test.name}' has not been created yet (id=0). Cannot patch")
        return self._transport.req("TestPatch", test=test, mask=modified)

    def delete_test(self, test: Union[ID, SynTest]) -> None:
        if isinstance(test, SynTest):
            test_id = test.id
        else:
            test_id = test
        self._transport.req("TestDelete", id=test_id)
        if isinstance(test, SynTest):
            test.undeploy()

    def set_test_status(self, test_id: ID, status: TestStatus) -> dict:
        return self._transport.req("TestStatusUpdate", id=test_id, status=status)

    def health(
        self,
        test_ids: List[ID],
        start: datetime,
        end: datetime,
        augment: bool = False,
        agent_ids: Optional[List[ID]] = None,
        task_ids: Optional[List[ID]] = None,
    ) -> List[Any]:
        return self._transport.req(
            "GetHealthForTests",
            test_ids=test_ids,
            start_time=start,
            end_time=end,
            augment=augment,
            agent_ids=agent_ids if agent_ids else [],
            task_ids=task_ids if task_ids else [],
        )

    def results(
        self,
        test: SynTest,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        periods: int = 3,
        **kwargs,
    ) -> List[dict]:
        if not test.deployed:
            raise RuntimeError(f"Test '{test.name}[id: {test.id}] is not deployed yet")
        if not end:
            end = datetime.now(tz=timezone.utc)
        if not start:
            start = end - timedelta(seconds=periods * test.max_period)
        return self.health([test.id], start=start, end=end, **kwargs)

    def trace(
        self,
        test_id: str,
        start: datetime,
        end: datetime,
        agent_ids: Optional[List[str]] = None,
        ips: Optional[List[str]] = None,
    ) -> Any:
        return self._transport.req(
            "GetTraceForTest",
            id=test_id,
            start_time=start,
            end_time=end,
            agent_ids=agent_ids if agent_ids else [],
            target_ips=ips if ips else [],
        )
