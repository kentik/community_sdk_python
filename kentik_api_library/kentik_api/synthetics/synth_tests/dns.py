from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

from kentik_api.synthetics.types import *

from .base import SynTest, SynTestSettings, list_factory
from .protobuf_tools import pb_assign_collection


@dataclass
class DNSTestSpecific:
    target: str = ""
    timeout: int = 0
    record_type: DNSRecordType = DNSRecordType.A
    servers: List[str] = field(default_factory=list)
    port: int = 0

    def fill_from_pb(self, pb: pb.DnsTest) -> None:
        self.target = pb.target
        self.timeout = pb.timeout
        self.record_type = DNSRecordType(pb.record_type)
        self.servers = pb.servers
        self.port = pb.port

    def to_pb(self, pb: pb.DnsTest) -> None:
        pb.target = self.target
        pb.timeout = self.timeout
        pb.record_type = self.record_type.value
        pb_assign_collection(self.servers, pb.servers)
        pb.port = self.port


@dataclass
class DNSTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns: DNSTestSpecific = DNSTestSpecific()

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "dns"

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.dns.fill_from_pb(pb.dns)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.dns.to_pb(pb.dns)


DNSTestType = TypeVar("DNSTestType", bound="DNSTest")


@dataclass
class DNSTest(SynTest):
    type: TestType = field(init=False, default=TestType.DNS)
    settings: DNSTestSettings = field(default_factory=DNSTestSettings)

    @classmethod
    def create(
        cls: Type[DNSTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
        timeout: int = 5000,
        port: int = 53,
    ) -> DNSTestType:
        return cls(
            name=name,
            settings=DNSTestSettings(
                agent_ids=agent_ids,
                dns=DNSTestSpecific(
                    target=target, record_type=record_type, servers=servers, timeout=timeout, port=port
                ),
            ),
        )

    def set_timeout(self, timeout: int):
        self.settings.dns.timeout = timeout
