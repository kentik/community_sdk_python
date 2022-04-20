from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

from kentik_api.synthetics.types import *

from .base import PingTraceTest, PingTraceTestSettings, list_factory
from .protobuf_tools import pb_assign_map


@dataclass
class PageLoadTestSpecific:
    target: str = ""
    timeout: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    ignore_tls_errors: bool = False
    css_selectors: Dict[str, str] = field(default_factory=dict)

    def fill_from_pb(self, pb: pb.PageLoadTest) -> None:
        self.target = pb.target
        self.timeout = pb.timeout
        self.headers = pb.headers
        self.ignore_tls_errors = pb.ignore_tls_errors
        self.css_selectors = pb.css_selectors

    def to_pb(self, pb: pb.PageLoadTest) -> None:
        pb.target = self.target
        pb.timeout = self.timeout
        pb_assign_map(self.headers, pb.headers)
        pb.ignore_tls_errors = self.ignore_tls_errors
        pb_assign_map(self.css_selectors, pb.css_selectors)


@dataclass
class PageLoadTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PAGE_LOAD]))
    page_load: PageLoadTestSpecific = field(default_factory=PageLoadTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "page-load"

    def fill_from_pb(self, pb: pb.TestSettings) -> None:
        super().fill_from_pb(pb)
        self.page_load.fill_from_pb(pb.page_load)

    def to_pb(self, pb: pb.TestSettings) -> None:
        super().to_pb(pb)
        self.page_load.to_pb(pb.page_load)


PageLoadTestType = TypeVar("PageLoadTestType", bound="PageLoadTest")


@dataclass
class PageLoadTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.PAGE_LOAD)
    settings: PageLoadTestSettings = field(default_factory=PageLoadTestSettings)

    @classmethod
    def validate_http_timeout(cls: Type[PageLoadTestType], timeout: int):
        if timeout < 5000:
            raise RuntimeError(f"Invalid parameter value ({timeout}): {cls.type.value} test timeout must be >= 5000ms")

    @classmethod
    def create(
        cls: Type[PageLoadTestType],
        name: str,
        target: str,
        agent_ids: List[str],
        timeout: int = 5000,
        headers: Optional[Dict[str, str]] = None,
        css_selectors: Optional[Dict[str, str]] = None,
        ignore_tls_errors: bool = False,
        ping: bool = False,
        trace: bool = False,
    ) -> PageLoadTestType:
        tasks: List[TaskType] = [TaskType.PAGE_LOAD]
        if ping:
            tasks.append(TaskType.PING)
        if trace:
            tasks.append(TaskType.TRACE_ROUTE)
        cls.validate_http_timeout(timeout)
        return cls(
            name=name,
            settings=PageLoadTestSettings(
                agent_ids=agent_ids,
                page_load=PageLoadTestSpecific(
                    target=target,
                    timeout=timeout,
                    headers=headers or {},
                    css_selectors=css_selectors or {},
                    ignore_tls_errors=ignore_tls_errors,
                ),
                tasks=tasks,
            ),
        )

    def set_timeout(self, timeout: int):
        self.validate_http_timeout(timeout)
        self.settings.page_load.timeout = timeout
