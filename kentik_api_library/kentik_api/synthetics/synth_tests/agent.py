from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class AgentTestSpecific(_ConfigElement):
    target: ID = ID()
    use_local_ip: bool = False

    def to_pb(self) -> pb.AgentTest:
        return pb.AgentTest(
            target=str(self.target),
            use_local_ip=self.use_local_ip,
        )


@dataclass
class AgentTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    agent: AgentTestSpecific = AgentTestSpecific()

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.agent.CopyFrom(self.agent.to_pb())
        return obj


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
