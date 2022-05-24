from kentik_api.public.types import ID
from kentik_api.synthetics.synth_client import KentikSynthClient
from tests.unit.synthetics import clear_readonly_fields, protobuf_assert_equal, syn_test_builder
from tests.unit.synthetics.stub_api_connector import StubAPISyntheticsConnector


def test_get_dns() -> None:
    # given
    pb_test, expected_test = syn_test_builder.make_dns_test_pair()
    connector = StubAPISyntheticsConnector(tests_response=pb_test)
    client = KentikSynthClient(connector)

    # when
    test = client.get_test(ID("1234"))

    # then
    assert test == expected_test


def test_create_dns() -> None:
    # given
    pb_test, input_test = syn_test_builder.make_dns_test_pair()
    connector = StubAPISyntheticsConnector()
    client = KentikSynthClient(connector)

    # when
    client.create_test(input_test)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(pb_test), "Test")


def test_update_dns() -> None:
    # given
    pb_test, input_test = syn_test_builder.make_dns_test_pair()
    connector = StubAPISyntheticsConnector()
    client = KentikSynthClient(connector)

    # when
    client.update_test(input_test)

    # then
    protobuf_assert_equal(connector.last_payload, clear_readonly_fields(pb_test), "Test")
