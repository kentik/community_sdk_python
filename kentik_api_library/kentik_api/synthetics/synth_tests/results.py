from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Type, TypeVar, Union

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.errors import DeserializationError
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc
from kentik_api.synthetics.types import Health

MetricDataT = TypeVar("MetricDataT", bound="MetricData")


@dataclass
class MetricData:
    current: int = 0
    rolling_avg: int = 0
    rolling_stddev: int = 0
    health: Health = Health.NONE

    @classmethod
    def from_pb(cls: Type[MetricDataT], src: pb.MetricData) -> MetricDataT:
        return cls(
            current=src.current,
            rolling_avg=src.rolling_avg,
            rolling_stddev=src.rolling_stddev,
            health=Health(src.health),
        )


PacketLossDataT = TypeVar("PacketLossDataT", bound="PacketLossData")


@dataclass
class PacketLossData:
    current: float = 0.0
    health: Health = Health.NONE

    @classmethod
    def from_pb(cls: Type[PacketLossDataT], src: pb.PacketLossData) -> PacketLossDataT:
        return cls(current=src.current, health=Health(src.health))


PingTaskResultsT = TypeVar("PingTaskResultsT", bound="PingTaskResults")


@dataclass
class PingTaskResults:
    type: str = "ping"
    target: str = ""  # hostname or IP
    packet_loss: PacketLossData = PacketLossData()
    latency: MetricData = MetricData()
    jitter: MetricData = MetricData()
    dst_ip: IP = IP()

    @classmethod
    def from_pb(cls: Type[PingTaskResultsT], src: pb.PingResults) -> PingTaskResultsT:
        return cls(
            target=src.target,
            packet_loss=PacketLossData.from_pb(src.packet_loss),
            latency=MetricData.from_pb(src.latency),
            jitter=MetricData.from_pb(src.jitter),
            dst_ip=IP(src.dst_ip),
        )


HttpResponseDataT = TypeVar("HttpResponseDataT", bound="HttpResponseData")


@dataclass
class HttpResponseData:
    status: int = 0  # HTTP status code
    size: int = 0
    data: str = ""

    @classmethod
    def from_pb(cls: Type[HttpResponseDataT], src: pb.HTTPResponseData) -> HttpResponseDataT:
        return cls(status=src.status, size=src.size, data=src.data)


HttpTaskResultsT = TypeVar("HttpTaskResultsT", bound="HttpTaskResults")


@dataclass
class HttpTaskResults:
    type: str = "http"
    target: str = ""  # url
    latency: MetricData = MetricData()
    response: HttpResponseData = HttpResponseData()
    dst_ip: IP = IP()

    @classmethod
    def from_pb(cls: Type[HttpTaskResultsT], src: pb.HTTPResults) -> HttpTaskResultsT:
        return cls(
            target=src.target,
            latency=MetricData.from_pb(src.latency),
            response=HttpResponseData.from_pb(src.response),
            dst_ip=IP(src.dst_ip),
        )


DnsResponseDataT = TypeVar("DnsResponseDataT", bound="DnsResponseData")


@dataclass
class DnsResponseData:
    status: int = 0
    data: str = ""

    @classmethod
    def from_pb(cls: Type[DnsResponseDataT], src: pb.DNSResponseData) -> DnsResponseDataT:
        return cls(status=src.status, data=src.data)


DnsTaskResultsT = TypeVar("DnsTaskResultsT", bound="DnsTaskResults")


@dataclass
class DnsTaskResults:
    type: str = "dns"
    target: str = ""  # url
    server: str = ""
    latency: MetricData = MetricData()
    response: DnsResponseData = DnsResponseData()

    @classmethod
    def from_pb(cls: Type[DnsTaskResultsT], src: pb.DNSResults) -> DnsTaskResultsT:
        return cls(
            target=src.target,
            server=src.server,
            latency=MetricData.from_pb(src.latency),
            response=DnsResponseData.from_pb(src.response),
        )


TaskResultsT = TypeVar("TaskResultsT", bound="TaskResults")


@dataclass
class TaskResults:
    health: Health = Health.NONE
    task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None] = None

    @classmethod
    def from_pb(cls: Type[TaskResultsT], src: pb.TaskResults) -> TaskResultsT:
        task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None]

        # task must be one of ping/http/dns
        if src.HasField("ping"):
            task = PingTaskResults.from_pb(src.ping)
        elif src.HasField("http"):
            task = HttpTaskResults.from_pb(src.http)
        elif src.HasField("dns"):
            task = DnsTaskResults.from_pb(src.dns)
        else:
            raise DeserializationError(cls.__name__, "none of ping/http/dns fields found in source protobuf object")
        return cls(health=Health(src.health), task=task)


AgentResultsT = TypeVar("AgentResultsT", bound="AgentResults")


@dataclass
class AgentResults:
    agent_id: ID = ID()
    health: Health = Health.NONE
    tasks: List[TaskResults] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[AgentResultsT], src: pb.AgentResults) -> AgentResultsT:
        return cls(
            agent_id=ID(src.agent_id),
            health=Health(src.health),
            tasks=[TaskResults.from_pb(task) for task in src.tasks],
        )


TestResultsT = TypeVar("TestResultsT", bound="TestResults")


@dataclass
class TestResults:
    __test__ = False  # mark class as "Not a test"; to avoid pytest warnings
    test_id: ID = ID()
    time: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)
    health: Health = Health.NONE
    agents: List[AgentResults] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[TestResultsT], src: pb.TestResults) -> TestResultsT:
        return cls(
            test_id=ID(src.test_id),
            time=pb_to_datetime_utc(src.time),
            health=Health(src.health),
            agents=[AgentResults.from_pb(agent) for agent in src.agents],
        )
