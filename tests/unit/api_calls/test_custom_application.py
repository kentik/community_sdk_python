from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.custom_applications import *

DUMMY_API_URL = "/customApplications"
DUMMY_APP_ID = "dummy_app_id"


def test_get_custom_applications__return_apiCall():

    # WHEN
    call = get_custom_applications()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "GET"


def test_create_custom_applications__return_apiCall():

    # WHEN
    call = create_custom_application()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_custom_applications__return_apiCall():

    # WHEN
    call = update_custom_application(DUMMY_APP_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_APP_ID}"
    assert call.method.name == "PUT"


def test_delete_custom_applications__return_apiCall():

    # WHEN
    call = delete_custom_application(DUMMY_APP_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_APP_ID}"
    assert call.method.name == "DELETE"
