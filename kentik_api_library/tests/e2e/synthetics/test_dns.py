import pytest

from kentik_api.synthetics.synth_tests import DNSTest
from kentik_api.synthetics.synth_tests.dns import DNSTestSettings, DNSTestSpecific
from kentik_api.synthetics.types import DNSRecordType, IPFamily, TestStatus, TestType

from .utils import HEALTH1, HEALTH2, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_dns_crud() -> None:
    agents = pick_agent_ids(count=2)
    settings1 = DNSTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=[agents[0]],
        health_settings=HEALTH1,
        dns=DNSTestSpecific(
            target="123",
            timeout=100,
            record_type=DNSRecordType.AAAA,
            servers=["4.4.4.4", "8.8.8.8"],
            port=53,
        ),
    )
    settings2 = DNSTestSettings(
        family=IPFamily.V4,  # family update doesn't take effect
        period=120,
        agent_ids=[agents[1]],
        health_settings=HEALTH2,
        dns=DNSTestSpecific(
            target="123",  # target can't be updated after a test has been created
            timeout=100,  # timeout update doesn't take effect
            record_type=DNSRecordType.A,
            servers=["5.5.5.5", "9.9.9.9"],
            port=63,
        ),
    )
    try:
        # create
        test = DNSTest("e2e-dns-test", TestStatus.ACTIVE, settings1)
        created_test = client().synthetics.create_test(test)
        assert isinstance(created_test, DNSTest)
        assert created_test.name == "e2e-dns-test"
        assert created_test.type == TestType.DNS
        assert created_test.status == TestStatus.ACTIVE
        assert created_test.settings == settings1

        # read
        received_test = client().synthetics.get_test(created_test.id)
        assert isinstance(received_test, DNSTest)
        assert received_test.name == "e2e-dns-test"
        assert received_test.type == TestType.DNS
        assert received_test.status == TestStatus.ACTIVE
        assert received_test.settings == settings1

        # update
        created_test.name = "e2e-dns-test-updated"
        created_test.settings = settings2
        updated_test = client().synthetics.update_test(created_test)
        assert isinstance(updated_test, DNSTest)
        assert updated_test.name == "e2e-dns-test-updated"
        assert updated_test.type == TestType.DNS
        assert updated_test.status == TestStatus.ACTIVE
        assert updated_test.settings == settings2
    finally:
        # delete (even if assertion failed)
        client().synthetics.delete_test(created_test.id)
