from dataclasses import dataclass, field
from typing import List

from kentik_api.public.types import ID, IP

from .agent import Agent


@dataclass
class IDbyIP:
    id: ID = ID()
    ip: IP = IP()


@dataclass
class ASN:
    id: ID = ID()
    name: str = ""


@dataclass
class DNS:
    name: str = ""


@dataclass
class Country:
    code: str = ""  # "CN"
    name: str = ""  # "China"


@dataclass
class Region:
    id: ID = ID()  # "112"
    name: str = ""  # "Zhejiang"


@dataclass
class City:
    id: ID = ID()
    name: str = ""
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class Geo:
    country: Country = Country()
    city: City = City()
    region: Region = Region()


@dataclass
class IPInfo:
    ip: IP = IP()
    asn: ASN = ASN()
    geo: Geo = Geo()
    dns: DNS = DNS()
    device_id: ID = ID()
    site_id: ID = ID()
    egress: str = ""


@dataclass
class TracerouteLookup:
    agent_id_by_ip: List[IDbyIP] = field(default_factory=list)
    agents: List[Agent] = field(default_factory=list)
    asns: List[ASN] = field(default_factory=list)
    device_id_by_ip: List[IDbyIP] = field(default_factory=list)
    site_id_by_ip: List[IDbyIP] = field(default_factory=list)
    ips: List[IPInfo] = field(default_factory=list)


@dataclass
class TraceHop:
    ttl: int = 0
    ip: IP = IP()
    timeout: bool = False
    latency: int = 0
    min_expected_latency: int = 0
    asn: int = 0
    site: int = 0
    region: int = 0
    target: bool = False
    trace_end: bool = False


@dataclass
class TraceProbe:
    as_path: List[int] = field(default_factory=list)
    completed: bool = False
    hop_count: int = 0
    region_path: List[str] = field(default_factory=list)
    site_path: List[str] = field(default_factory=list)
    hops: List[TraceHop] = field(default_factory=list)


@dataclass
class Trace:
    agent_id: ID = ID()
    agent_ip: IP = IP()
    target_ip: IP = IP()
    hop_count: int = 0
    probes: List[TraceProbe] = field(default_factory=list)


@dataclass
class Stats:
    average: int = 0
    max: int = 0
    total: int = 0


@dataclass
class TracerouteResult:
    time: str = ""
    traces: List[Trace] = field(default_factory=list)
    hop_count: int = 0
    count: Stats = Stats()
    distance: Stats = Stats()


@dataclass
class TracerouteInfo:
    is_trace_routes_truncated: bool = False
    max_asn_path_count: int = 0
    max_site_path_count: int = 0
    max_region_path_count: int = 0


@dataclass
class GetTraceForTestResponse:
    lookups: TracerouteLookup = TracerouteLookup()
    trace_routes: List[TracerouteResult] = field(default_factory=list)
    trace_routes_info: TracerouteInfo = TracerouteInfo()
