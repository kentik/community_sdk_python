from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.device_labels import *

DUMMY_API_URL = "/deviceLabels"
DUMMY_DEV_ID = "dummy_dim_id"


def test_get_device_labels__return_apiCall():

    # WHEN
    call = get_device_labels()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}"
    assert call.method.name == "GET"


def test_get_device_labels_info__return_apiCall():

    # WHEN
    call = get_device_label_info(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "GET"


def test_create_device_label__return_apiCall():

    # WHEN
    call = create_device_label()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_device_label__return_apiCall():

    # WHEN
    call = update_device_label(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "PUT"


def test_delete_device_label__return_apiCall():

    # WHEN
    call = delete_device_label(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "DELETE"
