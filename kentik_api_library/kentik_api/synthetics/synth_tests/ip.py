from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import IP
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory, sort_ip_address_list


@dataclass
class IPTestSpecific:
    targets: List[IP] = field(default_factory=list)

    def fill_from_pb(self, src: pb.IpTest) -> None:
        self.targets = [IP(ip) for ip in src.targets]

    def to_pb(self) -> pb.IpTest:
        return pb.IpTest(targets=[str(ip) for ip in self.targets])


@dataclass
class IPTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    ip: IPTestSpecific = IPTestSpecific()

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.ip.fill_from_pb(src.ip)

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.ip.CopyFrom(self.ip.to_pb())
        return obj


IPTestT = TypeVar("IPTestT", bound="IPTest")


@dataclass
class IPTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.IP)
    settings: IPTestSettings = field(default_factory=IPTestSettings)

    @classmethod
    def create(cls: Type[IPTestT], name: str, targets: List[str], agent_ids: List[str]) -> IPTestT:
        return cls(
            name=name,
            settings=IPTestSettings(agent_ids=agent_ids, ip=IPTestSpecific(targets=sort_ip_address_list(targets))),
        )
