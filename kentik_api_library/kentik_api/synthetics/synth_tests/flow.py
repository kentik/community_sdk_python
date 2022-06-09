from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DirectionType, FlowTestSubType, TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class FlowTestSpecific(_ConfigElement):
    target: str = ""
    target_refresh_interval_millis: int = 0
    max_providers: int = 0
    max_ip_targets: int = 0
    type: FlowTestSubType = FlowTestSubType.NONE
    inet_direction: DirectionType = DirectionType.NONE
    direction: DirectionType = DirectionType.NONE

    def to_pb(self) -> pb.FlowTest:
        return pb.FlowTest(
            target=self.target,
            target_refresh_interval_millis=self.target_refresh_interval_millis,
            max_providers=self.max_providers,
            max_ip_targets=self.max_ip_targets,
            type=self.type.value,
            inet_direction=self.inet_direction.value,
            direction=self.direction.value,
        )


@dataclass
class FlowTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    flow: FlowTestSpecific = field(default_factory=FlowTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "flow"

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.flow.CopyFrom(self.flow.to_pb())
        return obj


FlowTestT = TypeVar("FlowTestT", bound="FlowTest")


@dataclass
class FlowTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.FLOW)
    settings: FlowTestSettings = field(default=FlowTestSettings(agent_ids=[]))

    # noinspection PyShadowingBuiltins
    @classmethod
    def create(
        cls: Type[FlowTestT],
        name: str,
        target: str,
        agent_ids: List[str],
        target_type: FlowTestSubType,
        direction: DirectionType,
        inet_direction: DirectionType,
        max_ip_targets: int = 10,
        max_providers: int = 3,
        target_refresh_interval_millis: int = 43200000,
    ) -> FlowTestT:
        return cls(
            name=name,
            settings=FlowTestSettings(
                agent_ids=agent_ids,
                flow=FlowTestSpecific(
                    target=target,
                    type=target_type,
                    direction=direction,
                    inet_direction=inet_direction,
                    max_ip_targets=max_ip_targets,
                    max_providers=max_providers,
                    target_refresh_interval_millis=target_refresh_interval_millis,
                ),
            ),
        )
