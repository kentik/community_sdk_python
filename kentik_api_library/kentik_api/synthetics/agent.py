from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.defaults import DEFAULT_DATE_NO_ZULU
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.protobuf_tools import pb_from_datetime, pb_to_datetime_utc
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


AgentType = TypeVar("AgentType", bound="Agent")


@dataclass
class Agent:
    id: ID = ID()
    site_name: str = ""
    status: AgentStatus = AgentStatus.UNSPECIFIED
    alias: str = ""
    type: AgentOwnershipType = AgentOwnershipType.NONE
    os: str = ""
    ip: IP = IP()
    lat: float = 0.0
    long: float = 0.0
    last_authed: datetime = datetime.fromisoformat(DEFAULT_DATE_NO_ZULU)
    family: IPFamily = IPFamily.UNSPECIFIED
    asn: int = 0
    site_id: ID = ID()
    version: str = ""
    city: str = ""
    region: str = ""
    country: str = ""
    test_ids: List[ID] = field(default_factory=list)
    local_ip: IP = IP()
    cloud_region: str = ""
    cloud_provider: str = ""
    agent_impl: AgentImplementType = AgentImplementType.UNSPECIFIED

    def to_pb(self) -> pb.Agent:
        return pb.Agent(
            id=str(self.id),
            site_name=self.site_name,
            status=self.status.value,
            alias=self.alias,
            type=self.type.value,
            os=self.os,
            ip=str(self.ip),
            lat=self.lat,
            long=self.long,
            last_authed=pb_from_datetime(self.last_authed),
            family=self.family.value,
            asn=self.asn,
            site_id=str(self.site_id),
            version=self.version,
            city=self.city,
            region=self.region,
            country=self.country,
            test_ids=[str(id) for id in self.test_ids],
            local_ip=str(self.local_ip),
            cloud_region=self.cloud_region,
            cloud_provider=self.cloud_provider,
            agent_impl=self.agent_impl.value,
        )

    @classmethod
    def from_pb(cls: Type[AgentType], pb: pb.Agent) -> AgentType:
        return cls(
            id=ID(pb.id),
            site_name=pb.site_name,
            status=AgentStatus(pb.status),
            alias=pb.alias,
            type=AgentOwnershipType(pb.type),
            os=pb.os,
            ip=IP(pb.ip),
            lat=pb.lat,
            long=pb.long,
            last_authed=pb_to_datetime_utc(pb.last_authed),
            family=IPFamily(pb.family),
            asn=pb.asn,
            site_id=ID(pb.site_id),
            version=pb.version,
            city=pb.city,
            region=pb.region,
            country=pb.country,
            test_ids=[ID(id) for id in pb.test_ids],
            local_ip=IP(pb.local_ip),
            cloud_region=pb.cloud_region,
            cloud_provider=pb.cloud_provider,
            agent_impl=AgentImplementType(pb.agent_impl),
        )
