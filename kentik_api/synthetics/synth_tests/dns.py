from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import DNSRecordType, TaskType, TestType

from .base import SynTest, SynTestSettings, _ConfigElement, list_factory


@dataclass
class DNSTestSpecific(_ConfigElement):
    PB_TYPE = pb.DnsTest

    target: str = ""
    timeout: int = 0  # currently support for timeout attribute in DNS tests is suspended
    record_type: DNSRecordType = DNSRecordType.A
    servers: List[str] = field(default_factory=list)
    port: int = 0


@dataclass
class DNSTestSettings(SynTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.DNS]))
    dns: DNSTestSpecific = DNSTestSpecific()

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "dns"


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
                    target=target,
                    record_type=record_type,
                    servers=servers,
                    timeout=timeout,
                    port=port,
                ),
            ),
        )

    def set_timeout(self, timeout: int):
        self.settings.dns.timeout = timeout
