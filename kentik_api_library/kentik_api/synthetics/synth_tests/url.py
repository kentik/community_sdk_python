from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class URLTestSpecific(_ConfigElement):
    PB_TYPE = pb.UrlTest

    target: str = ""
    timeout: int = 0
    method: str = ""  # HTTP method
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    ignore_tls_errors: bool = False


@dataclass
class UrlTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.HTTP]))
    url: URLTestSpecific = field(default_factory=URLTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "http"


UrlTestT = TypeVar("UrlTestT", bound="UrlTest")


@dataclass
class UrlTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.URL)
    settings: UrlTestSettings = field(default_factory=UrlTestSettings)

    @classmethod
    def validate_http_timeout(cls: Type[UrlTestT], timeout: int):
        if timeout < 5000:
            raise RuntimeError(f"Invalid parameter value ({timeout}): {cls.type.value} test timeout must be >= 5000ms")

    @classmethod
    def create(
        cls: Type[UrlTestT],
        name: str,
        target: str,
        agent_ids: List[str],
        timeout: int = 5000,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: str = "",
        ignore_tls_errors: bool = False,
        ping: bool = False,
        trace: bool = False,
    ) -> UrlTestT:
        tasks: List[TaskType] = [TaskType.HTTP]
        if ping:
            tasks.append(TaskType.PING)
        if trace:
            tasks.append(TaskType.TRACE_ROUTE)
        cls.validate_http_timeout(timeout)
        return cls(
            name=name,
            settings=UrlTestSettings(
                agent_ids=agent_ids,
                url=URLTestSpecific(
                    target=target,
                    timeout=timeout,
                    method=method,
                    body=body,
                    headers=headers or {},
                    ignore_tls_errors=ignore_tls_errors,
                ),
                tasks=tasks,
            ),
        )

    def set_timeout(self, timeout: int):
        self.validate_http_timeout(timeout)
        self.settings.url.timeout = timeout
