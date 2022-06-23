from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class NetworkMeshTestSpecific(_ConfigElement):
    PB_TYPE = pb.NetworkMeshTest

    use_local_ip: bool = False


@dataclass
class NetworkMeshTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    network_mesh: NetworkMeshTestSpecific = NetworkMeshTestSpecific()


NetworkMeshTestT = TypeVar("NetworkMeshTestT", bound="NetworkMeshTest")


@dataclass
class NetworkMeshTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.NETWORK_MESH)
    settings: NetworkMeshTestSettings = field(default_factory=NetworkMeshTestSettings)

    @classmethod
    def create(
        cls: Type[NetworkMeshTestT],
        name: str,
        agent_ids: List[str],
        use_local_ip: bool = False,
    ) -> NetworkMeshTestT:
        return cls(
            name=name,
            settings=NetworkMeshTestSettings(
                agent_ids=agent_ids,
                network_mesh=NetworkMeshTestSpecific(use_local_ip=use_local_ip),
            ),
        )
