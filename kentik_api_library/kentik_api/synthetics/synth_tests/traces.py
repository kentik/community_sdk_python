from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc

LocationType = TypeVar("LocationType", bound="Location")


@dataclass
class Location:
    latitude: float = 0.0
    longitude: float = 0.0
    country: str = ""
    region: str = ""
    city: str = ""

    @classmethod
    def from_pb(cls: Type[LocationType], pb: pb.Location) -> LocationType:
        return cls(
            latitude=pb.latitude,
            longitude=pb.longitude,
            country=pb.country,
            region=pb.region,
            city=pb.city,
        )


NetNodeType = TypeVar("NetNodeType", bound="NetNode")


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
    def from_pb(cls: Type[NetNodeType], pb: pb.NetNode) -> NetNodeType:
        return cls(
            ip=IP(pb.ip),
            asn=pb.asn,
            as_name=pb.as_name,
            location=Location.from_pb(pb.location),
            dns_name=pb.dns_name,
            device_id=ID(pb.device_id),
            site_id=ID(pb.site_id),
        )


StatsType = TypeVar("StatsType", bound="Stats")


@dataclass
class Stats:
    average: int = 0
    min: int = 0
    max: int = 0

    @classmethod
    def from_pb(cls: Type[StatsType], pb: pb.Stats) -> StatsType:
        return cls(average=pb.average, min=pb.min, max=pb.max)


TraceHopType = TypeVar("TraceHopType", bound="TraceHop")


@dataclass
class TraceHop:
    latency: int = 0
    node_id: str = ""

    @classmethod
    def from_pb(cls: Type[TraceHopType], pb: pb.TraceHop) -> TraceHopType:
        return cls(latency=pb.latency, node_id=pb.node_id)


PathTraceType = TypeVar("PathTraceType", bound="PathTrace")


@dataclass
class PathTrace:
    as_path: List[int] = field(default_factory=list)
    is_complete: bool = False
    hops: List[TraceHop] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[PathTraceType], pb: pb.PathTrace) -> PathTraceType:
        return cls(
            as_path=pb.as_path,
            is_complete=pb.is_complete,
            hops=[TraceHop.from_pb(th) for th in pb.hops],
        )


PathType = TypeVar("PathType", bound="Path")


@dataclass
class Path:
    agent_id: ID = ID()
    target_ip: IP = IP()
    hop_count: Stats = Stats()
    max_as_path_length: int = 0
    traces: List[PathTrace] = field(default_factory=list)
    time: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)

    @classmethod
    def from_pb(cls: Type[PathType], pb: pb.Path) -> PathType:
        return cls(
            agent_id=ID(pb.agent_id),
            target_ip=IP(pb.target_ip),
            hop_count=Stats.from_pb(pb.hop_count),
            max_as_path_length=pb.max_as_path_length,
            traces=[PathTrace.from_pb(t) for t in pb.traces],
            time=pb_to_datetime_utc(pb.time),
        )


TraceResponseType = TypeVar("TraceResponseType", bound="TraceResponse")


@dataclass
class TraceResponse:
    nodes: Dict[str, NetNode] = field(default_factory=dict)
    paths: List[Path] = field(default_factory=list)

    @classmethod
    def from_pb(cls: Type[TraceResponseType], pb: pb.GetTraceForTestResponse) -> TraceResponseType:
        nodes = {k: NetNode.from_pb(v) for k, v in pb.nodes.items()}
        paths = [Path.from_pb(p) for p in pb.paths]
        return cls(nodes=nodes, paths=paths)
