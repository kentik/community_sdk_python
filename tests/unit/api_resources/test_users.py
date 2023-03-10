from datetime import datetime, timezone
from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.users_api import UsersAPI
from kentik_api.public.types import ID
from kentik_api.public.user import User
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_user_success() -> None:
    # given
    create_response_payload = """
    {
        "user": {
                    "id":"145985",
                    "username":"test@user.example",
                    "user_full_name":"Test User",
                    "user_email":"test@user.example",
                    "role":"Member",
                    "email_service":"true",
                    "email_product":"true",
                    "last_login":null,
                    "created_date":"2020-12-09T14:33:28.330Z",
                    "updated_date":"2020-12-09T14:33:28.369Z",
                    "company_id":"74333",
                    "filters":{},
                    "saved_filters":[]
                }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    users_api = UsersAPI(connector)

    # when
    email = "test@user.example"
    user = User.new(
        username=email,
        full_name="Test User",
        user_email=email,
        role="Member",
        email_service=True,
        email_product=True,
    )
    created = users_api.create(user)

    # then request properly formed
    assert connector.last_url_path == "/user"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert "user" in connector.last_payload
    assert connector.last_payload["user"]["user_full_name"] == "Test User"
    assert connector.last_payload["user"]["user_email"] == "test@user.example"
    assert connector.last_payload["user"]["role"] == "Member"
    assert connector.last_payload["user"]["email_service"] is True
    assert connector.last_payload["user"]["email_product"] is True

    # and response properly parsed
    assert created.id == ID(145985)
    assert created.username == "test@user.example"
    assert created.full_name == "Test User"
    assert created.email == "test@user.example"
    assert created.company_id == ID(74333)
    assert created.role == "Member"
    assert created.email_service is True
    assert created.email_product is True
    assert created.created_date == datetime(2020, 12, 9, 14, 33, 28, 330000, tzinfo=timezone.utc)
    assert created.updated_date == datetime(2020, 12, 9, 14, 33, 28, 369000, tzinfo=timezone.utc)


def test_get_user_success() -> None:
    # given
    get_response_payload = """
        {
            "user": {
                        "id":"145999",
                        "username":"test@user.example",
                        "user_full_name":"Test User",
                        "user_email":"test@user.example",
                        "role":"Member",
                        "email_service":true,
                        "email_product":true,
                        "last_login":null,
                        "created_date":"2020-12-09T14:48:42.187Z",
                        "updated_date":"2020-12-09T14:48:43.243Z",
                        "company_id":"74333",
                        "filters":{},
                        "saved_filters":[]
                    }
        }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    users_api = UsersAPI(connector)

    # when
    user_id = ID(145999)
    user = users_api.get(user_id)

    # then request properly formed
    assert connector.last_url_path == f"/user/{user_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert int(user.id) == 145999
    assert user.username == "test@user.example"
    assert user.full_name == "Test User"
    assert user.email == "test@user.example"
    assert user.company_id == ID(74333)
    assert user.role == "Member"
    assert user.email_service is True
    assert user.email_product is True
    assert user.created_date == datetime(2020, 12, 9, 14, 48, 42, 187000, tzinfo=timezone.utc)
    assert user.updated_date == datetime(2020, 12, 9, 14, 48, 43, 243000, tzinfo=timezone.utc)


def test_update_user_success() -> None:
    # given
    update_response_payload = """
    {
        "user":{
                "id":"146034",
                "username":"test@user.example",
                "user_full_name":"User Testing",
                "user_email":"test@user.example",
                "role":"Member",
                "email_service":true,
                "email_product":true,
                "last_login":null,
                "created_date":"2020-12-09T15:23:29.768Z",
                "updated_date":"2020-12-09T15:23:31.108Z",
                "company_id":"74333",
                "filters":{},
                "saved_filters":[]
               }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    users_api = UsersAPI(connector)
    user_id = ID(146034)
    user = User(
        _id=user_id,
        username="testname",
        email="test@ema.il",
        email_service=True,
        email_product=True,
        full_name="User Test",
    )

    # when
    user.full_name = "User Testing"
    updated = users_api.update(user)

    # then request properly formed
    assert connector.last_url_path == f"/user/{user_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert "user" in connector.last_payload
    assert connector.last_payload["user"]["user_full_name"] == "User Testing"

    # then response properly parsed
    assert updated.id == ID(146034)
    assert updated.full_name == "User Testing"
    assert updated.email == "test@user.example"
    assert updated.created_date == datetime(2020, 12, 9, 15, 23, 29, 768000, tzinfo=timezone.utc)
    assert updated.updated_date == datetime(2020, 12, 9, 15, 23, 31, 108000, tzinfo=timezone.utc)


def test_delete_user_success() -> None:
    # given
    delete_response_payload = ""  # deleting user responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    users_api = UsersAPI(connector)

    # when
    user_id = ID(146034)
    delete_successful = users_api.delete(user_id)

    # then request properly formed
    assert connector.last_url_path == f"/user/{user_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful
