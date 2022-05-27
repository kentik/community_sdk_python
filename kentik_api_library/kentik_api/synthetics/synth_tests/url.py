from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, list_factory


@dataclass
class URLTestSpecific:
    target: str = ""
    timeout: int = 0
    http_method: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    ignore_tls_errors: bool = False

    def fill_from_pb(self, src: pb.UrlTest) -> None:
        self.target = src.target
        self.timeout = src.timeout
        self.http_method = src.method
        self.headers = src.headers
        self.body = src.body
        self.ignore_tls_errors = src.ignore_tls_errors

    def to_pb(self) -> pb.UrlTest:
        return pb.UrlTest(
            target=self.target,
            timeout=self.timeout,
            method=self.http_method,
            headers=self.headers,
            body=self.body,
            ignore_tls_errors=self.ignore_tls_errors,
        )


@dataclass
class UrlTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.HTTP]))
    url: URLTestSpecific = field(default_factory=URLTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "http"

    def fill_from_pb(self, src: pb.TestSettings) -> None:
        super().fill_from_pb(src)
        self.url.fill_from_pb(src.url)

    def to_pb(self) -> pb.TestSettings:
        obj = super().to_pb()
        obj.url.CopyFrom(self.url.to_pb())
        return obj


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
                    http_method=method,
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
