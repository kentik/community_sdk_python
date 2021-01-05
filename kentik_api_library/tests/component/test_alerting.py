from http import HTTPStatus

from kentik_api.api_resources.alerting_api import AlertingAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.manual_mitigation import ManualMitigation
from tests.component.stub_api_connector import StubAPIConnector


def test_create_manual_mitigation_success() -> None:
    # given
    create_response_payload = """
    {
        "response": {
            "result": "OK"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    alerting_api = AlertingAPI(connector)

    # when
    manual_mitigation = ManualMitigation("192.168.1.0/24", "comment", "1234", "12345", "20")
    created = alerting_api.create_manual_mitigation(manual_mitigation)

    # then
    assert connector.last_url == "/alerts/manual-mitigate"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["ipCidr"] == "192.168.1.0/24"
    assert connector.last_payload["comment"] == "comment"
    assert connector.last_payload["platformID"] == "1234"
    assert connector.last_payload["methodID"] == "12345"
    assert connector.last_payload["minutesBeforeAutoStop"] == "20"

    assert created is True
