from dataclasses import dataclass, field
from enum import Enum
from typing import List

from kentik_api.public.types import ID

from .synth_tests import IPFamily


class AgentStatus(Enum):
    unspecified = "AGENT_STATUS_UNSPECIFIED"
    ok = "AGENT_STATUS_OK"
    wait = "AGENT_STATUS_WAIT"
    deleted = "AGENT_STATUS_DELETED"


class AgentImplementType(Enum):
    unspecified = "IMPLEMENT_TYPE_UNSPECIFIED"
    rust = "IMPLEMENT_TYPE_RUST"
    node = "IMPLEMENT_TYPE_NODE"


@dataclass
class Agent:
    id: ID = ID("")
    name: str = ""
    status: AgentStatus = AgentStatus.unspecified
    alias: str = ""
    type: str = ""  # "global"
    os: str = ""
    ip: str = ""
    lat: float = 0.0
    long: float = 0.0
    last_authed: str = ""
    family: IPFamily = IPFamily.unspecified
    asn: int = 0
    site_id: ID = ID("0")
    version: str = ""
    challenge: str = ""
    city: str = ""
    region: str = ""
    country: str = ""
    test_ids: List[ID] = field(default_factory=list)
    local_ip: str = ""
    cloud_vpc: str = ""
    agent_impl: AgentImplementType = AgentImplementType.unspecified
