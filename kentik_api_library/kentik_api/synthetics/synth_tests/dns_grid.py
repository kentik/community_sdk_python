from dataclasses import dataclass, field
from typing import List, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DNSRecordType, TaskType, TestType

from .base import SynTest, SynTestSettings, list_factory
from .dns import DNSTestSpecific

DSNGridTestSpecific = DNSTestSpecific


@dataclass
class DNSGridTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns_grid: DSNGridTestSpecific = DSNGridTestSpecific()

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.dns_grid.fill_from_pb(src.dns_grid)

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.dns_grid.CopyFrom(self.dns_grid.to_pb())
        return obj


DNSGridTestT = TypeVar("DNSGridTestT", bound="DNSGridTest")


@dataclass
class DNSGridTest(SynTest):
    type: TestType = field(init=False, default=TestType.DNS_GRID)
    settings: DNSGridTestSettings = field(default_factory=DNSGridTestSettings)

    @classmethod
    def create(
        cls: Type[DNSGridTestT],
        name: str,
        target: str,
        agent_ids: List[str],
        servers: List[str],
        record_type: DNSRecordType = DNSRecordType.A,
        timeout: int = 5000,
        port: int = 53,
    ) -> DNSGridTestT:
        return cls(
            name=name,
            settings=DNSGridTestSettings(
                agent_ids=agent_ids,
                dns_grid=DSNGridTestSpecific(
                    target=target,
                    record_type=record_type,
                    servers=servers,
                    timeout=timeout,
                    port=port,
                ),
            ),
        )

    def set_timeout(self, timeout: int):
        self.settings.dns_grid.timeout = timeout
