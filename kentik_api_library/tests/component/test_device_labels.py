from http import HTTPStatus

from kentik_api import kentik_api
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.device_label import DeviceLabel
from tests.component.stub_api_connector import StubAPIConnector


def test_create_device_label_success():
    # given
    create_response_payload = """
    {
        "id": 42,
        "name": "apitest-device_label-1",
        "color": "#00FF00",
        "user_id": "user1",
        "company_id": "company1",
        "order": 0,
        "devices": [],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-05-16T20:21:10.406Z"
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED.value)
    client = kentik_api.KentikAPI(connector)

    # when
    device_label = DeviceLabel("apitest-device_label-1", "#00FF00")
    created = client.device_labels.create(device_label)

    # then request properly formed
    assert connector.last_url == "/deviceLabels"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-device_label-1"
    assert connector.last_payload["color"] == "#00FF00"

    # and response properly parsed
    assert created.id == 42
    assert created.name == "apitest-device_label-1"
    assert created.color == "#00FF00"
    assert created.user_id == "user1"
    assert created.company_id == "company1"
    assert created.created_date == "2018-05-16T20:21:10.406Z"
    assert created.updated_date == "2018-05-16T20:21:10.406Z"
    assert len(created.devices) == 0


def test_get_device_label_success():
    # given
    get_response_payload = """
    {
        "id": 32,
        "name": "ISP",
        "color": "#f1d5b9",
        "user_id": "user1",
        "company_id": "company1",
        "order": 0,
        "devices": [
            {
                "id": "device1",
                "device_name": "my_device_1",
                "device_subtype": "router"
            }
        ],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-05-16T20:21:10.406Z"
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK.value)
    client = kentik_api.KentikAPI(connector)

    # when
    device_label_id = 32
    device_label = client.device_labels.get(device_label_id)

    # then request properly formed
    assert connector.last_url == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert device_label.id == 32
    assert device_label.name == "ISP"
    assert device_label.color == "#f1d5b9"
    assert device_label.user_id == "user1"
    assert device_label.company_id == "company1"
    assert device_label.created_date == "2018-05-16T20:21:10.406Z"
    assert device_label.updated_date == "2018-05-16T20:21:10.406Z"
    assert len(device_label.devices) == 1
    assert device_label.devices[0].id == "device1"
    assert device_label.devices[0].device_name == "my_device_1"
    assert device_label.devices[0].device_subtype == "router"


def test_update_device_label_success():
    # given
    update_response_payload = """
    {
        "id": 42,
        "name": "apitest-device_label-one",
        "color": "#00FF00",
        "user_id": "user1",
        "company_id": "company1",
        "devices": [],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-05-16T20:21:10.406Z"
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK.value)
    client = kentik_api.KentikAPI(connector)

    # when
    device_label_id = 42
    device_label = DeviceLabel(id=device_label_id, name="apitest-device_label-one")
    updated = client.device_labels.update(device_label)

    # then request properly formed
    assert connector.last_url == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-device_label-one"
    assert "color" not in connector.last_payload

    # then response properly parsed
    assert updated.id == 42
    assert updated.name == "apitest-device_label-one"
    assert updated.color == "#00FF00"
    assert updated.user_id == "user1"
    assert updated.company_id == "company1"
    assert updated.created_date == "2018-05-16T20:21:10.406Z"
    assert updated.updated_date == "2018-05-16T20:21:10.406Z"
    assert len(updated.devices) == 0


def test_delete_device_label_success():
    # given
    delete_response_payload = """
    {
        "success": true
    }"""
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.OK.value)
    client = kentik_api.KentikAPI(connector)

    # when
    device_label_id = 42
    delete_successful = client.device_labels.delete(device_label_id)

    # then request properly formed
    assert connector.last_url == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful
