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
            target="123",
            timeout=100,
            record_type=DNSRecordType.AAAA,
            servers=["4.4.4.4", "8.8.8.8"],
            port=53,
        ),
    )
    settings2 = DNSGridTestSettings(
        family=IPFamily.V4,  # family update doesn't take effect
        period=120,
        agent_ids=[agents[1]],
        health_settings=HEALTH2,
        dns_grid=DSNGridTestSpecific(
            target="123",  # target can't be updated after a test has been created
            timeout=100,  # timeout update doesn't take effect
            record_type=DNSRecordType.A,
            servers=["5.5.5.5", "9.9.9.9"],
            port=63,
        ),
    )

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
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, DNSGridTest)
        assert updated_test.name == "e2e-dnsgrid-test-updated"
        assert received_test.type == TestType.DNS_GRID
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
