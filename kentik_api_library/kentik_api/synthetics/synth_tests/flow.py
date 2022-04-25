from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DirectionType, FlowTestSubType, TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class FlowTestSpecific:
    target: str = ""
    target_refresh_interval_millis: int = 0
    max_providers: int = 0
    max_ip_targets: int = 0
    type: FlowTestSubType = FlowTestSubType.NONE
    inet_direction: DirectionType = DirectionType.NONE
    direction: DirectionType = DirectionType.NONE

    def fill_from_pb(self, src: pb.FlowTest) -> None:
        self.target = src.target
        self.target_refresh_interval_millis = src.target_refresh_interval_millis
        self.max_providers = src.max_providers
        self.max_ip_targets = src.max_ip_targets
        self.type = FlowTestSubType(src.type)
        self.inet_direction = DirectionType(src.inet_direction)
        self.direction = DirectionType(src.direction)

    def to_pb(self, dst: pb.FlowTest) -> None:
        dst.target = self.target
        dst.target_refresh_interval_millis = self.target_refresh_interval_millis
        dst.max_providers = self.max_providers
        dst.max_ip_targets = self.max_ip_targets
        dst.type = self.type.value
        dst.inet_direction = self.inet_direction.value
        dst.direction = self.direction.value


@dataclass
class FlowTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    flow: FlowTestSpecific = field(default_factory=FlowTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "flow"

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.flow.fill_from_pb(src.flow)

    def to_pb(self, dst: pb.TestSettings) -> None:
        super().to_pb(dst)
        self.flow.to_pb(dst.flow)


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
