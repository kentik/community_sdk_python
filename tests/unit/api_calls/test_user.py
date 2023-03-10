from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.users import *

DUMMY_API_URL = "/user"
DUMMY_USR_ID = "dummy_dim_id"


def test_get_users__return_apiCall():

    # WHEN
    call = get_users()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_user_info__return_apiCall():

    # WHEN
    call = get_user_info(DUMMY_USR_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_USR_ID}"
    assert call.method.name == "GET"


def test_create_user__return_apiCall():

    # WHEN
    call = create_user()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_user__return_apiCall():

    # WHEN
    call = update_user(DUMMY_USR_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_USR_ID}"
    assert call.method.name == "PUT"


def test_delete_user__return_apiCall():

    # WHEN
    call = delete_user(DUMMY_USR_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_USR_ID}"
    assert call.method.name == "DELETE"
