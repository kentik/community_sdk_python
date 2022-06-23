from copy import deepcopy

import pytest

from kentik_api.public.types import IP
from kentik_api.synthetics.synth_tests import IPTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.ip import IPTestSettings, IPTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_ip_crud() -> None:
    agents = pick_agent_ids(count=2)
    settings1 = IPTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        ip=IPTestSpecific(targets=[IP("54.161.222.85"), IP("34.205.242.146")]),
    )
    settings2 = deepcopy(settings1)
    settings2.family = IPFamily.V6
    # settings2.period = 120  # period update doesn't take effect
    settings2.agent_ids = [agents[1]]
    settings2.health_settings = HEALTH2
    settings2.ping.timeout = 4000
    settings2.ping.count = 6
    settings2.ping.delay = 300
    settings2.trace.timeout = 22750
    settings2.trace.count = 4
    settings2.trace.limit = 40
    settings2.trace.delay = 30
    settings2.trace.protocol = Protocol.ICMP
    # settings2.ip.targets = [IP("55.161.222.85"), IP("35.205.242.146")]  # can't update after created test's been created

    try:
        # create
        test = IPTest("e2e-ip-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, IPTest)
        assert created_test.name == "e2e-ip-test"
        assert created_test.type == TestType.IP
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, IPTest)
        assert received_test.name == "e2e-ip-test"
        assert received_test.type == TestType.IP
        assert received_test.status == TestStatus.ACTIVE
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-ip-test-updated"
        created_test.settings = settings2
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, IPTest)
        assert updated_test.name == "e2e-ip-test-updated"
        assert updated_test.type == TestType.IP
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
