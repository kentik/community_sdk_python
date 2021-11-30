from dataclasses import dataclass, field
from enum import Enum
from typing import List

from kentik_api.public.types import ID, IP

from .synth_tests import IPFamily


class AgentStatus(Enum):
    UNSPECIFIED = "AGENT_STATUS_UNSPECIFIED"
    OK = "AGENT_STATUS_OK"
    WAIT = "AGENT_STATUS_WAIT"
    DELETED = "AGENT_STATUS_DELETED"


class AgentImplementType(Enum):
    UNSPECIFIED = "IMPLEMENT_TYPE_UNSPECIFIED"
    RUST = "IMPLEMENT_TYPE_RUST"
    NODE = "IMPLEMENT_TYPE_NODE"


@dataclass
class Agent:
    id: ID = ID()
    name: str = ""
    status: AgentStatus = AgentStatus.UNSPECIFIED
    alias: str = ""
    type: str = ""  # "global"
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
