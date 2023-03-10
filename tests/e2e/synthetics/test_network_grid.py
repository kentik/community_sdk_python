from copy import deepcopy

import pytest

from kentik_api.public.types import IP
from kentik_api.synthetics.synth_tests import NetworkGridTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.network_grid import GridTestSettings, NetworkGridTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType

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
def test_network_grid_crud(test_labels, notification_channels) -> None:
    agents = pick_agent_ids(count=2)
    initial_settings = GridTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=INITIAL_HEALTH_SETTINGS,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        network_grid=NetworkGridTestSpecific(targets=[IP("54.161.222.85"), IP("34.205.242.146")]),
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
    update_settings.network_grid.targets = [IP("77.126.243.32"), IP("44.211.231.198")]
    update_settings.notification_channels = []

    test = NetworkGridTest(make_e2e_test_name(TestType.NETWORK_GRID), TestStatus.ACTIVE, initial_settings)
    test.labels = test_labels

    execute_test_crud_steps(test, update_settings=update_settings)
