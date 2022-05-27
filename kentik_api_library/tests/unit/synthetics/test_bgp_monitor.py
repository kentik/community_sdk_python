from kentik_api.public.types import ID
from kentik_api.synthetics.synth_client import KentikSynthClient
from tests.unit.synthetics import syn_test_builder
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector


def test_get_bgp_monitor() -> None:
    # given
    pb_test, expected_test = syn_test_builder.make_bgp_test_pair()
    connector = StubAPISyntheticsConnector(tests_response=pb_test)
    client = KentikSynthClient(connector)

    # when
    test = client.get_test(ID("1234"))

    # then
    assert test == expected_test
