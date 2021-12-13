from dataclasses import dataclass, field
from typing import List

from kentik_api.public.types import ID, IP

from .agent import Agent
from .task import Task


@dataclass
class OverallHealth:
    health: str = ""  # "warning"
    time: str = ""  # "2021-11-08T07:16:00Z"


@dataclass
class HealthMoment:
    time: str = ""  # "2021-11-08T07:20:00Z"
    src_ip: IP = IP()  # ""
    dst_ip: IP = IP()  # "123.57.94.157"
    packet_loss: int = 0  # 0
    avg_latency: int = 0  # 87425
    avg_weighted_latency: int = 0  # 0
    rolling_avg_latency: int = 0  # 92665
    rolling_stddev_latency: int = 0  # 3465
    rolling_avg_weighted_latency: int = 0  # 0
    latency_health: str = ""  # "healthy"
    packet_loss_health: str = ""  # "healthy"
    overall_health: OverallHealth = OverallHealth()
    avg_jitter: int = 0  # 3793
    rolling_avg_jitter: int = 0  # 3751
    rolling_std_jitter: int = 0  # 418
    jitter_health: str = ""  # "healthy"
    data: str = ""  # "[]"
    size: int = 0  # 0
    status: int = 0  # 0
    task_type: str = ""  # "ping"


@dataclass
class AgentHealth:
    agent: Agent = Agent()
    health: List[HealthMoment] = field(default_factory=list)
    overall_health: OverallHealth = OverallHealth()


@dataclass
class TaskHealth:
    task: Task = Task()
    agents: List[AgentHealth] = field(default_factory=list)
    overall_health: OverallHealth = OverallHealth()


@dataclass
class AgentTaskConfig:
    id: ID = ID()  # agent id
    targets: List[IP] = field(default_factory=list)


@dataclass
class MeshMetric:
    name: str = ""  # "latency"
    health: str = ""  # "healthy"
    value: str = ""  # "141"


@dataclass
class MeshMetrics:
    time: str = ""
    latency: MeshMetric = MeshMetric()
    packet_loss: MeshMetric = MeshMetric()
    jitter: MeshMetric = MeshMetric()


@dataclass
class MeshColumn:
    id: ID = ID()
    name: str = ""
    alias: str = ""
    target: IP = IP()
    metrics: MeshMetrics = MeshMetrics()
    health: List[MeshMetrics] = field(default_factory=list)


@dataclass
class MeshResponse:
    id: ID = ID()
    name: str = ""
    local_ip: IP = IP()
    ip: IP = IP()
    alias: str = ""
    columns: List[MeshColumn] = field(default_factory=list)


@dataclass
class TestHealth:
    test_id: ID = ID()
    tasks: List[TaskHealth] = field(default_factory=list)
    overall_health: OverallHealth = OverallHealth()
    health_ts: List[OverallHealth] = field(default_factory=list)
    agent_task_config: List[AgentTaskConfig] = field(default_factory=list)
    mesh: List[MeshResponse] = field(default_factory=list)