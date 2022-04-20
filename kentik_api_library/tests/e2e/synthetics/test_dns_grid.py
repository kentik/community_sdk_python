import pytest

from kentik_api.synthetics.synth_tests import DNSGridTest
from kentik_api.synthetics.synth_tests.dns_grid import DNSGridTestSettings, DSNGridTestSpecific
from kentik_api.synthetics.types import DNSRecordType, IPFamily, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_dns_grid_crud() -> None:
    settings = DNSGridTestSettings(
        family=IPFamily.DUAL,
        period=60,
        agent_ids=["841"],
        health_settings=HEALTH,
        dns_grid=DSNGridTestSpecific(
            target="123",
            timeout=100,
            record_type=DNSRecordType.AAAA,
            servers=["4.4.4.4", "8.8.8.8"],
            port=53,
        ),
    )

    # create
    test = DNSGridTest("e2e-dnsgrid-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.DNS_GRID

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-dnsgrid-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-dnsgrid-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
