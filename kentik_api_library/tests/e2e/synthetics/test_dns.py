import pytest

from kentik_api.synthetics.synth_tests import DNSTest
from kentik_api.synthetics.synth_tests.dns import DNSTestSettings, DNSTestSpecific
from kentik_api.synthetics.types import DNSRecordType, IPFamily, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_dns_crud() -> None:
    settings = DNSTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=pick_agent_ids(),
        health_settings=HEALTH,
        dns=DNSTestSpecific(
            target="123",
            timeout=100,
            record_type=DNSRecordType.AAAA,
            servers=["4.4.4.4", "8.8.8.8"],
            port=53,
        ),
    )

    # create
    test = DNSTest("e2e-dns-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.DNS

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-dns-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-dns-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
