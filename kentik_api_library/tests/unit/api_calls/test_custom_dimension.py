from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.custom_dimensions import *

DUMMY_API_URL = "/customdimension"
DUMMY_POP_URL = "populator"
DUMMY_DIM_ID = "dummy_dim_id"
DUMMY_POP_ID = "dummy_pop_id"


def test_get_custom_dimensions__return_apiCall():

    # WHEN
    call = get_custom_dimensions()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_custom_dimension_info__return_apiCall():

    # WHEN
    call = get_custom_dimension_info(DUMMY_DIM_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}"
    assert call.method.name == "GET"


def test_create_custom_dimension__return_apiCall():

    # WHEN
    call = create_custom_dimension()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == DUMMY_API_URL
    assert call.method.name == "POST"


def test_update_custom_dimension__return_apiCall():

    # WHEN
    call = update_custom_dimension(DUMMY_DIM_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}"
    assert call.method.name == "PUT"


def test_delete_custom_dimension__return_apiCall():

    # WHEN
    call = delete_custom_dimension(DUMMY_DIM_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}"
    assert call.method.name == "DELETE"


def test_create_populator__return_apiCall():

    # WHEN
    call = create_populator(DUMMY_DIM_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}/{DUMMY_POP_URL}"
    assert call.method.name == "POST"


def test_update_populator__return_apiCall():

    # WHEN
    call = update_populator(DUMMY_DIM_ID, DUMMY_POP_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}/{DUMMY_POP_URL}/{DUMMY_POP_ID}"
    assert call.method.name == "PUT"


def test_delete_populator__return_apiCall():

    # WHEN
    call = delete_populator(DUMMY_DIM_ID, DUMMY_POP_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_DIM_ID}/{DUMMY_POP_URL}/{DUMMY_POP_ID}"
    assert call.method.name == "DELETE"
