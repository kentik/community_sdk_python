from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.tags import *

DUMMY_API_URL = "/tag"
DUMMY_TAG_ID = "dummy_dim_id"


def test_get_tags__return_apiCall():

    # WHEN
    call = get_tags()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_tag_info__return_apiCall():

    # WHEN
    call = get_tag_info(DUMMY_TAG_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TAG_ID}"
    assert call.method.name == "GET"


def test_create_tag__return_apiCall():

    # WHEN
    call = create_tag()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_tag__return_apiCall():

    # WHEN
    call = update_tag(DUMMY_TAG_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TAG_ID}"
    assert call.method.name == "PUT"


def test_delete_tag__return_apiCall():

    # WHEN
    call = delete_tag(DUMMY_TAG_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TAG_ID}"
    assert call.method.name == "DELETE"
