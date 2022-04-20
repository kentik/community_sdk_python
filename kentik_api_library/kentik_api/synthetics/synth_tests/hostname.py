from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class HostnameTestSpecific:
    target: str = ""

    def fill_from_pb(self, pb: pb.HostnameTest) -> None:
        self.target = pb.target

    def to_pb(self, pb: pb.HostnameTest) -> None:
        pb.target = self.target


@dataclass
class HostnameTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    hostname: HostnameTestSpecific = HostnameTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.hostname.fill_from_pb(pb.hostname)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.hostname.to_pb(pb.hostname)


HostnameTestType = TypeVar("HostnameTestType", bound="HostnameTest")


@dataclass
class HostnameTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.HOSTNAME)
    settings: HostnameTestSettings = field(default_factory=HostnameTestSettings)

    @classmethod
    def create(cls: Type[HostnameTestType], name: str, target: str, agent_ids: List[str]) -> HostnameTestType:
        return cls(
            name=name, settings=HostnameTestSettings(agent_ids=agent_ids, hostname=HostnameTestSpecific(target=target))
        )
