import pytest

from kentik_api.synthetics.synth_tests import PageLoadTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.page_load import PageLoadTestSettings, PageLoadTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_page_load_crud() -> None:
    settings = PageLoadTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=pick_agent_ids(count=1, page_load_support=True),
        health_settings=HEALTH,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE, TaskType.PAGE_LOAD],
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        page_load=PageLoadTestSpecific(
            target="https://www.example.com",
            timeout=7000,
            headers={"origin": "page-load-test"},
            ignore_tls_errors=True,
            css_selectors={"id": "#id", "class": ".class"},
        ),
    )

    # create
    test = PageLoadTest("e2e-pageload-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.PAGE_LOAD

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-pageload-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-pageload-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
