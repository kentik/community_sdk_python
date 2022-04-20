from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.public.types import ID
from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class AgentTestSpecific:
    target: ID = ID()
    user_local_ip: bool = False

    def fill_from_pb(self, pb: pb.AgentTest) -> None:
        self.target = ID(pb.target)
        self.user_local_ip = pb.use_local_ip

    def to_pb(self, pb: pb.AgentTest) -> None:
        pb.target = str(self.target)
        pb.use_local_ip = self.user_local_ip


@dataclass
class AgentTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    agent: AgentTestSpecific = AgentTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.agent.fill_from_pb(pb.agent)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.agent.to_pb(pb.agent)


AgentTestType = TypeVar("AgentTestType", bound="AgentTest")


@dataclass
class AgentTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.AGENT)
    settings: AgentTestSettings = field(default=AgentTestSettings(agent_ids=[]))

    @classmethod
    def create(cls: Type[AgentTestType], name: str, target: str, agent_ids: List[str]) -> AgentTestType:
        return cls(
            name=name,
            settings=AgentTestSettings(
                agent_ids=agent_ids,
                agent=AgentTestSpecific(target=target),
            ),
        )
