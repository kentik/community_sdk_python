from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DNSRecordType, TaskType, TestType

from .base import SynTest, SynTestSettings, list_factory


@dataclass
class DNSTestSpecific:
    target: str = ""
    timeout: int = 0  # currently support for timeout attribute in DNS tests is suspended
    record_type: DNSRecordType = DNSRecordType.A
    servers: List[str] = field(default_factory=list)
    port: int = 0

    def fill_from_pb(self, src: pb.DnsTest) -> None:
        self.target = src.target
        self.timeout = src.timeout
        self.record_type = DNSRecordType(src.record_type)
        self.servers = src.servers
        self.port = src.port

    def to_pb(self) -> pb.DnsTest:
        return pb.DnsTest(
            target=self.target,
            timeout=self.timeout,
            record_type=self.record_type.value,
            servers=self.servers,
            port=self.port,
        )


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

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.dns.CopyFrom(self.dns.to_pb())
        return obj


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
        timeout: int = 0,  # currently support for timeout attribute in DNS tests is suspended
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
