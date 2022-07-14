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
    PB_TYPE = pb.Agent

    # read-only
    _os: str = ""
    _version: str = ""
    _test_ids: List[ID] = field(default_factory=list)
    _type: AgentOwnershipType = AgentOwnershipType.NONE
    _agent_impl: AgentImplementType = AgentImplementType.UNSPECIFIED
    _last_authed: DateTime = DateTime.fromtimestamp(0, tz=timezone.utc)

    # read-write
    id: ID = ID()  # id is written in agent update request
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
    labels: List[str] = field(default_factory=list)

    @property
    def os(self) -> str:
        return self._os

    @property
    def version(self) -> str:
        return self._version

    @property
    def test_ids(self) -> List[ID]:
        return self._test_ids

    @property
    def type(self) -> AgentOwnershipType:
        return self._type

    @property
    def agent_impl(self) -> AgentImplementType:
        return self._agent_impl

    @property
    def last_authed(self) -> DateTime:
        return self._last_authed

    @property
    def is_private(self) -> bool:
        return self.type == AgentOwnershipType.PRIVATE

    @property
    def is_app_agent(self) -> bool:
        return self.agent_impl == AgentImplementType.NODE
