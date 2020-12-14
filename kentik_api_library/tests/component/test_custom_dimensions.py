from http import HTTPStatus

from kentik_api.api_resources.custom_dimensions_api import CustomDimensionsAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.custom_dimension import CustomDimension
from tests.component.stub_api_connector import StubAPIConnector


def test_create_custom_dimension_success() -> None:
    # given
    create_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": []
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension = CustomDimension(
        name="c_testapi_dimension_1",
        display_name="dimension_display_name",
        type="string",
    )
    created = custom_dimensions_api.create(dimension)

    # then request properly formed
    assert connector.last_url == "/customdimension"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["name"] == "c_testapi_dimension_1"
    assert connector.last_payload["display_name"] == "dimension_display_name"
    assert connector.last_payload["type"] == "string"

    # and response properly parsed
    assert created.id == 42
    assert created.name == "c_testapi_dimension_1"
    assert created.display_name == "dimension_display_name"
    assert created.type == "string"
    assert created.company_id == "74333"
    assert created.populators is not None
    assert len(created.populators) == 0


def test_get_custom_dimension_success() -> None:
    # given
    get_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name",
            "type": "string",
            "company_id": "74333",
            "populators": []
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = 42
    dimension = custom_dimensions_api.get(dimension_id)

    # then request properly formed
    assert connector.last_url == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert dimension.id == 42
    assert dimension.name == "c_testapi_dimension_1"
    assert dimension.display_name == "dimension_display_name"
    assert dimension.type == "string"
    assert dimension.company_id == "74333"
    assert dimension.populators is not None
    assert len(dimension.populators) == 0


def test_update_custom_dimension_success() -> None:
    # given
    update_response_payload = """
    {
        "customDimension": {
            "id": 42,
            "name": "c_testapi_dimension_1",
            "display_name": "dimension_display_name2",
            "type": "string",
            "company_id": "74333",
            "populators": []
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = 42
    dimension = CustomDimension(id=dimension_id, display_name="dimension_display_name2")
    updated = custom_dimensions_api.update(dimension)

    # then request properly formed
    assert connector.last_url == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert connector.last_payload["display_name"] == "dimension_display_name2"

    # and response properly parsed
    assert updated.id == 42
    assert updated.name == "c_testapi_dimension_1"
    assert updated.display_name == "dimension_display_name2"
    assert updated.type == "string"
    assert updated.company_id == "74333"
    assert updated.populators is not None
    assert len(updated.populators) == 0


def test_delete_custom_dimension_success() -> None:
    # given
    delete_response_payload = ""  # deleting custom dimension responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimension_id = 42
    delete_successful = custom_dimensions_api.delete(dimension_id)

    # then request properly formed
    assert connector.last_url == f"/customdimension/{dimension_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful


def test_get_all_custom_dimensions_success() -> None:
    # given
    get_response_payload = """
    {
        "customDimensions": [
            {
                "id": 42,
                "name": "c_testapi_dimension_1",
                "display_name": "dimension_display_name1",
                "type": "string",
                "populators": [],
                "company_id": "74333"
            },
            {
                "id": 43,
                "name": "c_testapi_dimension_2",
                "display_name": "dimension_display_name2",
                "type": "uint32",
                "company_id": "74334",
                "populators": []
            }
        ]
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    custom_dimensions_api = CustomDimensionsAPI(connector)

    # when
    dimensions = custom_dimensions_api.get_all()

    # then request properly formed
    assert connector.last_url == "/customdimensions"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # and response properly parsed
    assert len(dimensions) == 2
    assert dimensions[1].id == 43
    assert dimensions[1].name == "c_testapi_dimension_2"
    assert dimensions[1].display_name == "dimension_display_name2"
    assert dimensions[1].type == "uint32"
    assert dimensions[1].company_id == "74334"
    assert dimensions[1].populators is not None
    assert len(dimensions[1].populators) == 0
