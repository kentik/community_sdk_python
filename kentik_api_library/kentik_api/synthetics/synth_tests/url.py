from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory
from .protobuf_tools import pb_assign_map


@dataclass
class URLTestSpecific:
    target: str = ""
    timeout: int = 0
    http_method: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    body: str = ""
    ignore_tls_errors: bool = False

    def fill_from_pb(self, pb: pb.UrlTest) -> None:
        self.target = pb.target
        self.timeout = pb.timeout
        self.http_method = pb.method
        self.headers = pb.headers
        self.body = pb.body
        self.ignore_tls_errors = pb.ignore_tls_errors

    def to_pb(self, pb: pb.UrlTest) -> None:
        pb.target = self.target
        pb.timeout = self.timeout
        pb.method = self.http_method
        pb_assign_map(self.headers, pb.headers)
        pb.body = self.body
        pb.ignore_tls_errors = self.ignore_tls_errors


@dataclass
class UrlTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.HTTP]))
    url: URLTestSpecific = field(default_factory=URLTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "http"

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.url.fill_from_pb(pb.url)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.url.to_pb(pb.url)


UrlTestType = TypeVar("UrlTestType", bound="UrlTest")


@dataclass
class UrlTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.URL)
    settings: UrlTestSettings = field(default_factory=UrlTestSettings)

    @classmethod
    def validate_http_timeout(cls: Type[UrlTestType], timeout: int):
        if timeout < 5000:
            raise RuntimeError(f"Invalid parameter value ({timeout}): {cls.type.value} test timeout must be >= 5000ms")

    @classmethod
    def create(
        cls: Type[UrlTestType],
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
    ) -> UrlTestType:
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
