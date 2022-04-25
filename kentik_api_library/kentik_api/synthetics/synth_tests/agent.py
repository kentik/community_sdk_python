from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class AgentTestSpecific:
    target: ID = ID()
    user_local_ip: bool = False

    def fill_from_pb(self, src: pb.AgentTest) -> None:
        self.target = ID(src.target)
        self.user_local_ip = src.use_local_ip

    def to_pb(self, dst: pb.AgentTest) -> None:
        dst.target = str(self.target)
        dst.use_local_ip = self.user_local_ip


@dataclass
class AgentTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    agent: AgentTestSpecific = AgentTestSpecific()

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.agent.fill_from_pb(src.agent)

    def to_pb(self, dst: pb.TestSettings) -> None:
        super().to_pb(dst)
        self.agent.to_pb(dst.agent)


AgentTestT = TypeVar("AgentTestT", bound="AgentTest")


@dataclass
class AgentTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.AGENT)
    settings: AgentTestSettings = field(default=AgentTestSettings(agent_ids=[]))

    @classmethod
    def create(cls: Type[AgentTestT], name: str, target: str, agent_ids: List[str]) -> AgentTestT:
        return cls(
            name=name,
            settings=AgentTestSettings(
                agent_ids=agent_ids,
                agent=AgentTestSpecific(target=target),
            ),
        )
