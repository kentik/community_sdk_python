import logging
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar

from .types import *

log = logging.getLogger("synth_tests")


@dataclass
class Defaults:
    period: int = 60
    expiry: int = 5000
    family: IPFamily = IPFamily.dual


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
    _name: str
    expiry: int
    period: int = Defaults.period


@dataclass
class PingTask(_MonitoringTask):
    _name: str = "ping"
    count: int = 5
    expiry: int = 3000


@dataclass
class TraceTask(_MonitoringTask):
    _name: str = "traceroute"
    count: int = 3
    protocol: Protocol = Protocol.icmp
    port: int = 33434
    expiry: int = 22500
    limit: int = 30


@dataclass
class HTTPTask(_MonitoringTask):
    _name: str = "http"
    period: int = 0
    expiry: int = 0
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    body: str = ""
    ignoreTlsErrors: bool = False
    cssSelectors: dict = field(default_factory=dict)


class _DefaultList(list):
    _values: Tuple

    def __init__(self):
        super().__init__()
        for v in self._values:
            self.append(v)


class DefaultHTTPValidCodes(_DefaultList):
    _values = (200, 201)


class DefaultDNSValidCodes(_DefaultList):
    _values = (1, 2, 3)


@dataclass
class HealthSettings(_ConfigElement):
    latencyCritical: int = 0
    latencyWarning: int = 0
    latencyCriticalStddev: int = 0
    latencyWarningStddev: int = 0
    packetLossCritical: int = 0
    packetLossWarning: int = 0
    jitterCritical: int = 0
    jitterWarning: int = 0
    jitterCriticalStddev: int = 0
    jitterWarningStddev: int = 0
    httpLatencyCritical: int = 0
    httpLatencyWarning: int = 0
    httpLatencyCriticalStddev: int = 0
    httpLatencyWarningStddev: int = 0
    httpValidCodes: List[int] = field(default_factory=list)
    dnsValidCodes: List[int] = field(default_factory=list)


class DefaultTasks(_DefaultList):
    _values = ("ping", "traceroute")


@dataclass
class MonitoringSettings(_ConfigElement):
    activationGracePeriod: str = "2"
    activationTimeUnit: str = "m"
    activationTimeWindow: str = "5"
    activationTimes: str = "3"
    notificationChannels: List = field(default_factory=list)


@dataclass
class SynTestSettings(_ConfigElement):
    agentIds: List[str] = field(default_factory=list)
    tasks: List[str] = field(default_factory=DefaultTasks)
    healthSettings: HealthSettings = field(default_factory=HealthSettings)
    monitoringSettings: MonitoringSettings = field(default_factory=MonitoringSettings)
    port: int = 0
    period: int = Defaults.period
    count: int = 0
    expiry: int = Defaults.expiry
    limit: int = 0
    protocol: Protocol = field(init=False, default=Protocol.none)
    family: IPFamily = Defaults.family
    rollupLevel: int = field(init=False, default=1)
    servers: List[str] = field(default_factory=list)


@dataclass
class SynTest(_ConfigElement):
    name: str
    type: TestType = field(init=False, default=TestType.none)
    status: TestStatus = field(default=TestStatus.active)
    deviceId: str = field(init=False, default="0")
    _id: str = field(default="0", init=False)
    _cdate: str = field(default_factory=str, init=False)
    _edate: str = field(default_factory=str, init=False)
    settings: SynTestSettings = field(default_factory=SynTestSettings)

    @property
    def id(self) -> str:
        return self._id

    @property
    def deployed(self) -> bool:
        return self.id != "0"

    @property
    def cdate(self) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(self._cdate.replace("Z", "+00:00"))
        except ValueError:
            return None

    @property
    def edate(self) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(self._edate.replace("Z", "+00:00"))
        except ValueError:
            return None

    @property
    def max_period(self) -> int:
        return max([self.settings.period] + [self.settings.__getattribute__(t).period for t in self.configured_tasks])

    @property
    def configured_tasks(self) -> Set[str]:
        return set(
            f.name
            for f in fields(self.settings)
            if hasattr(f.type, "period")
            and hasattr(f.type, "_name")
            and self.settings.__getattribute__(f.name)._name in self.settings.tasks
        )

    def undeploy(self):
        self._id = "0"

    def to_dict(self) -> dict:
        return {"test": super(SynTest, self).to_dict()}

    @classmethod
    def test_from_dict(cls, d: dict):
        def class_for_type(test_type: TestType) -> Any:
            return {
                TestType.none: SynTest,
                TestType.agent: AgentTest,
                TestType.bgp_monitor: SynTest,
                TestType.dns: DNSTest,
                TestType.dns_grid: DNSGridTest,
                TestType.flow: FlowTest,
                TestType.hostname: HostnameTest,
                TestType.ip: IPTest,
                TestType.mesh: MeshTest,
                TestType.network_grid: NetworkGridTest,
                TestType.page_load: PageLoadTest,
                TestType.url: UrlTest,
            }.get(test_type)

        try:
            cls_type = class_for_type(TestType(d["type"]))
        except KeyError as ex:
            raise RuntimeError(f"Required attribute '{ex}' missing in test data ('{d}')")
        if cls_type is None:
            raise RuntimeError(f"Unsupported test type: {d['type']}")
        if cls_type == cls:
            log.debug("'%s' tests are not fully supported in the API. Test will have incomplete attributes", d["type"])
        return cls_type.from_dict(d)

    def set_period(self, period_seconds: int):
        self.settings.period = period_seconds
        for f in fields(self.settings):
            if hasattr(f.type, "period") and self.settings.__getattribute__(f.name):
                self.settings.__getattribute__(f.name).period = int(period_seconds)

    def set_timeout(self, timeout_seconds: float, tasks: Optional[List[str]] = None):
        if not tasks:
            self.settings.expiry = int(timeout_seconds * 1000)
        else:
            # sanity check
            missing = set(tasks).difference(self.configured_tasks)
            if missing:
                log.warning("task(s) '%s' not presents in test '%s'", " ".join(missing), self.name)
            for t in self.configured_tasks:
                if t in tasks:
                    self.settings.__getattribute__(t).expiry = int(timeout_seconds * 1000)  # API wants it in millis


@dataclass
class PingTraceTestSettings(SynTestSettings):
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)
    family: IPFamily = IPFamily.dual
    protocol: Protocol = Protocol.icmp


@dataclass
class PingTraceTest(SynTest):
    settings: PingTraceTestSettings = field(default_factory=PingTraceTestSettings)

    def set_timeout(self, timeout_seconds: float, tasks: Optional[List[str]] = None):
        existing = self.configured_tasks
        if tasks:
            # sanity check
            missing = set(tasks).difference(existing)
            if missing:
                log.warning("task(s) '%s' not presents in test '%s'", " ".join(missing), self.name)
        for t in existing:
            if not tasks or t in tasks:
                self.settings.__getattribute__(t).expiry = int(timeout_seconds * 1000)  # API wants it in millis


@dataclass
class HostnameTestSettings(PingTraceTestSettings):
    hostname: dict = field(default_factory=dict)


HostnameTestType = TypeVar("HostnameTestType", bound="HostnameTest")


@dataclass
class HostnameTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.hostname)
    settings: HostnameTestSettings = field(default_factory=HostnameTestSettings)

    @classmethod
    def create(cls: Type[HostnameTestType], name: str, target: str, agent_ids: List[str]) -> HostnameTestType:
        return cls(name=name, settings=HostnameTestSettings(agentIds=agent_ids, hostname=dict(target=target)))


@dataclass
class IPTestSettings(PingTraceTestSettings):
    ip: dict = field(default_factory=dict)


IPTestType = TypeVar("IPTestType", bound="IPTest")


@dataclass
class IPTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.ip)
    settings: IPTestSettings = field(default_factory=IPTestSettings)

    @classmethod
    def create(cls: Type[IPTestType], name: str, targets: List[str], agent_ids: List[str]) -> IPTestType:
        return cls(name=name, settings=IPTestSettings(agentIds=agent_ids, ip=dict(targets=targets)))


MeshTestType = TypeVar("MeshTestType", bound="MeshTest")


@dataclass
class MeshTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.mesh)

    @classmethod
    def create(cls: Type[MeshTestType], name: str, agent_ids: List[str]) -> MeshTestType:
        return cls(name=name, settings=PingTraceTestSettings(agentIds=agent_ids))


@dataclass
class GridTestSettings(PingTraceTestSettings):
    networkGrid: dict = field(default_factory=dict)


NetworkGridTestType = TypeVar("NetworkGridTestType", bound="NetworkGridTest")


@dataclass
class NetworkGridTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.network_grid)
    settings: GridTestSettings = field(default=GridTestSettings(agentIds=[]))

    @classmethod
    def create(
        cls: Type[NetworkGridTestType], name: str, targets: List[str], agent_ids: List[str]
    ) -> NetworkGridTestType:
        return cls(name=name, settings=GridTestSettings(agentIds=agent_ids, networkGrid=dict(targets=targets)))


@dataclass
class FlowTestSettings(PingTraceTestSettings):
    flow: dict = field(default_factory=dict)


FlowTestType = TypeVar("FlowTestType", bound="FlowTest")


@dataclass
class FlowTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.flow)
    settings: FlowTestSettings = field(default=FlowTestSettings(agentIds=[]))

    # noinspection PyShadowingBuiltins
    @classmethod
    def create(
        cls: Type[FlowTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        type: FlowTestSubType,
        direction: DirectionType,
        inet_direction: DirectionType,
        max_tasks: int = 5,
        target_refresh_interval: int = 43200000,
    ) -> FlowTestType:
        return cls(
            name=name,
            settings=FlowTestSettings(
                agentIds=agent_ids,
                flow=dict(
                    target=target,
                    type=type,
                    direction=direction,
                    inetDirection=inet_direction,
                    maxTasks=max_tasks,
                    targetRefreshIntervalMillis=target_refresh_interval,
                ),
            ),
        )


@dataclass
class DNSGridTestSettings(SynTestSettings):
    dnsGrid: dict = field(default_factory=dict)


DNSGridTestType = TypeVar("DNSGridTestType", bound="DNSGridTest")


@dataclass
class DNSGridTest(SynTest):
    type: TestType = field(init=False, default=TestType.dns_grid)
    settings: DNSGridTestSettings = field(default_factory=DNSGridTestSettings)

    @classmethod
    def create(
        cls: Type[DNSGridTestType],
        name: str,
        targets: List[str],
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
    ) -> DNSGridTestType:
        return cls(
            name=name,
            settings=DNSGridTestSettings(
                agentIds=agent_ids,
                dnsGrid=dict(targets=targets, type=record_type),
                servers=servers,
                tasks=["dns"],
                port=53,
            ),
        )

    @property
    def max_period(self) -> int:
        return self.settings.period


@dataclass
class DNSTestSettings(SynTestSettings):
    dns: dict = field(default_factory=dict)


DNSTestType = TypeVar("DNSTestType", bound="DNSTest")


@dataclass
class DNSTest(SynTest):
    type: TestType = field(init=False, default=TestType.dns)
    settings: DNSTestSettings = field(default_factory=DNSTestSettings)

    @classmethod
    def create(
        cls: Type[DNSTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
    ) -> DNSTestType:
        return cls(
            name=name,
            settings=DNSTestSettings(
                agentIds=agent_ids, dns=dict(target=target, type=record_type), servers=servers, tasks=["dns"], port=53
            ),
        )

    @property
    def max_period(self) -> int:
        return self.settings.period


@dataclass
class UrlTestSettings(SynTestSettings):
    url: dict = field(default_factory=dict)
    ping: PingTask = field(default_factory=PingTask)
    trace: TraceTask = field(default_factory=TraceTask)
    http: HTTPTask = field(default_factory=HTTPTask)


UrlTestType = TypeVar("UrlTestType", bound="UrlTest")


@dataclass
class UrlTest(SynTest):
    type: TestType = field(init=False, default=TestType.url)
    settings: UrlTestSettings = field(default_factory=UrlTestSettings)

    @classmethod
    def create(
        cls: Type[UrlTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: str = "",
        ignore_tls_errors: bool = False,
        ping: bool = False,
        trace: bool = False,
    ) -> UrlTestType:
        tasks: List[str] = ["http"]
        if ping:
            tasks.append("ping")
        if trace:
            tasks.append("traceroute")
        return cls(
            name=name,
            settings=UrlTestSettings(
                agentIds=agent_ids,
                url=dict(target=target),
                tasks=tasks,
                http=HTTPTask(method=method, body=body, headers=headers or {}, ignoreTlsErrors=ignore_tls_errors),
            ),
        )


@dataclass
class PageLoadTestSettings(PingTraceTestSettings):
    pageLoad: dict = field(default_factory=dict)
    http: HTTPTask = field(default_factory=HTTPTask)


PageLoadTestType = TypeVar("PageLoadTestType", bound="PageLoadTest")


@dataclass
class PageLoadTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.page_load)
    settings: PageLoadTestSettings = field(default_factory=PageLoadTestSettings)

    @classmethod
    def create(
        cls: Type[PageLoadTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: str = "",
        ignore_tls_errors: bool = False,
    ) -> PageLoadTestType:
        return cls(
            name=name,
            settings=PageLoadTestSettings(
                agentIds=agent_ids,
                pageLoad=dict(target=target),
                tasks=["page-load"],
                http=HTTPTask(method=method, body=body, headers=headers or {}, ignoreTlsErrors=ignore_tls_errors),
            ),
        )


@dataclass
class AgentTestSettings(PingTraceTestSettings):
    agent: dict = field(default_factory=dict)


AgentTestType = TypeVar("AgentTestType", bound="AgentTest")


@dataclass
class AgentTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.agent)
    settings: AgentTestSettings = field(default=AgentTestSettings(agentIds=[]))

    @classmethod
    def create(cls: Type[AgentTestType], name: str, target: str, agent_ids: List[str]) -> AgentTestType:
        return cls(name=name, settings=AgentTestSettings(agentIds=agent_ids, agent=dict(target=target)))
