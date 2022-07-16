from copy import deepcopy

import pytest

from kentik_api.synthetics.synth_tests import DNSGridTest
from kentik_api.synthetics.synth_tests.dns_grid import DNSGridTestSettings, DSNGridTestSpecific
from kentik_api.synthetics.types import DNSRecordType, IPFamily, TestStatus, TestType

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
def test_dns_grid_crud(test_labels, notification_channels) -> None:
    agents = pick_agent_ids(count=2)
    initial_settings = DNSGridTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=INITIAL_HEALTH_SETTINGS,
        dns_grid=DSNGridTestSpecific(
            target="www.example.com",
            record_type=DNSRecordType.AAAA,
            servers=["1.1.1.1", "8.8.8.8"],
            port=53,
        ),
        notification_channels=notification_channels,
    )
    update_settings = deepcopy(initial_settings)
    # update_settings.family = IPFamily.V6  # family update doesn't take effect
    update_settings.period = 120
    update_settings.agent_ids = [agents[1]]
    update_settings.health_settings = UPDATE_HEALTH_SETTINGS
    # update_settings.dns_grid.target="www.wikipedia.org"  # target can't be updated after a test has been created
    update_settings.dns_grid.record_type = DNSRecordType.A
    update_settings.dns_grid.servers = ["8.8.8.8", "9.9.9.9"]
    update_settings.dns_grid.port = 63
    update_settings.notification_channels = []

    test = DNSGridTest(make_e2e_test_name(TestType.DNS_GRID), TestStatus.ACTIVE, initial_settings)
    test.labels = test_labels

    execute_test_crud_steps(test, update_settings=update_settings)
