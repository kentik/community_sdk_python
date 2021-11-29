from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.custom_applications_api import CustomApplicationsAPI
from kentik_api.public.custom_application import CustomApplication
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_custom_application_success() -> None:
    # given
    create_response_payload = """
    {
        "name": "apitest-customapp-1",
        "description": "Testing custom application api",
        "ip_range": "192.168.0.1,192.168.0.2",
        "protocol": "6,17",
        "port": "9001,9002,9003",
        "asn": "asn1,asn2,asn3",
        "id": 207,
        "user_id": "144319",
        "company_id": "74333"
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    custom_applications_api = CustomApplicationsAPI(connector)

    # when
    app = CustomApplication(
        name="apitest-customapp-1",
        description="Testing custom application api",
        ip_range="192.168.0.1,192.168.0.2",
        protocol="6,17",
        port="9001,9002,9003",
        asn="asn1,asn2,asn3",
    )
    created = custom_applications_api.create(app)

    # then request properly formed
    assert connector.last_url_path == "/customApplications"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-customapp-1"
    assert connector.last_payload["description"] == "Testing custom application api"
    assert connector.last_payload["ip_range"] == "192.168.0.1,192.168.0.2"
    assert connector.last_payload["protocol"] == "6,17"
    assert connector.last_payload["port"] == "9001,9002,9003"
    assert connector.last_payload["asn"] == "asn1,asn2,asn3"

    # and response properly parsed
    assert created.name == "apitest-customapp-1"
    assert created.description == "Testing custom application api"
    assert created.ip_range == "192.168.0.1,192.168.0.2"
    assert created.protocol == "6,17"
    assert created.port == "9001,9002,9003"
    assert created.asn == "asn1,asn2,asn3"
    assert created.id == ID(207)
    assert created.user_id == ID(144319)
    assert created.company_id == ID(74333)


def test_update_custom_application_success() -> None:
    # given
    update_response_payload = """
    {
        "id": 207,
        "company_id": "74333",
        "user_id": "144319",
        "name": "apitest-customapp-one",
        "description": "TESTING CUSTOM APPS",
        "ip_range": "192.168.5.1,192.168.5.2",
        "protocol": "6,17",
        "port": "9011,9012,9013",
        "asn": "asn1,asn2,asn3",
        "cdate": "2020-12-11T07:07:20.968Z",
        "edate": "2020-12-11T07:07:20.968Z"
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    custom_applications_api = CustomApplicationsAPI(connector)

    # when
    app_id = ID(207)
    app = CustomApplication(
        id=app_id,
        name="apitest-customapp-one",
        description="TESTING CUSTOM APPS",
        ip_range="192.168.5.1,192.168.5.2",
        port="9011,9012,9013",
    )
    updated = custom_applications_api.update(app)

    # then request properly formed
    assert connector.last_url_path == f"/customApplications/{app_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "apitest-customapp-one"
    assert connector.last_payload["description"] == "TESTING CUSTOM APPS"
    assert connector.last_payload["ip_range"] == "192.168.5.1,192.168.5.2"
    assert connector.last_payload["port"] == "9011,9012,9013"
    assert "protocol" not in connector.last_payload
    assert "asn" not in connector.last_payload

    # and response properly parsed
    assert updated.name == "apitest-customapp-one"
    assert updated.description == "TESTING CUSTOM APPS"
    assert updated.ip_range == "192.168.5.1,192.168.5.2"
    assert updated.protocol == "6,17"
    assert updated.port == "9011,9012,9013"
    assert updated.asn == "asn1,asn2,asn3"
    assert updated.id == ID(207)
    assert updated.user_id == ID(144319)
    assert updated.company_id == ID(74333)
    assert updated.created_date == "2020-12-11T07:07:20.968Z"
    assert updated.updated_date == "2020-12-11T07:07:20.968Z"


def test_delete_custom_application_success() -> None:
    # given
    delete_response_payload = ""  # deleting custom application responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    custom_applications_api = CustomApplicationsAPI(connector)

    # when
    app_id = ID(42)
    delete_successful = custom_applications_api.delete(app_id)

    # then request properly formed
    assert connector.last_url_path == f"/customApplications/{app_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_all_custom_applications_success() -> None:
    # given
    get_response_payload = """
    [
        {
            "id": 42,
            "company_id": "74333",
            "user_id": null,
            "name": "apitest-customapp-1",
            "description": "TESTING CUSTOM APPS 1",
            "ip_range": "192.168.0.1,192.168.0.2",
            "protocol": "6,17",
            "port": "9001,9002,9003",
            "asn": "asn1,asn2,asn3",
            "cdate": "2020-12-11T07:07:20.968Z",
            "edate": "2020-12-11T07:07:20.968Z"
        },
        {
            "id": 43,
            "company_id": "74333",
            "user_id": "144319",
            "name": "apitest-customapp-2",
            "description": "TESTING CUSTOM APPS 2",
            "ip_range": "192.168.0.3,192.168.0.4",
            "protocol": "6,17",
            "port": "9011,9012,9013",
            "asn": "asn4,asn5,asn6",
            "cdate": "2020-12-11T07:08:20.968Z",
            "edate": "2020-12-11T07:08:20.968Z"
        }
    ]"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_applications_api = CustomApplicationsAPI(connector)

    # when
    apps = custom_applications_api.get_all()

    # then request properly formed
    assert connector.last_url_path == "/customApplications"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(apps) == 2
    assert apps[0].user_id is None
    assert apps[1].id == ID(43)
    assert apps[1].company_id == ID(74333)
    assert apps[1].user_id == ID(144319)
    assert apps[1].name == "apitest-customapp-2"
    assert apps[1].description == "TESTING CUSTOM APPS 2"
    assert apps[1].ip_range == "192.168.0.3,192.168.0.4"
    assert apps[1].protocol == "6,17"
    assert apps[1].port == "9011,9012,9013"
    assert apps[1].asn == "asn4,asn5,asn6"
    assert apps[1].created_date == "2020-12-11T07:08:20.968Z"
    assert apps[1].updated_date == "2020-12-11T07:08:20.968Z"
