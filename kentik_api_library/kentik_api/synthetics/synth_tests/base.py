import logging
from copy import deepcopy
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from ipaddress import ip_address
from typing import Any, Callable, List, Type, TypeVar, get_args

from google.protobuf.timestamp_pb2 import Timestamp

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
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


class DoNotSerializeMarker:
    """
    Marker type for _ConfigElement.to_pb() method: skip objects with field PB_TYPE == NotSerializableMarker
    during serialization to protobuf object
    """


_ConfigElementT = TypeVar("_ConfigElementT", bound="_ConfigElement")


class _ConfigElement:
    """
    Base class that enables automatic protobuf class <-> user facing dataclass serialization/deserialization.
    Protobuf class and user facing dataclass need to have fields named exactly the same.
    Fields starting with underscore "_" are treated as read-only and are not serialized to protobuf.
    """

    PB_TYPE = DoNotSerializeMarker  # Target protobuf type for serialization. To be overridden by inheriting class

    def to_pb(self) -> Any:
        """
        Serialize self to protobuf object type determined by "PB_TYPE"
        """

        def skip_serialization(obj: Any) -> bool:
            return hasattr(obj, "PB_TYPE") and obj.PB_TYPE == DoNotSerializeMarker

        def get_value(dst_type: Type[Any], src_value: Any) -> Any:
            if skip_serialization(src_value):
                return None  # None values are not serialized into output protobuf object
            if hasattr(src_value, "to_pb"):
                return src_value.to_pb()
            if isinstance(src_value, list):
                return [get_value(type(e), e) for e in src_value]
            if isinstance(src_value, dict):
                return {k: get_value(type(v), v) for k, v in src_value.items()}
            try:
                return dst_type(src_value)
            except TypeError as error:
                raise RuntimeError(f"Don't know how to serialize to '{dst_type}' (value: '{src_value}')") from error

        dummy_pb_instance = self.PB_TYPE()  # used only for examining the destination protobuf object field types
        args = {}
        for f in fields(self):
            if f.name[0] == "_":
                continue  # don't serialize read-only fields
            dst_field_type = type(getattr(dummy_pb_instance, f.name))
            src_field_value = getattr(self, f.name)
            args[f.name] = get_value(dst_field_type, src_field_value)
        return self.PB_TYPE(**args)

    @classmethod
    def from_pb(cls: Type[_ConfigElementT], obj: Any) -> _ConfigElementT:
        """
        from_pb can be overridden in a child class to tweak deserialization behavior, and still call _from_protobuf
        """

        return cls._from_protobuf(obj)

    @classmethod
    def _from_protobuf(cls: Type[_ConfigElementT], obj: Any) -> _ConfigElementT:
        def get_value(dst_type: Type[Any], src_value: Any) -> Any:
            if hasattr(dst_type, "from_pb"):
                return dst_type.from_pb(src_value)
            try:
                return dst_type(src_value)
            except TypeError as error:
                if dst_type._name == "List":
                    return [get_value(get_args(dst_type)[0], i) for i in src_value]
                if dst_type._name == "Dict":
                    return {_k: get_value(get_args(dst_type)[1], _v) for _k, _v in src_value.items()}
                raise RuntimeError(f"Don't know how to instantiate '{dst_type}' (value: '{src_value}')") from error

        _init_fields = [f for f in fields(cls) if f.init]
        args = {}
        for f in _init_fields:
            src_name = f.name[1:] if (f.name[0] == "_") else f.name  # handle read-only fields that start with "_"
            args[f.name] = get_value(f.type, getattr(obj, src_name))
        instance = cls(**args)

        _remaining_fields = [f for f in fields(cls) if not f.init]
        for f in _remaining_fields:
            src_name = f.name[1:] if (f.name[0] == "_") else f.name  # handle read-only fields that start with "_"
            v = get_value(f.type, getattr(obj, src_name))
            setattr(instance, f.name, v)
        return instance


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
    def from_pb(cls: Type[_ConfigElementT], obj: Any):
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

        return cls._from_protobuf(obj)


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
