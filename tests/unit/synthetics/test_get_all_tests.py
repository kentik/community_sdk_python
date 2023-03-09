from kentik_api.synthetics.synth_client import KentikSynthClient
from tests.unit.synthetics import syn_test_builder
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector


def test_get_all_tests() -> None:
    # given
    cases = [
        syn_test_builder.make_ip_test_pair(),
        syn_test_builder.make_agent_test_pair(),
        syn_test_builder.make_hostname_test_pair(),
        syn_test_builder.make_page_load_test_pair(),
        syn_test_builder.make_url_test_pair(),
        syn_test_builder.make_network_mesh_test_pair(),
        syn_test_builder.make_network_grid_test_pair(),
        syn_test_builder.make_dns_test_pair(),
        syn_test_builder.make_dns_grid_test_pair(),
        syn_test_builder.make_flow_test_pair(),
    ]
    pb_tests, expected_tests_response = zip(*cases)
    pb_tests = list(pb_tests)
    expected_tests_response = list(expected_tests_response)

    connector = StubAPISyntheticsConnector(tests_response=pb_tests)
    client = KentikSynthClient(connector)

    # when
    tests = client.get_all_tests()

    # then response properly parsed
    assert tests == expected_tests_response
