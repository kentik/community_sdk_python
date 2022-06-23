from copy import deepcopy

import pytest

from kentik_api.synthetics.synth_tests import DNSGridTest
from kentik_api.synthetics.synth_tests.dns_grid import DNSGridTestSettings, DSNGridTestSpecific
from kentik_api.synthetics.types import DNSRecordType, IPFamily, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_dns_grid_crud() -> None:
    agents = pick_agent_ids(count=2)
    settings1 = DNSGridTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
        dns_grid=DSNGridTestSpecific(
            target="www.example.com",
            record_type=DNSRecordType.AAAA,
            servers=["1.1.1.1", "8.8.8.8"],
            port=53,
        ),
    )
    settings2 = deepcopy(settings1)
    # settings2.family = IPFamily.V6  # family update doesn't take effect
    settings2.period = 120
    settings2.agent_ids = [agents[1]]
    settings2.health_settings = HEALTH2
    # settings2.dns_grid.target="www.wikipedia.org"  # target can't be updated after a test has been created
    settings2.dns_grid.record_type = DNSRecordType.A
    settings2.dns_grid.servers = ["8.8.8.8", "9.9.9.9"]
    settings2.dns_grid.port = 63

    try:
        # create
        test = DNSGridTest("e2e-dnsgrid-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, DNSGridTest)
        assert created_test.name == "e2e-dnsgrid-test"
        assert created_test.type == TestType.DNS_GRID
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, DNSGridTest)
        assert received_test.name == "e2e-dnsgrid-test"
        assert received_test.type == TestType.DNS_GRID
        assert received_test.status == TestStatus.ACTIVE
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-dnsgrid-test-updated"
        created_test.settings = settings2
        created_test.status = TestStatus.PAUSED  # to safely update DNS port to arbitrary value
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, DNSGridTest)
        assert updated_test.name == "e2e-dnsgrid-test-updated"
        assert updated_test.type == TestType.DNS_GRID
        assert updated_test.status == TestStatus.PAUSED
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
