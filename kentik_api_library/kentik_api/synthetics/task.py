from dataclasses import dataclass
from enum import Enum
from typing import Optional

from kentik_api.public.types import ID, IP

from .types import IPFamily


class TaskState(Enum):
    UNSPECIFIED = "TASK_STATE_UNSPECIFIED"
    CREATED = "TASK_STATE_CREATED"
    UPDATED = "TASK_STATE_UPDATED"
    DELETED = "TASK_STATE_DELETED"


@dataclass
class PingTask:
    target: IP = IP()
    period: int = 60  # seconds
    expiry: int = 3000
    count: int = 5


@dataclass
class TraceTask:
    target: IP = IP()
    period: int = 60  # in seconds
    expiry: int = 3000
    limit: int = 5


@dataclass
class HTTPTask:
    target: IP
    period: int
    expiry: int


@dataclass
class KnockTask:
    target: IP
    period: int
    expiry: int
    count: int
    port: int


@dataclass
class DNSTask:
    target: IP
    period: int
    expiry: int
    count: int
    port: int
    type: str
    resolver: str


class ShakeTask:
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
    ping: Optional[PingTask] = None
    traceroute: Optional[TraceTask] = None
    http: Optional[HTTPTask] = None
    knock: Optional[KnockTask] = None
    dns: Optional[DNSTask] = None
    shake: Optional[ShakeTask] = None
