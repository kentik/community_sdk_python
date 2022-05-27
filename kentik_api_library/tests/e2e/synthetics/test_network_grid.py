import pytest

from kentik_api.public.types import IP
from kentik_api.synthetics.synth_tests import NetworkGridTest
from kentik_api.synthetics.synth_tests.base import PingTask, TraceTask
from kentik_api.synthetics.synth_tests.network_grid import GridTestSettings, NetworkGridTestSpecific
from kentik_api.synthetics.types import IPFamily, Protocol, TestStatus, TestType

from .utils import HEALTH, client, credentials_missing_str, credentials_present, pick_agent_ids


@pytest.mark.skipif(not credentials_present, reason=credentials_missing_str)
def test_network_grid_crud() -> None:
    settings = GridTestSettings(
        family=IPFamily.V4,
        period=60,
        agent_ids=pick_agent_ids(),
        health_settings=HEALTH,
        ping=PingTask(timeout=3000, count=5, delay=200, protocol=Protocol.ICMP, port=2222),
        trace=TraceTask(timeout=22500, count=3, limit=30, delay=20, protocol=Protocol.UDP, port=3343),
        network_grid=NetworkGridTestSpecific(targets=[IP("54.161.222.85"), IP("34.205.242.146")]),
    )

    # create
    test = NetworkGridTest("e2e-networkgrid-test", TestStatus.ACTIVE, settings)
    created_test = client().synthetics.create_test(test)
    assert created_test.type == TestType.NETWORK_GRID

    # set status and read
    client().synthetics.set_test_status(created_test.id, TestStatus.PAUSED)
    received_test = client().synthetics.get_test(created_test.id)
    assert received_test.status == TestStatus.PAUSED

    # update
    created_test.name = "e2e-networkgrid-test-updated"
    updated_test = client().synthetics.update_test(created_test)
    assert updated_test.name == "e2e-networkgrid-test-updated"

    # delete
    client().synthetics.delete_test(created_test.id)
