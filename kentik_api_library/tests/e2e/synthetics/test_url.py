from copy import deepcopy

import pytest

from kentik_api.synthetics.synth_tests import UrlTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.url import UrlTestSettings, URLTestSpecific
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
def test_url_crud() -> None:
    agents = pick_agent_ids(count=2)
    initial_settings = UrlTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=INITIAL_HEALTH_SETTINGS,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE, TaskType.HTTP],
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        url=URLTestSpecific(
            target="https://www.example.com",
            timeout=7000,
            method="GET",
            headers={"origin": "url-test"},
            body="BODY",
            ignore_tls_errors=False,
        ),
    )
    update_settings = deepcopy(initial_settings)
    update_settings.family = IPFamily.V6
    update_settings.period = 120
    update_settings.agent_ids = [agents[1]]
    update_settings.health_settings = UPDATE_HEALTH_SETTINGS
    update_settings.tasks = [TaskType.PING, TaskType.TRACE_ROUTE]
    update_settings.ping.timeout = 4000
    update_settings.ping.count = 6
    update_settings.ping.delay = 300
    update_settings.trace.timeout = 22750
    update_settings.trace.count = 4
    update_settings.trace.limit = 40
    update_settings.trace.delay = 30
    update_settings.trace.protocol = Protocol.ICMP
    # update_settings.url.target="https://www.wikipedia.org"  # target can't be updated after a test has been created
    update_settings.url.timeout = 8000
    # update_settings.url.http_method = "HEAD"  # Method can't be updated after a test has been created
    update_settings.url.headers = {"api-key": "KLAJ34AJFDHLAK653LXL"}
    update_settings.url.body = ""
    update_settings.url.ignore_tls_errors = True

    test = UrlTest(make_e2e_test_name(TestType.URL), TestStatus.ACTIVE, initial_settings)

    execute_test_crud_steps(test, update_settings=update_settings)
