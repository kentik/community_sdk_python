from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class NetworkMeshTestSpecific:
    use_local_ip: bool = False

    def fill_from_pb(self, pb: pb.NetworkMeshTest) -> None:
        self.use_local_ip = pb.use_local_ip

    def to_pb(self, pb: pb.NetworkMeshTest) -> None:
        pb.use_local_ip = self.use_local_ip


@dataclass
class NetworkMeshTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    network_mesh: NetworkMeshTestSpecific = NetworkMeshTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.network_mesh.fill_from_pb(pb.network_mesh)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.network_mesh.to_pb(pb.network_mesh)


NetworkMeshTestType = TypeVar("NetworkMeshTestType", bound="NetworkMeshTest")


@dataclass
class NetworkMeshTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.NETWORK_MESH)
    settings: NetworkMeshTestSettings = field(default_factory=NetworkMeshTestSettings)

    @classmethod
    def create(
        cls: Type[NetworkMeshTestType], name: str, agent_ids: List[str], use_local_ip: bool = False
    ) -> NetworkMeshTestType:
        return cls(
            name=name,
            settings=NetworkMeshTestSettings(
                agent_ids=agent_ids, network_mesh=NetworkMeshTestSpecific(use_local_ip=use_local_ip)
            ),
        )
