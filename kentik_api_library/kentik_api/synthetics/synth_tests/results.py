from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Type, TypeVar, Union

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc
from kentik_api.synthetics.types import Health

MetricDataType = TypeVar("MetricDataType", bound="MetricData")


@dataclass
class MetricData:
    current: int = 0
    rolling_avg: int = 0
    rolling_stddev: int = 0
    health: Health = Health.NONE

    @classmethod
    def from_pb(cls: Type[MetricDataType], pb: pb.MetricData) -> MetricDataType:
        return cls(
            current=pb.current,
            rolling_avg=pb.rolling_avg,
            rolling_stddev=pb.rolling_stddev,
            health=Health(pb.health),
        )


PacketLossDataType = TypeVar("PacketLossDataType", bound="PacketLossData")


@dataclass
class PacketLossData:
    current: float = 0.0
    health: Health = Health.NONE

    @classmethod
    def from_pb(cls: Type[PacketLossDataType], pb: pb.PacketLossData) -> PacketLossDataType:
        return cls(current=pb.current, health=Health(pb.health))


PingTaskResultsType = TypeVar("PingTaskResultsType", bound="PingTaskResults")


@dataclass
class PingTaskResults:
    type: str = "ping"
    target: str = ""  # url
    packet_loss: PacketLossData = PacketLossData()
    latency: MetricData = MetricData()
    jitter: MetricData = MetricData()
    dst_ip: IP = IP()

    @classmethod
    def from_pb(cls: Type[PingTaskResultsType], pb: pb.PingResults) -> PingTaskResultsType:
        return cls(
            target=pb.target,
            packet_loss=PacketLossData.from_pb(pb.packet_loss),
            latency=MetricData.from_pb(pb.latency),
            jitter=MetricData.from_pb(pb.jitter),
            dst_ip=IP(pb.dst_ip),
        )


HttpResponseDataType = TypeVar("HttpResponseDataType", bound="HttpResponseData")


@dataclass
class HttpResponseData:
    status: int = 0  # HTTP status code
    size: int = 0
    data: str = ""

    @classmethod
    def from_pb(cls: Type[HttpResponseDataType], pb: pb.HTTPResponseData) -> HttpResponseDataType:
        return cls(status=pb.status, size=pb.size, data=pb.data)


HttpTaskResultsType = TypeVar("HttpTaskResultsType", bound="HttpTaskResults")


@dataclass
class HttpTaskResults:
    type: str = "http"
    target: str = ""  # url
    latency: MetricData = MetricData()
    response: HttpResponseData = HttpResponseData()
    dst_ip: IP = IP()

    @classmethod
    def from_pb(cls: Type[HttpTaskResultsType], pb: pb.HTTPResults) -> HttpTaskResultsType:
        return cls(
            target=pb.target,
            latency=MetricData.from_pb(pb.latency),
            response=HttpResponseData.from_pb(pb.response),
            dst_ip=IP(pb.dst_ip),
        )


DnsResponseDataType = TypeVar("DnsResponseDataType", bound="DnsResponseData")


@dataclass
class DnsResponseData:
    status: int = 0
    data: str = ""

    @classmethod
    def from_pb(cls: Type[DnsResponseDataType], pb: pb.DNSResponseData) -> DnsResponseDataType:
        return cls(status=pb.status, data=pb.data)


DnsTaskResultsType = TypeVar("DnsTaskResultsType", bound="DnsTaskResults")


@dataclass
class DnsTaskResults:
    type: str = "dns"
    target: str = ""  # url
    server: str = ""
    latency: MetricData = MetricData()
    response: DnsResponseData = DnsResponseData()

    @classmethod
    def from_pb(cls: Type[DnsTaskResultsType], pb: pb.DNSResults) -> DnsTaskResultsType:
        return cls(
            target=pb.target,
            server=pb.server,
            latency=MetricData.from_pb(pb.latency),
            response=DnsResponseData.from_pb(pb.response),
        )


TaskResultsType = TypeVar("TaskResultsType", bound="TaskResults")


@dataclass
class TaskResults:
    health: Health = Health.NONE
    task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None] = None

    @classmethod
    def from_pb(cls: Type[TaskResultsType], pb: pb.TaskResults) -> TaskResultsType:
        task: Union[PingTaskResults, HttpTaskResults, DnsTaskResults, None]

        # one-of
        if pb.HasField("ping"):
            task = PingTaskResults.from_pb(pb.ping)
        elif pb.HasField("http"):
            task = HttpTaskResults.from_pb(pb.http)
        elif pb.HasField("dns"):
            task = DnsTaskResults.from_pb(pb.dns)
        else:
            task = None
        return cls(health=Health(pb.health), task=task)


AgentResultsType = TypeVar("AgentResultsType", bound="AgentResults")


@dataclass
class AgentResults:
    agent_id: ID = ID()
    health: Health = Health.NONE
    tasks: List[TaskResults] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[AgentResultsType], pb: pb.AgentResults) -> AgentResultsType:
        return cls(
            agent_id=ID(pb.agent_id),
            health=Health(pb.health),
            tasks=[TaskResults.from_pb(task) for task in pb.tasks],
        )


TestResultsType = TypeVar("TestResultsType", bound="TestResults")


@dataclass
class TestResults:
    __test__ = False  # mark class as "Not a test"; to avoid pytest warnings
    test_id: ID = ID()
    time: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)
    health: Health = Health.NONE
    agents: List[AgentResults] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[TestResultsType], pb: pb.TestResults) -> TestResultsType:
        return cls(
            test_id=ID(pb.test_id),
            time=pb_to_datetime_utc(pb.time),
            health=Health(pb.health),
            agents=[AgentResults.from_pb(agent) for agent in pb.agents],
        )
