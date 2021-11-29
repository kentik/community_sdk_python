from dataclasses import dataclass
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
    id: ID  # "574"
    name: str  # "Linode,US (63949)"
    status: AgentStatus  # "AGENT_STATUS_OK"
    alias: str  # "Tokyo, Japan"
    type: str  # "global"
    os: str  # ""
    ip: str  # "139.162.75.56"
    lat: float  # 35.689506
    long: float  # 139.6917
    last_authored: str  # "2021-11-29T10:  #09:  #34.742Z"
    family: IPFamily  # "IP_FAMILY_DUAL"
    asn: int  # 63949
    site_id: ID  # "0"
    version: str  # "0.0.17"
    challenge: str  # ""
    city: str  # "Tokyo"
    region: str  # ""
    country: str  # "JP"
    test_ids: List[ID]  # []
    local_ip: str  # ""
    cloud_vpc: str  # ""
    agent_impl: AgentImplementType  # "IMPLEMENT_TYPE_RUST"
