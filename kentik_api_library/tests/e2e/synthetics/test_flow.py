import pytest

from kentik_api.synthetics.synth_tests import FlowTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.flow import FlowTestSettings, FlowTestSpecific
from kentik_api.synthetics.types import DirectionType, FlowTestSubType, IPFamily, Protocol, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_flow_crud() -> None:
    settings = FlowTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=pick_agent_ids(),
        health_settings=HEALTH,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        flow=FlowTestSpecific(
            target="123",
            target_refresh_interval_millis=150,
            max_providers=5,
            max_ip_targets=4,
            type=FlowTestSubType.CITY,
            inet_direction=DirectionType.DST,
            direction=DirectionType.DST,
        ),
    )

    # create
    test = FlowTest("e2e-flow-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.FLOW

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-flow-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-flow-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
