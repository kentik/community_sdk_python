from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class HostnameTestSpecific(_ConfigElement):
    target: str = ""

    def to_pb(self) -> pb.HostnameTest:
        return pb.HostnameTest(target=self.target)


@dataclass
class HostnameTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    hostname: HostnameTestSpecific = HostnameTestSpecific()

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.hostname.CopyFrom(self.hostname.to_pb())
        return obj


HostnameTestT = TypeVar("HostnameTestT", bound="HostnameTest")


@dataclass
class HostnameTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.HOSTNAME)
    settings: HostnameTestSettings = field(default_factory=HostnameTestSettings)

    @classmethod
    def create(cls: Type[HostnameTestT], name: str, target: str, agent_ids: List[str]) -> HostnameTestT:
        return cls(
            name=name, settings=HostnameTestSettings(agent_ids=agent_ids, hostname=HostnameTestSpecific(target=target))
        )
