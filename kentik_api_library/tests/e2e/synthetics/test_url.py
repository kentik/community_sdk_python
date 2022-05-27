import pytest

from kentik_api.synthetics.synth_tests import UrlTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.url import UrlTestSettings, URLTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_url_crud() -> None:
    agents = pick_agent_ids(count=2)
    settings1 = UrlTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE, TaskType.HTTP],
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        url=URLTestSpecific(
            target="https://www.example.com",
            timeout=7000,
            http_method="GET",
            headers={"origin": "url-test"},
            body="BODY",
            ignore_tls_errors=False,
        ),
    )
    settings2 = UrlTestSettings(
        family=IPFamily.V6,
        period=120,
        agent_ids=[agents[1]],
        health_settings=HEALTH2,
        tasks=[TaskType.PING, TaskType.TRACE_ROUTE],
        ping=PingTask(timeout=4000, count=6, delay=300, protocol=Protocol.ICMP, port=3333),
        trace=TraceTask(timeout=22750, count=4, limit=40, delay=30, protocol=Protocol.ICMP, port=4343),
        url=URLTestSpecific(
            target="https://www.example.com",  # target can't be updated after a test has been created
            timeout=8000,
            http_method="GET",  # Method can't be updated after a test has been created
            headers={"api-key": "KLAJ34AJFDHLAK653LXL"},
            body="",
            ignore_tls_errors=True,
        ),
    )
    try:
        # create
        test = UrlTest("e2e-url-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, UrlTest)
        assert created_test.name == "e2e-url-test"
        assert created_test.type == TestType.URL
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, UrlTest)
        assert received_test.name == "e2e-url-test"
        assert received_test.type == TestType.URL
        assert received_test.status == TestStatus.ACTIVE
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-url-test-updated"
        created_test.settings = settings2
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, UrlTest)
        assert updated_test.name == "e2e-url-test-updated"
        assert updated_test.type == TestType.URL
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
