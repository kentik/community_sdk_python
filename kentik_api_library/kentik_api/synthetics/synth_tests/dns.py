from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DNSRecordType, TaskType, TestType

from .base import SynTest, SynTestSettings, list_factory
from .protobuf_tools import pb_assign_collection


@dataclass
class DNSTestSpecific:
    target: str = ""
    timeout: int = 0
    record_type: DNSRecordType = DNSRecordType.A
    servers: List[str] = field(default_factory=list)
    port: int = 0

    def fill_from_pb(self, src: pb.DnsTest) -> None:
        self.target = src.target
        self.timeout = src.timeout
        self.record_type = DNSRecordType(src.record_type)
        self.servers = src.servers
        self.port = src.port

    def to_pb(self, dst: pb.DnsTest) -> None:
        dst.target = self.target
        dst.timeout = self.timeout
        dst.record_type = self.record_type.value
        pb_assign_collection(self.servers, dst.servers)
        dst.port = self.port


@dataclass
class DNSTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns: DNSTestSpecific = DNSTestSpecific()

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "dns"

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.dns.fill_from_pb(src.dns)

    def to_pb(self, dst: pb.TestSettings) -> None:
        super().to_pb(dst)
        self.dns.to_pb(dst.dns)


DNSTestT = TypeVar("DNSTestT", bound="DNSTest")


@dataclass
class DNSTest(SynTest):
    type: TestType = field(init=False, default=TestType.DNS)
    settings: DNSTestSettings = field(default_factory=DNSTestSettings)

    @classmethod
    def create(
        cls: Type[DNSTestT],
        name: str,
        target: str,
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
        timeout: int = 5000,
        port: int = 53,
    ) -> DNSTestT:
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
