from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory, sort_ip_address_list
from .ip import IPTestSpecific

NetworkGridTestSpecific = IPTestSpecific


@dataclass
class GridTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    network_grid: NetworkGridTestSpecific = NetworkGridTestSpecific()

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.network_grid.fill_from_pb(src.network_grid)

    def to_pb(self, dst: pb.TestSettings) -> None:
        super().to_pb(dst)
        self.network_grid.to_pb(dst.network_grid)


NetworkGridTestT = TypeVar("NetworkGridTestT", bound="NetworkGridTest")


@dataclass
class NetworkGridTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.NETWORK_GRID)
    settings: GridTestSettings = field(default=GridTestSettings(agent_ids=[]))

    @classmethod
    def create(cls: Type[NetworkGridTestT], name: str, targets: List[str], agent_ids: List[str]) -> NetworkGridTestT:
        return cls(
            name=name,
            settings=GridTestSettings(
                agent_ids=agent_ids, network_grid=NetworkGridTestSpecific(targets=sort_ip_address_list(targets))
            ),
        )
