from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.batch_api import BatchAPI
from kentik_api.public.batch_operation import BatchOperationPart, Criterion, Deletion, Upsert
from tests.unit.stub_api_connector import StubAPIConnector


def test_batch_operation_on_flow_tags_success() -> None:
    # given
    response_payload = """{
            "message": "Successfully stored request. Batch queued for processing.",
            "guid": "guid1234"
        }"""
    criterion1 = Criterion(["192.168.0.2", "192.168.0.3"])
    criterion2 = Criterion(["192.168.0.4", "192.168.0.5"], Criterion.Direction.SRC)
    upsert1 = Upsert("value1", [criterion1, criterion2])
    upsert2 = Upsert("value2", [criterion1])
    deletion1 = Deletion("del_value1")
    deletion2 = Deletion("del_value2")
    batch_operation = BatchOperationPart(
        replace_all=False,
        complete=True,
        upserts=[upsert1, upsert2],
        deletes=[deletion1, deletion2],
    )
    connector = StubAPIConnector(response_payload, HTTPStatus.OK)
    batch_api = BatchAPI(connector)

    # when
    response = batch_api.batch_operation_on_flow_tags(batch_operation)

    # then
    assert connector.last_url_path == "/batch/tags"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["replace_all"] is False
    assert connector.last_payload["complete"] is True
    assert connector.last_payload["upserts"][0]["value"] == "value1"
    assert connector.last_payload["upserts"][1]["value"] == "value2"
    assert len(connector.last_payload["upserts"][0]["criteria"]) == 2
    assert len(connector.last_payload["upserts"][1]["criteria"]) == 1
    assert connector.last_payload["upserts"][0]["criteria"][0]["direction"] == "either"
    assert connector.last_payload["upserts"][0]["criteria"][1]["direction"] == "src"
    assert len(connector.last_payload["deletes"]) == 2
    assert connector.last_payload["deletes"][0]["value"] == "del_value1"

    assert response.message == "Successfully stored request. Batch queued for processing."
    assert response.guid == "guid1234"


def test_batch_operation_on_populators_success() -> None:
    # given
    response_payload = """{
            "message": "Successfully stored request. Batch queued for processing.",
            "guid": "guid2137"
        }"""
    criterion = Criterion(["192.168.0.2", "192.168.0.3"])
    upsert = Upsert("value", [criterion])
    deletion = Deletion("del_value")
    batch_operation = BatchOperationPart(
        replace_all=False,
        complete=True,
        upserts=[upsert],
        deletes=[deletion],
        guid="guid2137",
    )
    connector = StubAPIConnector(response_payload, HTTPStatus.OK)
    batch_api = BatchAPI(connector)

    # when
    response = batch_api.batch_operation_on_populators("dimension_name", batch_operation)

    # then
    assert connector.last_url_path == "/batch/customdimensions/dimension_name/populators"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["replace_all"] is False
    assert connector.last_payload["complete"] is True
    assert connector.last_payload["guid"] == "guid2137"
    assert connector.last_payload["upserts"][0]["value"] == "value"
    assert connector.last_payload["deletes"][0]["value"] == "del_value"

    assert response.message == "Successfully stored request. Batch queued for processing."
    assert response.guid == "guid2137"


def test_get_status_success() -> None:
    # given
    response_payload = """
        {
            "custom_dimension": {
                "id": 98,
                "name": "MY_FAVE_DIM"
            },
            "guid": "guid12345",
            "is_multipart": false,
            "is_pending": false,
            "is_complete": true,
            "number_of_parts": 1,
            "user": {
              "id": 2233,
              "email": "username@domain.com"
            },
            "upserts": {
                "total": 9955,
                "applied": 9898,
                "invalid": 0,
                "unchanged": 0,
                "over_limit": 57
             },
             "deletes": {
               "total": 0,
               "applied": 0,
               "unchanged": 0,
               "invalid": 0
              },
              "replace_all": {
                "requested": true,
                "deletes_performed": 0,
                "successful": true
              },
              "batch_date": "2018-09-25T21:41:18.88816Z"
        }"""
    batch_guid = "guid12345"
    connector = StubAPIConnector(response_payload, HTTPStatus.OK)
    batch_api = BatchAPI(connector)

    # when
    status = batch_api.get_status(batch_guid)

    # then
    assert connector.last_url_path == "/batch/guid12345/status"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert status.custom_dimension is not None
    assert status.custom_dimension.id == 98
    assert status.custom_dimension.name == "MY_FAVE_DIM"
    assert status.guid == "guid12345"
    assert status.is_multipart is False
    assert status.is_complete is True
    assert status.number_of_parts == 1
    assert status.user.id == 2233
    assert status.user.email == "username@domain.com"
    assert status.upserts.total == 9955
    assert status.upserts.applied == 9898
    assert status.upserts.over_limit == 57
    assert status.upserts.invalid == 0
    assert status.upserts.unchanged == 0
    assert status.deletes.total == 0
    assert status.deletes.unchanged == 0
    assert status.deletes.invalid == 0
    assert status.deletes.applied == 0
    assert status.replace_all.requested is True
    assert status.replace_all.successful is True
    assert status.replace_all.deletes_performed == 0
    assert status.batch_date == "2018-09-25T21:41:18.88816Z"
