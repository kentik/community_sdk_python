from datetime import datetime, timezone
from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.device_labels_api import DeviceLabelsAPI
from kentik_api.public.device_label import DeviceLabel
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_device_label_success() -> None:
    # given
    create_response_payload = """
    {
        "id": 42,
        "name": "apitest-device_label-1",
        "color": "#00FF00",
        "user_id": "52",
        "company_id": "72",
        "order": 0,
        "devices": [],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-05-16T20:21:10.406Z"
    }"""

    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    device_labels_api = DeviceLabelsAPI(connector)

    # when
    device_label = DeviceLabel.new(name="apitest-device_label-1", color="#00FF00")
    created = device_labels_api.create(device_label)

    # then request properly formed
    assert connector.last_url_path == "/deviceLabels"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-device_label-1"
    assert connector.last_payload["color"] == "#00FF00"

    # and response properly parsed
    assert created.id == ID(42)
    assert created.name == "apitest-device_label-1"
    assert created.color == "#00FF00"
    assert created.user_id == ID(52)
    assert created.company_id == ID(72)
    assert created.created_date == datetime(2018, 5, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert created.updated_date == datetime(2018, 5, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert len(created.devices) == 0


def test_get_device_label_success() -> None:
    # given
    get_response_payload = """
    {
        "id": 32,
        "name": "ISP",
        "color": "#f1d5b9",
        "user_id": null,
        "company_id": "72",
        "order": 0,
        "devices": [
            {
                "id": "42",
                "device_name": "my_device_1",
                "device_subtype": "router"
            }
        ],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-05-16T20:21:10.406Z"
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    device_labels_api = DeviceLabelsAPI(connector)

    # when
    device_label_id = ID(32)
    device_label = device_labels_api.get(device_label_id)

    # then request properly formed
    assert connector.last_url_path == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert device_label.id == ID(32)
    assert device_label.name == "ISP"
    assert device_label.color == "#f1d5b9"
    assert device_label.user_id is None
    assert device_label.company_id == ID(72)
    assert device_label.created_date == datetime(2018, 5, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert device_label.updated_date == datetime(2018, 5, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert len(device_label.devices) == 1
    assert device_label.devices[0].id == ID(42)
    assert device_label.devices[0].device_name == "my_device_1"
    assert device_label.devices[0].device_subtype == "router"


def test_update_device_label_success() -> None:
    # given
    update_response_payload = """
    {
        "id": 42,
        "name": "apitest-device_label-one",
        "color": "#AA00FF",
        "user_id": "52",
        "company_id": "72",
        "devices": [],
        "created_date": "2018-05-16T20:21:10.406Z",
        "updated_date": "2018-06-16T20:21:10.406Z"
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    device_labels_api = DeviceLabelsAPI(connector)
    device_label_id = ID(42)
    existing_label = DeviceLabel(
        name="apitest-device_label",
        color="#00FF00",
        _devices=[],
        _id=device_label_id,
        _user_id=ID(52),
        _company_id=ID(72),
        _created_date="2018-05-16T20:21:10.406Z",
        _updated_date="2018-05-16T20:21:10.406Z",
    )

    # when
    existing_label.name = "apitest-device_label-one"
    existing_label.color = "#AA00FF"
    updated = device_labels_api.update(existing_label)

    # then request properly formed
    assert connector.last_url_path == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-device_label-one"
    assert connector.last_payload["color"] == "#AA00FF"

    # then response properly parsed
    assert updated.id == ID(42)
    assert updated.name == "apitest-device_label-one"
    assert updated.color == "#AA00FF"
    assert updated.user_id == ID(52)
    assert updated.company_id == ID(72)
    assert updated.created_date == datetime(2018, 5, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert updated.updated_date == datetime(2018, 6, 16, 20, 21, 10, 406000, tzinfo=timezone.utc)
    assert len(updated.devices) == 0


def test_delete_device_label_success() -> None:
    # given
    delete_response_payload = """
    {
        "success": true
    }"""
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.OK)
    device_labels_api = DeviceLabelsAPI(connector)

    # when
    device_label_id = ID(42)
    delete_successful = device_labels_api.delete(device_label_id)

    # then request properly formed
    assert connector.last_url_path == f"/deviceLabels/{device_label_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_all_device_labels_success() -> None:
    # given
    get_response_payload = """
    [
        {
            "id": 41,
            "name": "device_labels_1",
            "color": "#5289D9",
            "user_id": null,
            "company_id": "74333",
            "devices": [],
            "created_date": "2020-11-20T12:54:49.575Z",
            "updated_date": "2020-11-20T12:54:49.575Z"
        },
        {
            "id": 42,
            "name": "device_labels_2",
            "color": "#3F4EA0",
            "user_id": "136885",
            "company_id": "74333",
            "devices": [
                {
                    "id": "1",
                    "device_name": "device1",
                    "device_type": "type1",
                    "device_subtype": "subtype1"
                },
                {
                    "id": "2",
                    "device_name": "device2",
                    "device_type": "type2",
                    "device_subtype": "subtype2"
                }
            ],
            "created_date": "2020-11-20T13:45:27.430Z",
            "updated_date": "2020-11-20T13:45:27.430Z"
        }
    ]"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    device_labels_api = DeviceLabelsAPI(connector)

    # when
    labels = device_labels_api.get_all()

    # then request properly formed
    assert connector.last_url_path == "/deviceLabels"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert len(labels) == 2
    assert labels[0].user_id is None  # API allows user_id to be None
    assert labels[1].id == ID(42)
    assert labels[1].name == "device_labels_2"
    assert labels[1].color == "#3F4EA0"
    assert labels[1].user_id == ID(136885)
    assert labels[1].company_id == ID(74333)
    assert labels[1].created_date == datetime(2020, 11, 20, 13, 45, 27, 430000, tzinfo=timezone.utc)
    assert labels[1].updated_date == datetime(2020, 11, 20, 13, 45, 27, 430000, tzinfo=timezone.utc)
    assert len(labels[1].devices) == 2
    assert labels[1].devices[1].id == ID(2)
    assert labels[1].devices[1].device_name == "device2"
    assert labels[1].devices[1].device_subtype == "subtype2"
    assert labels[1].devices[1].device_type == "type2"
