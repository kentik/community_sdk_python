from dataclasses import dataclass, field
from datetime import timezone
from typing import List, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP
from kentik_api.synthetics.synth_tests.base import DateTime, _ConfigElement
from kentik_api.synthetics.types import IPFamily, SerializableEnum


class AgentStatus(SerializableEnum):
    UNSPECIFIED = pb.AgentStatus.AGENT_STATUS_UNSPECIFIED
    OK = pb.AgentStatus.AGENT_STATUS_OK
    WAIT = pb.AgentStatus.AGENT_STATUS_WAIT
    DELETED = pb.AgentStatus.AGENT_STATUS_DELETED


class AgentImplementType(SerializableEnum):
    UNSPECIFIED = pb.ImplementType.IMPLEMENT_TYPE_UNSPECIFIED
    RUST = pb.ImplementType.IMPLEMENT_TYPE_RUST
    NODE = pb.ImplementType.IMPLEMENT_TYPE_NODE


class AgentOwnershipType(SerializableEnum):
    NONE = ""
    PRIVATE = "private"
    GLOBAL = "global"


AgentT = TypeVar("AgentT", bound="Agent")


@dataclass
class Agent(_ConfigElement):
    # read-only
    type: AgentOwnershipType = AgentOwnershipType.NONE
    os: str = ""
    last_authed: DateTime = DateTime.fromtimestamp(0, tz=timezone.utc)
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
        """
        Need only to serialize the read-write fields; so can't use the  _ConfigElement.to_pb() method that serializes all fields
        """

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
