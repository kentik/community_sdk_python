from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc

LocationT = TypeVar("LocationT", bound="Location")


@dataclass
class Location:
    latitude: float = 0.0
    longitude: float = 0.0
    country: str = ""
    region: str = ""
    city: str = ""

    @classmethod
    def from_pb(cls: Type[LocationT], src: pb.Location) -> LocationT:
        return cls(
            latitude=src.latitude,
            longitude=src.longitude,
            country=src.country,
            region=src.region,
            city=src.city,
        )


NetNodeT = TypeVar("NetNodeT", bound="NetNode")


@dataclass
class NetNode:
    ip: IP = IP()
    asn: int = 0
    as_name: str = ""
    location: Location = Location()
    dns_name: str = ""
    device_id: ID = ID()
    site_id: ID = ID()

    @classmethod
    def from_pb(cls: Type[NetNodeT], src: pb.NetNode) -> NetNodeT:
        return cls(
            ip=IP(src.ip),
            asn=src.asn,
            as_name=src.as_name,
            location=Location.from_pb(src.location),
            dns_name=src.dns_name,
            device_id=ID(src.device_id),
            site_id=ID(src.site_id),
        )


StatsT = TypeVar("StatsT", bound="Stats")


@dataclass
class Stats:
    average: int = 0
    min: int = 0
    max: int = 0

    @classmethod
    def from_pb(cls: Type[StatsT], src: pb.Stats) -> StatsT:
        return cls(average=src.average, min=src.min, max=src.max)


TraceHopT = TypeVar("TraceHopT", bound="TraceHop")


@dataclass
class TraceHop:
    latency: int = 0
    node_id: str = ""

    @classmethod
    def from_pb(cls: Type[TraceHopT], src: pb.TraceHop) -> TraceHopT:
        return cls(latency=src.latency, node_id=src.node_id)


PathTraceT = TypeVar("PathTraceT", bound="PathTrace")


@dataclass
class PathTrace:
    as_path: List[int] = field(default_factory=list)
    is_complete: bool = False
    hops: List[TraceHop] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[PathTraceT], src: pb.PathTrace) -> PathTraceT:
        return cls(
            as_path=src.as_path,
            is_complete=src.is_complete,
            hops=[TraceHop.from_pb(th) for th in src.hops],
        )


PathT = TypeVar("PathT", bound="Path")


@dataclass
class Path:
    agent_id: ID = ID()
    target_ip: IP = IP()
    hop_count: Stats = Stats()
    max_as_path_length: int = 0
    traces: List[PathTrace] = field(default_factory=list)
    time: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)

    @classmethod
    def from_pb(cls: Type[PathT], src: pb.Path) -> PathT:
        return cls(
            agent_id=ID(src.agent_id),
            target_ip=IP(src.target_ip),
            hop_count=Stats.from_pb(src.hop_count),
            max_as_path_length=src.max_as_path_length,
            traces=[PathTrace.from_pb(t) for t in src.traces],
            time=pb_to_datetime_utc(src.time),
        )


TraceResponseT = TypeVar("TraceResponseT", bound="TraceResponse")


@dataclass
class TraceResponse:
    nodes: Dict[str, NetNode] = field(default_factory=dict)
    paths: List[Path] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[TraceResponseT], src: pb.GetTraceForTestResponse) -> TraceResponseT:
        nodes = {k: NetNode.from_pb(v) for k, v in src.nodes.items()}
        paths = [Path.from_pb(p) for p in src.paths]
        return cls(nodes=nodes, paths=paths)
