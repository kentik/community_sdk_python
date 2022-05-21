import pytest

from kentik_api.synthetics.synth_tests import UrlTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.url import UrlTestSettings, URLTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TaskType, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_url_crud() -> None:
    settings = UrlTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=pick_agent_ids(),
        health_settings=HEALTH,
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

    # create
    test = UrlTest("e2e-url-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.URL

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-url-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-url-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
