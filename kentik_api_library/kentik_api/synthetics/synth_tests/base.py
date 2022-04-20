import logging
from dataclasses import dataclass, field, fields
from datetime import datetime
from ipaddress import ip_address
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar

import inflection

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU, DEFAULT_ID
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_assign_collection, pb_to_datetime_utc
from kentik_api.synthetics.types import *

log = logging.getLogger("synth_tests")


def list_factory(l: List[Any]) -> Callable[[], List[Any]]:
    """Return method that returns a list"""

    def wrapped() -> List[Any]:
        return l

    return wrapped


def sort_ip_address_list(addresses: List[str]) -> List[IP]:
    """
    Sort list of IP addresses in standard notation in true address order
    """
    ip_addrs = [ip_address(_a) for _a in addresses]
    return [
        IP(str(a))
        for a in sorted([_a for _a in ip_addrs if _a.version == 4]) + sorted([_a for _a in ip_addrs if _a.version == 6])
    ]


@dataclass
class Defaults:
    period: int = 60
    timeout: int = 5000
    family: IPFamily = IPFamily.DUAL


_ConfigElementType = TypeVar("_ConfigElementType", bound="_ConfigElement")


@dataclass
class _ConfigElement:
    def to_dict(self) -> dict:
        def value_to_dict(value: Any) -> Any:
            if hasattr(value, "to_dict"):
                return value.to_dict()
            elif type(value) == dict:
                return {_k: value_to_dict(_v) for _k, _v in value.items()}
            elif type(value) == list:
                return [value_to_dict(_v) for _v in value]
            else:
                return value

        ret: Dict[str, dict] = dict()
        for k, v in [(f.name, self.__getattribute__(f.name)) for f in fields(self) if f.name[0] != "_"]:
            ret[k] = value_to_dict(v)
        return ret

    @classmethod
    def from_dict(cls: Type[_ConfigElementType], d: dict) -> _ConfigElementType:
        # noinspection PyProtectedMember
        def get_value(f, v):
            if hasattr(f, "from_dict"):
                return f.from_dict(v)
            else:
                try:
                    return f(v)
                except TypeError:
                    if f._name == "List":
                        return [get_value(type(i), i) for i in v]
                    elif f._name == "Dict":
                        return {_k: get_value(type(_v), _v) for _k, _v in v.items()}
                    else:
                        raise RuntimeError(f"Don't know how to instantiate '{f}' (value: '{v}')")

        _init_fields = {f.name: f for f in fields(cls) if f.init}
        args = {k: get_value(_init_fields[k].type, v) for k, v in d.items() if k in _init_fields.keys()}
        # noinspection PyArgumentList
        inst = cls(**args)  # type: ignore
        _other_fields = {f.name: f for f in fields(cls) if not f.init}
        for n, f in _other_fields.items():
            if n[0] == "_":
                k = n.split("_")[1]
            else:
                k = n
            if k in d:
                setattr(inst, n, get_value(f.type, d[k]))
        return inst


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
    port: int = 0

    @property
    def task_name(self):
        return "ping"

    def fill_from_pb(self, pb: pb.TestPingSettings) -> None:
        self.count = pb.count
        self.timeout = pb.timeout
        self.delay = pb.delay
        self.protocol = Protocol(pb.protocol)
        self.port = pb.port

    def to_pb(self, pb: pb.TestPingSettings) -> None:
        pb.count = self.count
        pb.timeout = self.timeout
        pb.delay = self.delay
        pb.protocol = self.protocol.value
        pb.port = self.port


@dataclass
class TraceTask(_MonitoringTask):
    count: int = 3
    timeout: int = 22500
    limit: int = 30  # max. hop count
    delay: int = 0  # inter-probe delay
    protocol: Protocol = Protocol.ICMP
    port: int = 33434

    @property
    def task_name(self):
        return "traceroute"

    def fill_from_pb(self, pb: pb.TestTraceSettings) -> None:
        self.count = pb.count
        self.timeout = pb.timeout
        self.limit = pb.limit
        self.delay = pb.delay
        self.protocol = Protocol(pb.protocol)
        self.port = pb.port

    def to_pb(self, pb: pb.TestTraceSettings) -> None:
        pb.count = self.count
        pb.timeout = self.timeout
        pb.limit = self.limit
        pb.delay = self.delay
        pb.protocol = self.protocol.value
        pb.port = self.port


@dataclass
class ActivationSettings(_ConfigElement):
    grace_period: str = "1"
    time_unit: str = "m"
    time_window: str = ""
    times: str = "2"

    def fill_from_pb(self, pb: pb.ActivationSettings) -> None:
        self.grace_period = pb.grace_period
        self.time_unit = pb.time_unit
        self.time_window = pb.time_window
        self.times = pb.times

    def to_pb(self, pb: pb.ActivationSettings) -> None:
        pb.grace_period = self.grace_period
        pb.time_unit = self.time_unit
        pb.time_window = self.time_window
        pb.times = self.times


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

    def fill_from_pb(self, pb: pb.HealthSettings) -> None:
        self.latency_critical = pb.latency_critical
        self.latency_warning = pb.latency_warning
        self.latency_critical_stddev = pb.latency_critical_stddev
        self.latency_warning_stddev = pb.latency_warning_stddev
        self.packet_loss_critical = pb.packet_loss_critical
        self.packet_loss_warning = pb.packet_loss_warning
        self.jitter_critical = pb.jitter_critical
        self.jitter_warning = pb.jitter_warning
        self.jitter_critical_stddev = pb.jitter_critical_stddev
        self.jitter_warning_stddev = pb.jitter_warning_stddev
        self.http_latency_critical = pb.http_latency_critical
        self.http_latency_warning = pb.http_latency_warning
        self.http_latency_critical_stddev = pb.http_latency_critical_stddev
        self.http_latency_warning_stddev = pb.http_latency_warning_stddev
        self.http_valid_codes = pb.http_valid_codes
        self.dns_valid_codes = pb.dns_valid_codes
        self.unhealthy_subtest_threshold = pb.unhealthy_subtest_threshold
        self.activation.fill_from_pb(pb.activation)

    def to_pb(self, pb: pb.HealthSettings) -> None:
        pb.latency_critical = self.latency_critical
        pb.latency_warning = self.latency_warning
        pb.latency_critical_stddev = self.latency_critical_stddev
        pb.latency_warning_stddev = self.latency_warning_stddev
        pb.packet_loss_critical = self.packet_loss_critical
        pb.packet_loss_warning = self.packet_loss_warning
        pb.jitter_critical = self.jitter_critical
        pb.jitter_warning = self.jitter_warning
        pb.jitter_critical_stddev = self.jitter_critical_stddev
        pb.jitter_warning_stddev = self.jitter_warning_stddev
        pb.http_latency_critical = self.http_latency_critical
        pb.http_latency_warning = self.http_latency_warning
        pb.http_latency_critical_stddev = self.http_latency_critical_stddev
        pb.http_latency_warning_stddev = self.http_latency_warning_stddev
        pb_assign_collection(self.http_valid_codes, pb.http_valid_codes)
        pb_assign_collection(self.dns_valid_codes, pb.dns_valid_codes)
        pb.unhealthy_subtest_threshold = self.unhealthy_subtest_threshold
        self.activation.to_pb(pb.activation)


@dataclass
class SynTestSettings(_ConfigElement):
    tasks: List[TaskType] = field(default_factory=list)
    family: IPFamily = Defaults.family
    period: int = Defaults.period
    agent_ids: List[ID] = field(default_factory=list)
    health_settings: HealthSettings = field(default_factory=HealthSettings)
    notification_channels: List[str] = field(default_factory=list)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return None

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        self.family = IPFamily(pb.family)
        self.period = pb.period
        self.agent_ids = [ID(id) for id in pb.agent_ids]
        self.tasks = [TaskType(task) for task in pb.tasks]
        self.health_settings.fill_from_pb(pb.health_settings)
        self.notification_channels = pb.notification_channels

    def to_pb(self, pb: pb.TestSettings) -> None:
        pb.family = self.family.value
        pb.period = self.period
        pb_assign_collection([str(id) for id in self.agent_ids], pb.agent_ids)
        pb_assign_collection([task.value for task in self.tasks], pb.tasks)
        self.health_settings.to_pb(pb.health_settings)
        pb_assign_collection(self.notification_channels, pb.notification_channels)

    def to_dict(self) -> dict:
        def _id(i: str) -> str:
            try:
                return f"{int(i):010}"
            except ValueError:
                return i

        self.agent_ids.sort(key=lambda x: _id(x))
        return super().to_dict()


@dataclass
class UserInfo(_ConfigElement):
    id: str = ""
    email: str = ""
    full_name: str = ""

    def __str__(self):
        if all(not x for x in (self.__dict__.values())):
            return "<empty>"
        if self.full_name:
            return f"{self.full_name} user_id: {self.id} e-mail: {self.email}"
        else:
            return f"user_id: {self.id} e-mail: {self.email}"

    def fill_from_pb(self, pb: pb.UserInfo) -> None:
        self.id = ID(pb.id)
        self.email = pb.email
        self.full_name = pb.full_name


@dataclass
class SynTest(_ConfigElement):
    # read-write
    name: str
    type: TestType = field(init=False, default=TestType.NONE)
    status: TestStatus = field(default=TestStatus.ACTIVE)
    settings: SynTestSettings = field(default_factory=SynTestSettings)

    # read-only
    _id: ID = field(default=DEFAULT_ID, init=False)
    _cdate: datetime = field(default=datetime.fromisoformat(DEFAULT_DATE_NO_ZULU), init=False)
    _edate: datetime = field(default=datetime.fromisoformat(DEFAULT_DATE_NO_ZULU), init=False)
    _created_by: UserInfo = field(default_factory=UserInfo, init=False)
    _last_updated_by: UserInfo = field(default_factory=UserInfo, init=False)

    def fill_from_pb(self, pb: pb.Test) -> None:
        self.name = pb.name
        self.type = TestType(pb.type)
        self.status = TestStatus(pb.status)
        self.settings.fill_from_pb(pb.settings)
        self._id = ID(pb.id)
        self._cdate = pb_to_datetime_utc(pb.cdate)
        self._edate = pb_to_datetime_utc(pb.edate)
        self._created_by.fill_from_pb(pb.created_by)
        self._last_updated_by.fill_from_pb(pb.last_updated_by)

    def to_pb(self, pb: pb.Test) -> None:
        pb.id = str(self._id)  # required for "update" api call
        pb.name = self.name
        pb.type = self.type.value
        pb.status = self.status.value
        self.settings.to_pb(pb.settings)

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
        return {"test": super(SynTest, self).to_dict()}

    def set_period(self, period_seconds: int):
        self.settings.period = period_seconds

    def set_timeout(self, timeout: int):
        pass


@dataclass
class PingTraceTestSettings(SynTestSettings):
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.ping.fill_from_pb(pb.ping)
        self.trace.fill_from_pb(pb.trace)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.ping.to_pb(pb.ping)
        self.trace.to_pb(pb.trace)


@dataclass
class PingTraceTest(SynTest):
    settings: PingTraceTestSettings = field(default_factory=PingTraceTestSettings)

    def fill_from_pb(self, pb: pb.Test) -> None:
        super().fill_from_pb(pb)

    def to_pb(self, pb: pb.Test) -> None:
        super().to_pb(pb)
