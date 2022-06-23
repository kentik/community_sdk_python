from dataclasses import dataclass, field
from datetime import timezone
from typing import Dict, List, TypeVar

from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.base import DateTime, _ConfigElement

LocationT = TypeVar("LocationT", bound="Location")


@dataclass
class Location(_ConfigElement):
    latitude: float = 0.0
    longitude: float = 0.0
    country: str = ""
    region: str = ""
    city: str = ""


NetNodeT = TypeVar("NetNodeT", bound="NetNode")


@dataclass
class NetNode(_ConfigElement):
    ip: IP = IP()
    asn: int = 0
    as_name: str = ""
    location: Location = Location()
    dns_name: str = ""
    device_id: ID = ID()
    site_id: ID = ID()


StatsT = TypeVar("StatsT", bound="Stats")


@dataclass
class Stats(_ConfigElement):
    average: int = 0
    min: int = 0
    max: int = 0


TraceHopT = TypeVar("TraceHopT", bound="TraceHop")


@dataclass
class TraceHop(_ConfigElement):
    latency: int = 0
    node_id: str = ""


PathTraceT = TypeVar("PathTraceT", bound="PathTrace")


@dataclass
class PathTrace(_ConfigElement):
    as_path: List[int] = field(default_factory=list)
    is_complete: bool = False
    hops: List[TraceHop] = field(default_factory=list)


PathT = TypeVar("PathT", bound="Path")


@dataclass
class Path(_ConfigElement):
    agent_id: ID = ID()
    target_ip: IP = IP()
    hop_count: Stats = Stats()
    max_as_path_length: int = 0
    traces: List[PathTrace] = field(default_factory=list)
    time: DateTime = DateTime.fromtimestamp(0, tz=timezone.utc)


TraceResponseT = TypeVar("TraceResponseT", bound="TraceResponse")


@dataclass
class TraceResponse(_ConfigElement):
    nodes: Dict[str, NetNode] = field(default_factory=dict)
    paths: List[Path] = field(default_factory=list)
