from dataclasses import dataclass, field
from enum import Enum
from typing import List

import kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 as pb
from kentik_api.public.types import ID, IP

from .synth_tests import IPFamily


class AgentStatus(Enum):
    UNSPECIFIED = pb.AgentStatus.AGENT_STATUS_UNSPECIFIED
    OK = pb.AgentStatus.AGENT_STATUS_OK
    WAIT = pb.AgentStatus.AGENT_STATUS_WAIT
    DELETED = pb.AgentStatus.AGENT_STATUS_DELETED


class AgentImplementType(Enum):
    UNSPECIFIED = pb.ImplementType.IMPLEMENT_TYPE_UNSPECIFIED
    RUST = pb.ImplementType.IMPLEMENT_TYPE_RUST
    NODE = pb.ImplementType.IMPLEMENT_TYPE_NODE


class AgentType(Enum):
    PRIVATE = "private"
    GLOBAL = "global"


@dataclass
class Agent:
    id: ID = ID()
    name: str = ""
    status: AgentStatus = AgentStatus.UNSPECIFIED
    alias: str = ""
    type: AgentType = AgentType.GLOBAL
    os: str = ""
    ip: IP = IP()
    lat: float = 0.0
    long: float = 0.0
    last_authed: str = ""
    family: IPFamily = IPFamily.unspecified
    asn: int = 0
    site_id: ID = ID()
    version: str = ""
    challenge: str = ""
    city: str = ""
    region: str = ""
    country: str = ""
    test_ids: List[ID] = field(default_factory=list)
    local_ip: IP = IP()
    cloud_vpc: str = ""
    agent_impl: AgentImplementType = AgentImplementType.UNSPECIFIED
