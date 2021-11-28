from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.devices import *

DUMMY_API_URL = "/device"
DUMMY_INT_URL = "interface"
DUMMY_DEV_ID = "dummy_dim_id"
DUMMY_INT_ID = "dummy_int_id"


def test_get_devices__return_apiCall():

    # WHEN
    call = get_devices()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_devices_info__return_apiCall():

    # WHEN
    call = get_device_info(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "GET"


def test_create_device__return_apiCall():

    # WHEN
    call = create_device()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_device__return_apiCall():

    # WHEN
    call = update_device(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "PUT"


def test_delete_device__return_apiCall():

    # WHEN
    call = delete_device(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}"
    assert call.method.name == "DELETE"


def test_apply_device_labels():

    # WHEN
    call = apply_device_labels(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s/{DUMMY_DEV_ID}/labels"
    assert call.method.name == "PUT"


def test_get_device_interfaces__return_apiCall():

    # WHEN
    call = get_device_interfaces(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}/{DUMMY_INT_URL}s"
    assert call.method.name == "GET"


def test_get_device_interface_info__return_apiCall():

    # WHEN
    call = get_device_interface_info(DUMMY_DEV_ID, DUMMY_INT_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}/{DUMMY_INT_URL}/{DUMMY_INT_ID}"
    assert call.method.name == "GET"


def test_create_interface__return_apiCall():

    # WHEN
    call = create_interface(DUMMY_DEV_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}/{DUMMY_INT_URL}"
    assert call.method.name == "POST"


def test_update_interface__return_apiCall():

    # WHEN
    call = update_interface(DUMMY_DEV_ID, DUMMY_INT_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}/{DUMMY_INT_URL}/{DUMMY_INT_ID}"
    assert call.method.name == "PUT"


def test_delete_interface__return_apiCall():

    # WHEN
    call = delete_interface(DUMMY_DEV_ID, DUMMY_INT_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DEV_ID}/{DUMMY_INT_URL}/{DUMMY_INT_ID}"
    assert call.method.name == "DELETE"
