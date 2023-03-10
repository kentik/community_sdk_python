from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.synthetics.types import TaskType, TestType

from .base import PingTraceTest, PingTraceTestSettings, _ConfigElement, list_factory


@dataclass
class PageLoadTestSpecific(_ConfigElement):
    PB_TYPE = pb.PageLoadTest

    target: str = ""
    timeout: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    ignore_tls_errors: bool = False
    css_selectors: Dict[str, str] = field(default_factory=dict)


@dataclass
class PageLoadTestSettings(PingTraceTestSettings):
    tasks: List[TaskType] = field(default_factory=list_factory([TaskType.PAGE_LOAD]))
    page_load: PageLoadTestSpecific = field(default_factory=PageLoadTestSpecific)

    @classmethod
    def task_name(cls) -> Optional[str]:
        return "page-load"


PageLoadTestT = TypeVar("PageLoadTestT", bound="PageLoadTest")


@dataclass
class PageLoadTest(PingTraceTest):
    type: TestType = field(init=False, default=TestType.PAGE_LOAD)
    settings: PageLoadTestSettings = field(default_factory=PageLoadTestSettings)

    @classmethod
    def validate_http_timeout(cls: Type[PageLoadTestT], timeout: int):
        if timeout < 5000:
            raise RuntimeError(f"Invalid parameter value ({timeout}): {cls.type.value} test timeout must be >= 5000ms")

    @classmethod
    def create(
        cls: Type[PageLoadTestT],
        name: str,
        target: str,
        agent_ids: List[str],
        timeout: int = 5000,
        headers: Optional[Dict[str, str]] = None,
        css_selectors: Optional[Dict[str, str]] = None,
        ignore_tls_errors: bool = False,
        ping: bool = False,
        trace: bool = False,
    ) -> PageLoadTestT:
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
