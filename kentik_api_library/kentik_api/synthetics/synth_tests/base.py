import logging
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone, tzinfo
from ipaddress import ip_address
from typing import Any, Callable, List, Optional, Set, Type, TypeVar, get_args

import inflection
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
    Marker type for _ConfigElement.to_pb() method: skip objects with field PB_TYPE == NotSerializableMarker during serialization to protobuf object
    """


_ConfigElementT = TypeVar("_ConfigElementT", bound="_ConfigElement")


class _ConfigElement:
    """
    Base class that enables automatic protobuf class <-> user facing dataclass serialization/deserialization.
    Protobuf class and user facing dataclass need to have fields named exactly the same.
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
                if not src_value:
                    return []
                list_item_type = type(src_value[0])  # assuming either primitive type or type with "to_pb()" method
                return [get_value(list_item_type, e) for e in src_value]
            if isinstance(src_value, dict):
                if not src_value:
                    return {}
                dict_value_type = type(list(src_value.values())[0])  # assuming primitive type or type with "to_pb()"
                return {k: get_value(dict_value_type, v) for k, v in src_value.items()}
            try:
                return dst_type(src_value)
            except TypeError as error:
                raise RuntimeError(f"Don't know how to serialize to '{dst_type}' (value: '{src_value}')") from error

        dummy_pb_instance = self.PB_TYPE()  # used only for examining the destination protobuf object field types
        args = {}
        for f in fields(self):
            dst_field_name = f.name[1:] if (f.name[0] == "_") else f.name  # handle private fields that start with "_"
            dst_field_type = type(getattr(dummy_pb_instance, dst_field_name))
            src_field_value = getattr(self, f.name)
            args[dst_field_name] = get_value(dst_field_type, src_field_value)
        return self.PB_TYPE(**args)

    @classmethod
    def from_pb(cls: Type[_ConfigElementT], obj: Any) -> _ConfigElementT:
        def get_value(dst_type: Type[Any], src_value: Any) -> Any:
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
            src_name = f.name[1:] if (f.name[0] == "_") else f.name  # handle private fields that start with "_"
            v = get_value(f.type, getattr(obj, src_name))
            setattr(instance, f.name, v)
        return instance


DateTimeT = TypeVar("DateTimeT", bound="DateTime")


class DateTime(datetime):
    """
    A datetime type with protobuf serialization logic
    """

    PB_TYPE = DoNotSerializeMarker  # datetime fields are read-only - provided by the server. Skip serialization

    @classmethod
    def fromtimestamp(cls: Type[DateTimeT], timestamp: float, tz: Optional[tzinfo] = None) -> DateTimeT:
        dt = datetime.fromtimestamp(timestamp, tz)
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            tzinfo=dt.tzinfo,
        )

    @classmethod
    def from_pb(cls: Type[DateTimeT], value: Timestamp) -> DateTimeT:
        return cls.fromtimestamp(value.seconds, timezone.utc)

    def to_pb(self) -> Timestamp:
        seconds = int(self.timestamp())
        return Timestamp(seconds=seconds, nanos=0)


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
    def task_name(cls) -> Optional[str]:
        return None


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
    PB_TYPE = pb.Test

    # read-write
    name: str
    type: TestType = field(init=False, default=TestType.NONE)
    status: TestStatus = field(default=TestStatus.ACTIVE)
    settings: SynTestSettings = field(default_factory=SynTestSettings)

    # read-only (although _id is serialized for Update call)
    _id: ID = field(default=DEFAULT_ID, init=False)
    _cdate: DateTime = field(default=DateTime.fromtimestamp(0, tz=timezone.utc), init=False)
    _edate: DateTime = field(default=DateTime.fromtimestamp(0, tz=timezone.utc), init=False)
    _created_by: UserInfo = field(default_factory=UserInfo, init=False)
    _last_updated_by: UserInfo = field(default_factory=UserInfo, init=False)

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
        # What is the purpose of this property? Do we need it?
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

    def set_period(self, period_seconds: int):
        self.settings.period = period_seconds

    def set_timeout(self, timeout: int):
        pass


@dataclass
class PingTraceTestSettings(SynTestSettings):
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)


@dataclass
class PingTraceTest(SynTest):
    settings: PingTraceTestSettings = field(default_factory=PingTraceTestSettings)
