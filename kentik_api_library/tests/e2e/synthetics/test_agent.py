import pytest

from kentik_api.public.types import ID
from kentik_api.synthetics.synth_tests import AgentTest
from kentik_api.synthetics.synth_tests.agent import AgentTestSettings, AgentTestSpecific
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_agent_test_crud() -> None:
    agents = pick_agent_ids(count=4)
    settings1 = AgentTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        agent=AgentTestSpecific(target=agents[1], use_local_ip=False),
    )
    settings2 = AgentTestSettings(
        family=IPFamily.V6,
        period=60,  # period update doesn't take effect
        agent_ids=[agents[2]],
        health_settings=HEALTH2,
        ping=PingTask(timeout=4000, count=6, delay=300, protocol=Protocol.ICMP, port=3333),
        trace=TraceTask(timeout=22750, count=4, limit=40, delay=30, protocol=Protocol.ICMP, port=4343),
        agent=AgentTestSpecific(target=agents[3], use_local_ip=True),
    )

    try:
        # create
        test = AgentTest("e2e-agent-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, AgentTest)
        assert created_test.name == "e2e-agent-test"
        assert created_test.type == TestType.AGENT
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # set status and read
        client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, AgentTest)
        assert received_test.name == "e2e-agent-test"
        assert received_test.type == TestType.AGENT
        assert received_test.status == TestStatus.PAUSED
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-agent-test-updated"
        created_test.status = TestStatus.ACTIVE
        created_test.settings = settings2
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, AgentTest)
        assert updated_test.name == "e2e-agent-test-updated"
        assert received_test.type == TestType.AGENT
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
