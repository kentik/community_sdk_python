from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.synthetics.types import *

from .base import SynTest, SynTestSettings, list_factory
from .protobuf_tools import pb_assign_collection


@dataclass
class DSNGridTestSpecific:
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
class DNSGridTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns_grid: DSNGridTestSpecific = DSNGridTestSpecific()

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.dns_grid.fill_from_pb(pb.dns_grid)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.dns_grid.to_pb(pb.dns_grid)


DNSGridTestType = TypeVar("DNSGridTestType", bound="DNSGridTest")


@dataclass
class DNSGridTest(SynTest):
    type: TestType = field(init=False, default=TestType.DNS_GRID)
    settings: DNSGridTestSettings = field(default_factory=DNSGridTestSettings)

    @classmethod
    def create(
        cls: Type[DNSGridTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
        timeout: int = 5000,
        port: int = 53,
    ) -> DNSGridTestType:
        return cls(
            name=name,
            settings=DNSGridTestSettings(
                agent_ids=agent_ids,
                dns_grid=DSNGridTestSpecific(
                    target=target, record_type=record_type, servers=servers, timeout=timeout, port=port
                ),
            ),
        )

    def set_timeout(self, timeout: int):
        self.settings.dns_grid.timeout = timeout
