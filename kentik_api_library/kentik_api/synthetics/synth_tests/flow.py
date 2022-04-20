from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

from kentik_api.synthetics.types import *

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

    def fill_from_pb(self, pb: pb.FlowTest) -> None:
        self.target = pb.target
        self.target_refresh_interval_millis = pb.target_refresh_interval_millis
        self.max_providers = pb.max_providers
        self.max_ip_targets = pb.max_ip_targets
        self.type = FlowTestSubType(pb.type)
        self.inet_direction = DirectionType(pb.inet_direction)
        self.direction = DirectionType(pb.direction)

    def to_pb(self, pb: pb.FlowTest) -> None:
        pb.target = self.target
        pb.target_refresh_interval_millis = self.target_refresh_interval_millis
        pb.max_providers = self.max_providers
        pb.max_ip_targets = self.max_ip_targets
        pb.type = self.type.value
        pb.inet_direction = self.inet_direction.value
        pb.direction = self.direction.value


@dataclass
class FlowTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    flow: FlowTestSpecific = field(default_factory=FlowTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "flow"

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.flow.fill_from_pb(pb.flow)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.flow.to_pb(pb.flow)


FlowTestType = TypeVar("FlowTestType", bound="FlowTest")


@dataclass
class FlowTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.FLOW)
    settings: FlowTestSettings = field(default=FlowTestSettings(agent_ids=[]))

    # noinspection PyShadowingBuiltins
    @classmethod
    def create(
        cls: Type[FlowTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        target_type: FlowTestSubType,
        direction: DirectionType,
        inet_direction: DirectionType,
        max_ip_targets: int = 10,
        max_providers: int = 3,
        target_refresh_interval_millis: int = 43200000,
    ) -> FlowTestType:
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
