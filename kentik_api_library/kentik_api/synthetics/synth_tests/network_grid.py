from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.public.types import IP
from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory, sort_ip_address_list
from .protobuf_tools import pb_assign_collection


@dataclass
class NetworkGridTestSpecific:
    targets: List[IP] = field(default_factory=list)

    def fill_from_pb(self, pb: pb.IpTest) -> None:
        self.targets = [IP(ip) for ip in pb.targets]

    def to_pb(self, pb: pb.IpTest) -> None:
        pb_assign_collection([str(ip) for ip in self.targets], pb.targets)


@dataclass
class GridTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    network_grid: NetworkGridTestSpecific = NetworkGridTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.network_grid.fill_from_pb(pb.network_grid)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.network_grid.to_pb(pb.network_grid)


NetworkGridTestType = TypeVar("NetworkGridTestType", bound="NetworkGridTest")


@dataclass
class NetworkGridTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.NETWORK_GRID)
    settings: GridTestSettings = field(default=GridTestSettings(agent_ids=[]))

    @classmethod
    def create(
        cls: Type[NetworkGridTestType], name: str, targets: List[str], agent_ids: List[str]
    ) -> NetworkGridTestType:
        return cls(
            name=name,
            settings=GridTestSettings(
                agent_ids=agent_ids, network_grid=NetworkGridTestSpecific(targets=sort_ip_address_list(targets))
            ),
        )
