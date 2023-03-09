from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DirectionType, FlowTestSubType, TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class FlowTestSpecific(_ConfigElement):
    PB_TYPE = pb.FlowTest

    target: str = ""  # city name
    target_refresh_interval_millis: int = 0
    max_providers: int = 0
    max_ip_targets: int = 0
    type: FlowTestSubType = FlowTestSubType.NONE
    inet_direction: DirectionType = DirectionType.NONE
    direction: DirectionType = DirectionType.NONE


@dataclass
class FlowTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PING, TaskType.TRACE_ROUTE]))
    flow: FlowTestSpecific = field(default_factory=FlowTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "flow"


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
