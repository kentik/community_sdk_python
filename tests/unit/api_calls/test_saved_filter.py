from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.saved_filters import *

DUMMY_API_URL = "/saved-filter/custom"
DUMMY_FIL_ID = "dummy_dim_id"


def test_get_saved_filters__return_apiCall():

    # WHEN
    call = get_saved_filters()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == "/saved-filters/custom"
    assert call.method.name == "GET"


def test_get_saved_filter_info__return_apiCall():

    # WHEN
    call = get_saved_filter_info(DUMMY_FIL_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_FIL_ID}"
    assert call.method.name == "GET"


def test_create_saved_filter__return_apiCall():

    # WHEN
    call = create_saved_filter()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_saved_filter__return_apiCall():

    # WHEN
    call = update_saved_filter(DUMMY_FIL_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_FIL_ID}"
    assert call.method.name == "PUT"


def test_delete_saved_filter__return_apiCall():

    # WHEN
    call = delete_saved_filter(DUMMY_FIL_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_FIL_ID}"
    assert call.method.name == "DELETE"
