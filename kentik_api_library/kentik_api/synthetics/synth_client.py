import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from urllib.parse import urlparse

from kentik_api.public.types import ID

from .agent import Agent
from .api_transport import KentikAPITransport
from .api_transport_http import SynthHTTPTransport
from .synth_tests import SynTest, TestStatus

log = logging.getLogger("synth_client")


def deserialize(cls, obj, deserialize_func) -> Any:
    if isinstance(obj, cls):
        return obj
    return deserialize_func(obj)


class KentikSynthClient:
    def __init__(
        self,
        credentials: Tuple[str, str],
        transport: Optional[Type[KentikAPITransport]] = None,
        url: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        if url:
            u = urlparse(url)
            dns_path = u.netloc.split(".")
            if dns_path[0] == "api":
                dns_path.insert(0, "synthetics")
                log.debug("Setting url to: %s (input: %s)", u._replace(netloc=".".join(dns_path)).geturl(), url)
                self._url = u._replace(netloc=".".join(dns_path)).geturl()
            else:
                self._url = url
        else:
            self._url = "https://synthetics.api.kentik.com"
        if transport:
            # noinspection Mypy
            # noinspection PyCallingNonCallable
            self._transport = transport(credentials, url=self._url, proxy=proxy)  # type: ignore
        else:
            self._transport = SynthHTTPTransport(credentials, url=self._url, proxy=proxy)

    @property
    def agents(self) -> List[Agent]:
        return self._transport.req("AgentsList")

    def agent(self, agent_id: ID) -> Agent:
        return self._transport.req("AgentGet", id=agent_id)

    def patch_agent(self, agent: Agent, modified: str) -> Agent:
        # return self._transport.req("AgentPatch", id=agent_id, body=dict(agent=data, mask=modified))
        return self._transport.req("AgentPatch", agent=agent, mask=modified)

    def delete_agent(self, agent_id: ID) -> None:
        self._transport.req("AgentDelete", id=agent_id)

    @property
    def tests(self) -> List[SynTest]:
        return [deserialize(SynTest, t, SynTest.test_from_dict) for t in self._transport.req("TestsList")]

    def list_tests(self, presets: bool = False, raw: bool = False) -> Any:
        r = self._transport.req("TestsList", params=dict(presets=presets))
        if raw:
            return r
        return [deserialize(SynTest, t, SynTest.test_from_dict) for t in r]

    def test(self, test: Union[ID, SynTest]) -> SynTest:
        if isinstance(test, SynTest):
            test_id = test.id
        else:
            test_id = test

        # NOTE: "isinstance" calls related to transport will eventually go away
        if isinstance(self._transport, SynthHTTPTransport):
            return SynTest.test_from_dict(self._transport.req("TestGet", id=test_id))
        return self._transport.req("TestGet", id=test_id)

    def test_raw(self, test_id: ID) -> Any:
        return self._transport.req("TestGet", id=test_id)

    def create_test(self, test: SynTest) -> SynTest:
        if isinstance(self._transport, SynthHTTPTransport):
            return SynTest.test_from_dict(self._transport.req("TestCreate", body=test.to_dict()))
        return self._transport.req("TestCreate", test=test)

    def patch_test(self, test: SynTest, modified: str) -> SynTest:
        if test.id == ID("0"):
            raise RuntimeError(f"test '{test.name}' has not been created yet (id=0). Cannot patch")
        if isinstance(self._transport, SynthHTTPTransport):
            body = test.to_dict()
            body["mask"] = modified
            return SynTest.test_from_dict(self._transport.req("TestPatch", id=test.id, body=body))
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
        if isinstance(self._transport, SynthHTTPTransport):
            return self._transport.req("TestStatusUpdate", id=test_id, body=dict(id=test_id, status=status.value))
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
        if isinstance(self._transport, SynthHTTPTransport):
            return self._transport.req(
                "GetHealthForTests",
                body=dict(
                    ids=test_ids,
                    startTime=start.isoformat(),
                    endTime=end.isoformat(),
                    augment=augment,
                    agentIds=agent_ids if agent_ids else [],
                    taskIds=task_ids if task_ids else [],
                ),
            )
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
    ):
        return self._transport.req(
            "GetTraceForTest",
            id=test_id,
            body=dict(
                id=test_id,
                startTime=start.isoformat(),
                endTime=end.isoformat(),
                agentIds=agent_ids if agent_ids else [],
                targetIps=ips if ips else [],
            ),
        )
