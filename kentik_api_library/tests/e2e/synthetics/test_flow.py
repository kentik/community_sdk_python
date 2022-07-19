from copy import deepcopy

import pytest

from kentik_api.synthetics.synth_tests import FlowTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.flow import FlowTestSettings, FlowTestSpecific
from kentik_api.synthetics.types import DirectionType, FlowTestSubType, IPFamily, Protocol, TestStatus, TestType

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
def test_flow_crud(test_labels, notification_channels) -> None:
    agents = pick_agent_ids(count=2)
    initial_settings = FlowTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=INITIAL_HEALTH_SETTINGS,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        flow=FlowTestSpecific(
            target="San Francisco",
            target_refresh_interval_millis=150,
            max_providers=5,
            max_ip_targets=4,
            type=FlowTestSubType.CITY,
            inet_direction=DirectionType.DST,
            direction=DirectionType.DST,
        ),
        notification_channels=notification_channels,
    )
    update_settings = deepcopy(initial_settings)
    update_settings.family = IPFamily.V6
    # update_settings.period = 120  # period update doesn't take effect
    update_settings.agent_ids = [agents[1]]
    update_settings.health_settings = UPDATE_HEALTH_SETTINGS
    update_settings.ping.timeout = 4000
    update_settings.ping.count = 6
    update_settings.ping.delay = 300
    update_settings.trace.timeout = 22750
    update_settings.trace.count = 4
    update_settings.trace.limit = 40
    update_settings.trace.delay = 30
    update_settings.trace.protocol = Protocol.ICMP
    # update_settings.flow.target="www.wikipedia.org"  # target can't be updated after a test has been created
    update_settings.flow.target_refresh_interval_millis = 250
    update_settings.flow.max_providers = 6
    update_settings.flow.max_ip_targets = 5
    # update_settings.flow.type = FlowTestSubType.REGION  # type update doesn't take effect
    update_settings.flow.inet_direction = DirectionType.SRC
    update_settings.flow.direction = DirectionType.SRC
    update_settings.notification_channels = []

    test = FlowTest(make_e2e_test_name(TestType.FLOW), TestStatus.ACTIVE, initial_settings)
    test.labels = test_labels

    execute_test_crud_steps(test, update_settings=update_settings)
