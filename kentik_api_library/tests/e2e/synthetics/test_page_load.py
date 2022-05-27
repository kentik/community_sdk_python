import pytest

from kentik_api.synthetics.synth_tests import PageLoadTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.page_load import PageLoadTestSettings, PageLoadTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_page_load_crud() -> None:
    agents = pick_agent_ids(count=2, page_load_support=True)
    settings1 = PageLoadTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
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
    settings2 = PageLoadTestSettings(
        family=IPFamily.V6,
        period=120,
        agent_ids=[agents[1]],
        health_settings=HEALTH2,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE, TaskType.PAGE_LOAD],
        ping=PingTask(timeout=4000, count=6, delay=300, protocol=Protocol.ICMP, port=3333),
        trace=TraceTask(timeout=22750, count=4, limit=40, delay=30, protocol=Protocol.ICMP, port=4343),
        page_load=PageLoadTestSpecific(
            target="https://www.example.com",  # target can't be updated after test has been created
            timeout=8000,
            headers={"x-auth-token": "0FS230FJXGJK4234"},
            ignore_tls_errors=False,
            css_selectors={},
        ),
    )
    try:
        # create
        test = PageLoadTest("e2e-pageload-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, PageLoadTest)
        assert created_test.name == "e2e-pageload-test"
        assert created_test.type == TestType.PAGE_LOAD
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, PageLoadTest)
        assert received_test.name == "e2e-pageload-test"
        assert received_test.type == TestType.PAGE_LOAD
        assert received_test.status == TestStatus.ACTIVE
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-pageload-test-updated"
        created_test.settings = settings2
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, PageLoadTest)
        assert updated_test.name == "e2e-pageload-test-updated"
        assert updated_test.type == TestType.PAGE_LOAD
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
