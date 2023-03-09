from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.sites import *

DUMMY_API_URL = "/site"
DUMMY_SITE_ID = "dummy_dim_id"


def test_get_sites__return_apiCall():

    # WHEN
    call = get_sites()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_site_info__return_apiCall():

    # WHEN
    call = get_site_info(DUMMY_SITE_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_SITE_ID}"
    assert call.method.name == "GET"


def test_create_site__return_apiCall():

    # WHEN
    call = create_site()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_site__return_apiCall():

    # WHEN
    call = update_site(DUMMY_SITE_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_SITE_ID}"
    assert call.method.name == "PUT"


def test_delete_site__return_apiCall():

    # WHEN
    call = delete_site(DUMMY_SITE_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_SITE_ID}"
    assert call.method.name == "DELETE"
