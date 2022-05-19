from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_to_datetime_utc
from kentik_api.synthetics.types import IPFamily


class AgentStatus(Enum):
    UNSPECIFIED = pb.AgentStatus.AGENT_STATUS_UNSPECIFIED
    OK = pb.AgentStatus.AGENT_STATUS_OK
    WAIT = pb.AgentStatus.AGENT_STATUS_WAIT
    DELETED = pb.AgentStatus.AGENT_STATUS_DELETED


class AgentImplementType(Enum):
    UNSPECIFIED = pb.ImplementType.IMPLEMENT_TYPE_UNSPECIFIED
    RUST = pb.ImplementType.IMPLEMENT_TYPE_RUST
    NODE = pb.ImplementType.IMPLEMENT_TYPE_NODE


class AgentOwnershipType(Enum):
    NONE = ""
    PRIVATE = "private"
    GLOBAL = "global"


AgentT = TypeVar("AgentT", bound="Agent")


@dataclass
class Agent:
    # read-only
    type: AgentOwnershipType = AgentOwnershipType.NONE
    os: str = ""
    last_authed: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)
    test_ids: List[ID] = field(default_factory=list)
    version: str = ""
    agent_impl: AgentImplementType = AgentImplementType.UNSPECIFIED

    # read-write
    id: ID = ID()
    site_name: str = ""
    status: AgentStatus = AgentStatus.UNSPECIFIED
    alias: str = ""
    ip: IP = IP()
    lat: float = 0.0
    long: float = 0.0
    family: IPFamily = IPFamily.UNSPECIFIED
    asn: int = 0
    site_id: ID = ID()
    city: str = ""
    region: str = ""
    country: str = ""
    local_ip: IP = IP()
    cloud_region: str = ""
    cloud_provider: str = ""

    def to_pb(self) -> pb.Agent:
        return pb.Agent(
            id=str(self.id),
            site_name=self.site_name,
            status=self.status.value,
            alias=self.alias,
            ip=str(self.ip),
            lat=self.lat,
            long=self.long,
            family=self.family.value,
            asn=self.asn,
            site_id=str(self.site_id),
            city=self.city,
            region=self.region,
            country=self.country,
            local_ip=str(self.local_ip),
            cloud_region=self.cloud_region,
            cloud_provider=self.cloud_provider,
        )

    @classmethod
    def from_pb(cls: Type[AgentT], pba: pb.Agent) -> AgentT:
        return cls(
            id=ID(pba.id),
            site_name=pba.site_name,
            status=AgentStatus(pba.status),
            alias=pba.alias,
            type=AgentOwnershipType(pba.type),
            os=pba.os,
            ip=IP(pba.ip),
            lat=pba.lat,
            long=pba.long,
            last_authed=pb_to_datetime_utc(pba.last_authed),
            family=IPFamily(pba.family),
            asn=pba.asn,
            site_id=ID(pba.site_id),
            version=pba.version,
            city=pba.city,
            region=pba.region,
            country=pba.country,
            test_ids=[ID(id) for id in pba.test_ids],
            local_ip=IP(pba.local_ip),
            cloud_region=pba.cloud_region,
            cloud_provider=pba.cloud_provider,
            agent_impl=AgentImplementType(pba.agent_impl),
        )
