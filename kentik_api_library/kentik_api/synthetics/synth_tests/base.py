import logging
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Any, Callable, List, Type, TypeVar

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.internal.grpc import DoNotSerializeMarker, _ConfigElement, _ConfigElementT
from kentik_api.public.defaults import DEFAULT_ID
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

log = logging.getLogger("synth_tests")


def list_factory(l: List[Any]) -> Callable[[], List[Any]]:
    """
    Return a method that returns the provided list. For initializing fields of type List in dataclasses
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


DateTimeT = TypeVar("DateTimeT", bound="DateTime")


class DateTime(datetime):
    """
    A datetime type with protobuf serialization logic
    """

    PB_TYPE = Timestamp

    @classmethod
    def from_pb(cls: Type[DateTimeT], value: Timestamp) -> DateTimeT:
        return cls.fromtimestamp(value.seconds + value.nanos / 1e9, timezone.utc)

    def to_pb(self) -> Timestamp:
        ts = self.timestamp()
        return Timestamp(seconds=int(ts), nanos=int(round(ts - int(ts), 3) * 1e9))


@dataclass
class _MonitoringTask(_ConfigElement):
    timeout: int

    @property
    def task_name(self):
        return ""


@dataclass
class PingTask(_MonitoringTask):
    PB_TYPE = pb.TestPingSettings

    count: int = 5
    timeout: int = 3000
    delay: int = 200  # inter-probe delay
    protocol: Protocol = Protocol.ICMP
    port: int = 0  # unused when protocol=Protocol.ICMP

    @property
    def task_name(self):
        return "ping"


@dataclass
class TraceTask(_MonitoringTask):
    PB_TYPE = pb.TestTraceSettings

    count: int = 3
    timeout: int = 22500
    limit: int = 30  # max. hop count
    delay: int = 0  # inter-probe delay
    protocol: Protocol = Protocol.ICMP
    port: int = 0  # unused when protocol=Protocol.ICMP

    @property
    def task_name(self):
        return "traceroute"


@dataclass
class ActivationSettings(_ConfigElement):
    PB_TYPE = pb.ActivationSettings

    grace_period: str = "1"
    time_unit: str = "m"
    time_window: str = ""
    times: str = "2"


@dataclass
class HealthSettings(_ConfigElement):
    PB_TYPE = pb.HealthSettings

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


SynTestSettingsT = TypeVar("SynTestSettingsT", bound="SynTestSettings")


@dataclass
class SynTestSettings(_ConfigElement):
    PB_TYPE = pb.TestSettings

    tasks: List[TaskType] = field(default_factory=list)
    family: IPFamily = Defaults.family
    period: int = Defaults.period  # in seconds
    agent_ids: List[ID] = field(default_factory=list)
    health_settings: HealthSettings = field(default_factory=HealthSettings)
    notification_channels: List[str] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[SynTestSettingsT], obj: Any) -> SynTestSettingsT:
        """Tweak inherited "from_pb" method to handle ignored and legacy task types"""

        IGNORED_TASK_TYPES = ["bgp-monitor"]
        LEGACY_TASK_TYPES = {"knock": "ping"}

        obj = deepcopy(obj)

        # remove ignored task types
        for ignored in IGNORED_TASK_TYPES:
            while ignored in obj.tasks:
                obj.tasks.remove(ignored)

        # replace legacy task types
        for legacy, replacement in LEGACY_TASK_TYPES.items():
            while legacy in obj.tasks:
                obj.tasks.remove(legacy)
                obj.tasks.append(replacement)

        return super().from_pb(obj)


@dataclass
class UserInfo(_ConfigElement):
    PB_TYPE = DoNotSerializeMarker  # UserInfo is read-only - provided by the server. Skip serialization

    id: ID = ID()
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
    VALID_TEST_PERIODS = [1, 15, 60, 120, 300, 600, 900, 1800, 3600, 5400]
    PB_TYPE = pb.Test

    # read-write
    id: ID = field(default=DEFAULT_ID, init=False)  # id is written for Update request
    name: str
    type: TestType = field(init=False, default=TestType.NONE)
    status: TestStatus = field(default=TestStatus.ACTIVE)
    settings: SynTestSettings = field(default_factory=SynTestSettings)
    labels: List[str] = field(default_factory=list)
    edate: DateTime = field(default=DateTime.fromtimestamp(0, tz=timezone.utc), init=False)  # yes, edate is read-write

    # read-only
    _cdate: DateTime = field(default=DateTime.fromtimestamp(0, tz=timezone.utc), init=False)
    _created_by: UserInfo = field(default_factory=UserInfo, init=False)
    _last_updated_by: UserInfo = field(default_factory=UserInfo, init=False)

    def _common_attribute_fixups(self):
        # Correct settings.health_settings.activation parameters if necessary
        orig = None
        if not self.settings.health_settings.activation.times:
            self.settings.health_settings.activation.times = "3"
        min_activation_window = int(
            self.settings.period * (int(self.settings.health_settings.activation.times) + 1) / 60
        )
        if not self.settings.health_settings.activation.time_window:
            orig = "{}{}".format(
                self.settings.health_settings.activation.time_window, self.settings.health_settings.activation.time_unit
            )
            self.settings.health_settings.activation.time_window = str(min_activation_window)
            self.settings.health_settings.activation.time_unit = "m"
        else:
            # Fixup alert time window
            # Convert current activation window to minutes
            if self.settings.health_settings.activation.time_unit == "h":
                self.settings.health_settings.activation.time_window = str(
                    int(self.settings.health_settings.activation.time_window) * 60
                )
                self.settings.health_settings.activation.time_unit = "m"
            if int(self.settings.health_settings.activation.time_window) < min_activation_window:
                orig = "{}{}".format(
                    self.settings.health_settings.activation.time_window,
                    self.settings.health_settings.activation.time_unit,
                )
                self.settings.health_settings.activation.time_window = str(min_activation_window)
        if orig is not None:
            log.debug(
                "_common_attribute_fixups: test: '%s' activation.time_window changed from %s to '%s%s'",
                self.name,
                orig,
                self.settings.health_settings.activation.time_window,
                self.settings.health_settings.activation.time_unit,
            )

    def __post_init__(self):
        self._common_attribute_fixups()

    @property
    def deployed(self) -> bool:
        return self.id != DEFAULT_ID

    @property
    def created_date(self) -> datetime:
        return self._cdate

    @property
    def updated_date(self) -> datetime:
        return self.edate

    @property
    def created_by(self) -> UserInfo:
        return self._created_by

    @property
    def last_updated_by(self) -> UserInfo:
        return self._last_updated_by

    @property
    def targets(self) -> List[str]:
        type_label = self.type.value
        try:
            d = getattr(self.settings, type_label)
            if hasattr(d, "target"):
                return [d.target]
            if hasattr(d, "targets"):
                return sorted(d.targets, key=lambda x: str(x))
        except AttributeError:
            pass
        log.debug("'%s' (type: '%s'): Test has no targets", self.name, self.type.value)
        return []

    def undeploy(self):
        self.id = DEFAULT_ID

    def set_period(self, period_seconds: int):
        if period_seconds not in self.VALID_TEST_PERIODS:
            log.warning(
                "Test period (%d) is not one of allowed values (%s)",
                period_seconds,
                ", ".join([str(x) for x in self.VALID_TEST_PERIODS]),
            )
            try:
                period_seconds = max([v for v in self.VALID_TEST_PERIODS if v < period_seconds])
            except ValueError:
                period_seconds = 60
            log.warning("Test period set to: %d", period_seconds)
        self.settings.period = period_seconds
        self._common_attribute_fixups()


@dataclass
class PingTraceTestSettings(SynTestSettings):
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)


@dataclass
class PingTraceTest(SynTest):
    settings: PingTraceTestSettings = field(default_factory=PingTraceTestSettings)
