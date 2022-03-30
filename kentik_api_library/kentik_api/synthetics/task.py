from dataclasses import dataclass
from enum import Enum
from typing import Optional

import kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP

from .types import IPFamily


class TaskState(Enum):
    UNSPECIFIED = pb.TaskState.TASK_STATE_UNSPECIFIED
    CREATED = pb.TaskState.TASK_STATE_CREATED
    UPDATED = pb.TaskState.TASK_STATE_UPDATED
    DELETED = pb.TaskState.TASK_STATE_DELETED


@dataclass
class PingTaskDefinition:
    target: IP = IP()
    period: int = 60  # seconds
    expiry: int = 3000
    count: int = 5


@dataclass
class TraceTaskDefinition:
    target: IP = IP()
    period: int = 60  # in seconds
    expiry: int = 3000
    limit: int = 5


@dataclass
class HTTPTaskDefinition:
    target: IP
    period: int
    expiry: int


@dataclass
class KnockTaskDefinition:
    target: IP
    period: int
    expiry: int
    count: int
    port: int


@dataclass
class DNSTaskDefinition:
    target: IP
    period: int
    expiry: int
    count: int
    port: int
    type: str
    resolver: str


@dataclass
class ShakeTaskDefinition:
    target: IP
    port: int
    period: int
    expiry: int


@dataclass
class Task:
    id: ID = ID()
    test_id: ID = ID()
    device_id: ID = ID()
    state: TaskState = TaskState.UNSPECIFIED
    status: str = ""
    family: IPFamily = IPFamily.unspecified
    ping: Optional[PingTaskDefinition] = None
    traceroute: Optional[TraceTaskDefinition] = None
    http: Optional[HTTPTaskDefinition] = None
    knock: Optional[KnockTaskDefinition] = None
    dns: Optional[DNSTaskDefinition] = None
    shake: Optional[ShakeTaskDefinition] = None
