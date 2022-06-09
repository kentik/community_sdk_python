import logging
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, get_args

import inflection

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_ID
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

log = logging.getLogger("synth_tests")


def list_factory(l: List[Any]) -> Callable[[], List[Any]]:
    """
    Return a method that returns the provided list
    """

    def wrapped() -> List[Any]:
        return l

    return wrapped


def sort_ip_address_list(addresses: List[str]) -> List[IP]:
    """
    Sort list of IP addresses in standard notation in true address order
    """
    ip_addrs = [ip_address(_a) for _a in addresses]
    ipv4_addrs = sorted([_a for _a in ip_addrs if _a.version == 4])
    ipv6_addrs = sorted([_a for _a in ip_addrs if _a.version == 6])
    return [IP(str(a)) for a in ipv4_addrs] + [IP(str(a)) for a in ipv6_addrs]


@dataclass
class Defaults:
    period: int = 60
    timeout: int = 5000
    family: IPFamily = IPFamily.DUAL


_ConfigElementT = TypeVar("_ConfigElementT", bound="_ConfigElement")


class _ConfigElement:
    """
    Base class that enables automatic protobuf class -> user facing dataclass deserialization.
    Protobuf class and user facing dataclass need to have fields named exactly the same.
    """

    def to_dict(self) -> Dict:
        def value_to_dict(value: Any) -> Any:
            if hasattr(value, "to_dict"):
                return value.to_dict()
            if isinstance(value, dict):
                return {_k: value_to_dict(_v) for _k, _v in value.items()}
            if isinstance(value, list):
                return [value_to_dict(_v) for _v in value]
            return value

        ret: Dict[str, Dict] = {}
        for k, v in [(f.name, self.__getattribute__(f.name)) for f in fields(self) if f.name[0] != "_"]:
            ret[k] = value_to_dict(v)
        return ret

    @classmethod
    def from_pb(cls: Type[_ConfigElementT], obj: Any) -> _ConfigElementT:
        def get_value(dst_type: Type[Any], src_value: Any):
            if dst_type is datetime:
                return pb_to_datetime_utc(src_value)

            if hasattr(dst_type, "from_pb"):
                return dst_type.from_pb(src_value)

            try:
                return dst_type(src_value)
            except TypeError as error:
                if dst_type._name == "List":
                    list_item_type = get_args(dst_type)[0]
                    return [get_value(list_item_type, i) for i in src_value]
                if dst_type._name == "Dict":
                    dict_value_type = get_args(dst_type)[1]
                    return {_k: get_value(dict_value_type, _v) for _k, _v in src_value.items()}
                raise RuntimeError(f"Don't know how to instantiate '{dst_type}' (value: '{src_value}')") from error

        _init_fields = [f for f in fields(cls) if f.init]
        args = {f.name: get_value(f.type, getattr(obj, f.name)) for f in _init_fields}
        instance = cls(**args)

        _remaining_fields = [f for f in fields(cls) if not f.init]
        for f in _remaining_fields:
            name = f.name[1:] if (f.name[0] == "_") else f.name  # handle private fields that start with "_"
            v = get_value(f.type, getattr(obj, name))
            setattr(instance, f.name, v)
        return instance


@dataclass
class _MonitoringTask(_ConfigElement):
    timeout: int

    @property
    def task_name(self):
        return ""


@dataclass
class PingTask(_MonitoringTask):
    count: int = 5
    timeout: int = 3000
    delay: int = 200  # inter-probe delay
    protocol: Protocol = Protocol.ICMP
    port: int = 0  # unused when protocol=Protocol.ICMP

    @property
    def task_name(self):
        return "ping"

    def to_pb(self) -> pb.TestPingSettings:
        return pb.TestPingSettings(
            count=self.count,
            timeout=self.timeout,
            delay=self.delay,
            protocol=self.protocol.value,
            port=self.port,
        )


@dataclass
class TraceTask(_MonitoringTask):
    count: int = 3
    timeout: int = 22500
    limit: int = 30  # max. hop count
    delay: int = 0  # inter-probe delay
    protocol: Protocol = Protocol.ICMP
    port: int = 0  # unused when protocol=Protocol.ICMP

    @property
    def task_name(self):
        return "traceroute"

    def to_pb(self) -> pb.TestTraceSettings:
        return pb.TestTraceSettings(
            count=self.count,
            timeout=self.timeout,
            limit=self.limit,
            delay=self.delay,
            protocol=self.protocol.value,
            port=self.port,
        )


@dataclass
class ActivationSettings(_ConfigElement):
    grace_period: str = "1"
    time_unit: str = "m"
    time_window: str = ""
    times: str = "2"

    def to_pb(self) -> pb.ActivationSettings:
        return pb.ActivationSettings(
            grace_period=self.grace_period,
            time_unit=self.time_unit,
            time_window=self.time_window,
            times=self.times,
        )


@dataclass
class HealthSettings(_ConfigElement):
    latency_critical: float = 0.0
    latency_warning: float = 0.0
    latency_critical_stddev: float = 0.0
    latency_warning_stddev: float = 0.0
    packet_loss_critical: int = 0
    packet_loss_warning: int = 0
    jitter_critical: float = 0.0
    jitter_warning: float = 0.0
    jitter_critical_stddev: float = 0.0
    jitter_warning_stddev: float = 0.0
    http_latency_critical: float = 0.0
    http_latency_warning: float = 0.0
    http_latency_critical_stddev: float = 0.0
    http_latency_warning_stddev: float = 0.0
    http_valid_codes: List[int] = field(default_factory=list)
    dns_valid_codes: List[int] = field(default_factory=list)
    unhealthy_subtest_threshold: int = 1
    activation: ActivationSettings = field(default_factory=ActivationSettings)

    def to_pb(self) -> pb.HealthSettings:
        return pb.HealthSettings(
            latency_critical=self.latency_critical,
            latency_warning=self.latency_warning,
            latency_critical_stddev=self.latency_critical_stddev,
            latency_warning_stddev=self.latency_warning_stddev,
            packet_loss_critical=self.packet_loss_critical,
            packet_loss_warning=self.packet_loss_warning,
            jitter_critical=self.jitter_critical,
            jitter_warning=self.jitter_warning,
            jitter_critical_stddev=self.jitter_critical_stddev,
            jitter_warning_stddev=self.jitter_warning_stddev,
            http_latency_critical=self.http_latency_critical,
            http_latency_warning=self.http_latency_warning,
            http_latency_critical_stddev=self.http_latency_critical_stddev,
            http_latency_warning_stddev=self.http_latency_warning_stddev,
            http_valid_codes=self.http_valid_codes,
            dns_valid_codes=self.dns_valid_codes,
            unhealthy_subtest_threshold=self.unhealthy_subtest_threshold,
            activation=self.activation.to_pb(),
        )


@dataclass
class SynTestSettings(_ConfigElement):
    tasks: List[TaskType] = field(default_factory=list)
    family: IPFamily = Defaults.family
    period: int = Defaults.period  # in seconds
    agent_ids: List[ID] = field(default_factory=list)
    health_settings: HealthSettings = field(default_factory=HealthSettings)
    notification_channels: List[str] = field(default_factory=list)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return None

    def to_pb(self) -> pb.TestSettings:
        return pb.TestSettings(
            family=self.family.value,
            period=self.period,
            agent_ids=[str(id) for id in self.agent_ids],
            tasks=[task.value for task in self.tasks],
            health_settings=self.health_settings.to_pb(),
            notification_channels=self.notification_channels,
        )


@dataclass
class UserInfo(_ConfigElement):
    id: str = ""  # should this be of type ID, like in case of other resources in Kentik ???
    email: str = ""
    full_name: str = ""

    def __str__(self):
        if all(not x for x in (self.__dict__.values())):
            return "<empty>"
        if self.full_name:
            return f"{self.full_name} user_id: {self.id} e-mail: {self.email}"
        return f"user_id: {self.id} e-mail: {self.email}"


@dataclass
class SynTest(_ConfigElement):
    # read-write
    name: str
    type: TestType = field(init=False, default=TestType.NONE)
    status: TestStatus = field(default=TestStatus.ACTIVE)
    settings: SynTestSettings = field(default_factory=SynTestSettings)

    # read-only
    _id: ID = field(default=DEFAULT_ID, init=False)
    _cdate: datetime = field(default=datetime.fromtimestamp(0, tz=timezone.utc), init=False)
    _edate: datetime = field(default=datetime.fromtimestamp(0, tz=timezone.utc), init=False)
    _created_by: UserInfo = field(default_factory=UserInfo, init=False)
    _last_updated_by: UserInfo = field(default_factory=UserInfo, init=False)

    def to_pb(self) -> pb.Test:
        return pb.Test(
            id=str(self._id),  # required for "update" api call
            name=self.name,
            type=self.type.value,
            status=self.status.value,
            settings=self.settings.to_pb(),
        )

    @property
    def deployed(self) -> bool:
        return self.id != DEFAULT_ID

    @property
    def id(self) -> ID:
        return self._id

    @property
    def created_date(self) -> datetime:
        return self._cdate

    @property
    def updated_date(self) -> datetime:
        return self._edate

    @property
    def created_by(self) -> UserInfo:
        return self._created_by

    @property
    def last_updated_by(self) -> UserInfo:
        return self._last_updated_by

    @property
    def targets(self) -> List[str]:
        type_label = inflection.camelize(self.type.value, False)
        try:
            d = getattr(self.settings, type_label)
            if "target" in d:
                return [d["target"]]
            if "targets" in d:
                return sorted(d["targets"])
        except AttributeError:
            pass
        log.debug("'%s' (type: '%s'): Test has no targets", self.name, self.type.value)
        return []

    @property
    def configured_tasks(self) -> Set[str]:
        tasks = set(
            f.name
            for f in fields(self.settings)
            if f.name
            and hasattr(f.type, "task_name")
            and self.settings.__getattribute__(f.name).task_name in self.settings.tasks
        )
        n = self.settings.task_name()
        if n:
            tasks.add(n)
        return tasks

    def undeploy(self):
        self._id = DEFAULT_ID

    def to_dict(self) -> dict:
        return {"test": super().to_dict()}

    def set_period(self, period_seconds: int):
        self.settings.period = period_seconds

    def set_timeout(self, timeout: int):
        pass


@dataclass
class PingTraceTestSettings(SynTestSettings):
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.ping.CopyFrom(self.ping.to_pb())
        obj.trace.CopyFrom(self.trace.to_pb())
        return obj


@dataclass
class PingTraceTest(SynTest):
    settings: PingTraceTestSettings = field(default_factory=PingTraceTestSettings)
