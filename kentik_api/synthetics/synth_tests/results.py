from dataclasses import dataclass, field
from datetime import timezone
from typing import List, Type, TypeVar, Union

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.errors import DeserializationError
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.base import DateTime, _ConfigElement
from kentik_api.synthetics.types import Health

MetricDataT = TypeVar("MetricDataT", bound="MetricData")


@dataclass
class MetricData(_ConfigElement):
    current: int = 0
    rolling_avg: int = 0
    rolling_stddev: int = 0
    health: Health = Health.NONE


PacketLossDataT = TypeVar("PacketLossDataT", bound="PacketLossData")


@dataclass
class PacketLossData(_ConfigElement):
    current: float = 0.0
    health: Health = Health.NONE


PingTaskResultsT = TypeVar("PingTaskResultsT", bound="PingTaskResults")


@dataclass
class PingTaskResults(_ConfigElement):
    target: str = ""  # hostname or IP
    packet_loss: PacketLossData = PacketLossData()
    latency: MetricData = MetricData()
    jitter: MetricData = MetricData()
    dst_ip: IP = IP()


HttpResponseDataT = TypeVar("HttpResponseDataT", bound="HttpResponseData")


@dataclass
class HttpResponseData(_ConfigElement):
    status: int = 0  # HTTP status code
    size: int = 0
    data: str = ""


HttpTaskResultsT = TypeVar("HttpTaskResultsT", bound="HttpTaskResults")


@dataclass
class HttpTaskResults(_ConfigElement):
    target: str = ""  # url
    latency: MetricData = MetricData()
    response: HttpResponseData = HttpResponseData()
    dst_ip: IP = IP()


DnsResponseDataT = TypeVar("DnsResponseDataT", bound="DnsResponseData")


@dataclass
class DnsResponseData(_ConfigElement):
    status: int = 0
    data: str = ""


DnsTaskResultsT = TypeVar("DnsTaskResultsT", bound="DnsTaskResults")


@dataclass
class DnsTaskResults(_ConfigElement):
    target: str = ""  # url
    server: str = ""
    latency: MetricData = MetricData()
    response: DnsResponseData = DnsResponseData()


TaskResultsT = TypeVar("TaskResultsT", bound="TaskResults")


@dataclass
class TaskResults:
    health: Health = Health.NONE
    task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None] = None

    @classmethod
    def from_pb(cls: Type[TaskResultsT], src: pb.TaskResults) -> TaskResultsT:
        """Tricky deserialization; can't be done using _ConfigElement.from_pb"""

        task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None]

        # task must be one of ping/http/dns
        if src.HasField("ping"):
            task = PingTaskResults.from_pb(src.ping)
        elif src.HasField("http"):
            task = HttpTaskResults.from_pb(src.http)
        elif src.HasField("dns"):
            task = DnsTaskResults.from_pb(src.dns)
        else:
            raise DeserializationError(
                cls.__name__,
                "none of ping/http/dns fields found in source protobuf object",
            )
        return cls(health=Health(src.health), task=task)


AgentResultsT = TypeVar("AgentResultsT", bound="AgentResults")


@dataclass
class AgentResults(_ConfigElement):
    agent_id: ID = ID()
    health: Health = Health.NONE
    tasks: List[TaskResults] = field(default_factory=list)


TestResultsT = TypeVar("TestResultsT", bound="TestResults")


@dataclass
class TestResults(_ConfigElement):
    __test__ = False  # mark class as "Not a test"; to avoid pytest warnings
    test_id: ID = ID()
    time: DateTime = DateTime.fromtimestamp(0, tz=timezone.utc)
    health: Health = Health.NONE
    agents: List[AgentResults] = field(default_factory=list)
