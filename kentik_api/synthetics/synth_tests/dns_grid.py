from dataclasses import dataclass, field
from typing import List, Type, TypeVar

from kentik_api.synthetics.types import DNSRecordType, TaskType, TestType

from .base import SynTest, SynTestSettings, list_factory
from .dns import DNSTestSpecific

DSNGridTestSpecific = DNSTestSpecific


@dataclass
class DNSGridTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns_grid: DSNGridTestSpecific = DSNGridTestSpecific()


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
        timeout: int = 0,  # currently support for timeout attribute in DNS tests is suspended
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
