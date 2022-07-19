from copy import deepcopy

import pytest

from kentik_api.synthetics.synth_tests import PageLoadTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.page_load import PageLoadTestSettings, PageLoadTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

from .utils import (
    INITIAL_HEALTH_SETTINGS,
    UPDATE_HEALTH_SETTINGS,
    credentials_missing_str,
    credentials_present,
    execute_test_crud_steps,
    make_e2e_test_name,
    pick_agent_ids,
)


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_page_load_crud(test_labels, notification_channels) -> None:
    agents = pick_agent_ids(count=2, page_load_support=True)
    initial_settings = PageLoadTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=INITIAL_HEALTH_SETTINGS,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE, TaskType.PAGE_LOAD],
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        page_load=PageLoadTestSpecific(
            target="https://www.example.com",
            timeout=7000,
            headers={"origin": "page-load-test"},
            ignore_tls_errors=True,
            css_selectors={"id": "#id", "class": ".class"},
        ),
        notification_channels=notification_channels,
    )
    update_settings = deepcopy(initial_settings)
    update_settings.family = IPFamily.V6
    update_settings.period = 120
    update_settings.agent_ids = [agents[1]]
    update_settings.health_settings = UPDATE_HEALTH_SETTINGS
    update_settings.tasks = [TaskType.PING, TaskType.TRACE_ROUTE, TaskType.PAGE_LOAD]
    update_settings.ping.timeout = 4000
    update_settings.ping.count = 6
    update_settings.ping.delay = 300
    update_settings.trace.timeout = 22750
    update_settings.trace.count = 4
    update_settings.trace.limit = 40
    update_settings.trace.delay = 30
    update_settings.trace.protocol = Protocol.ICMP
    # update_settings.page_load.target="https://www.wikipedia.org"  # target can't be updated after test has been created
    update_settings.page_load.timeout = 8000
    update_settings.page_load.headers = {"x-auth-token": "0FS230FJXGJK4234"}
    update_settings.page_load.ignore_tls_errors = False
    update_settings.page_load.css_selectors = {}
    update_settings.notification_channels = []

    test = PageLoadTest(make_e2e_test_name(TestType.PAGE_LOAD), TestStatus.ACTIVE, initial_settings)
    test.labels = test_labels

    execute_test_crud_steps(test, update_settings=update_settings)
