from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class HostnameTestSpecific:
    target: str = ""

    def fill_from_pb(self, src: pb.HostnameTest) -> None:
        self.target = src.target

    def to_pb(self, dst: pb.HostnameTest) -> None:
        dst.target = self.target


@dataclass
class HostnameTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    hostname: HostnameTestSpecific = HostnameTestSpecific()

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.hostname.fill_from_pb(src.hostname)

    def to_pb(self, dst: pb.TestSettings) -> None:
        super().to_pb(dst)
        self.hostname.to_pb(dst.hostname)


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
