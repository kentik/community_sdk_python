from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.public.types import IP
from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory, sort_ip_address_list
from .protobuf_tools import pb_assign_collection


@dataclass
class IPTestSpecific:
    targets: List[IP] = field(default_factory=list)

    def fill_from_pb(self, pb: pb.IpTest) -> None:
        self.targets = [IP(ip) for ip in pb.targets]

    def to_pb(self, pb: pb.IpTest) -> None:
        pb_assign_collection([str(ip) for ip in self.targets], pb.targets)


@dataclass
class IPTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    ip: IPTestSpecific = IPTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.ip.fill_from_pb(pb.ip)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.ip.to_pb(pb.ip)


IPTestType = TypeVar("IPTestType", bound="IPTest")


@dataclass
class IPTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.IP)
    settings: IPTestSettings = field(default_factory=IPTestSettings)

    @classmethod
    def create(cls: Type[IPTestType], name: str, targets: List[str], agent_ids: List[str]) -> IPTestType:
        return cls(
            name=name,
            settings=IPTestSettings(agent_ids=agent_ids, ip=IPTestSpecific(targets=sort_ip_address_list(targets))),
        )
