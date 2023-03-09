from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.my_kentik_portal import *

DUMMY_API_URL = "/mykentik/tenant"
DUMMY_USR_URL = "user"
DUMMY_TEN_ID = "dummy_ten_id"
DUMMY_USR_ID = "dummy_usr_id"


def test_get_tenants_return_apiCall():

    # WHEN
    call = get_tenants()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}s"
    assert call.method.name == "GET"


def test_get_tenant_info_return_apiCall():

    # WHEN
    call = get_tenant_info(DUMMY_TEN_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}"
    assert call.method.name == "GET"


def test_create_tenant_user_return_apiCall():

    # WHEN
    call = create_tenant_user(DUMMY_TEN_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}/{DUMMY_USR_URL}"
    assert call.method.name == "POST"


def test_delete_tenant_user_return_apiCall():

    # WHEN
    call = delete_tenant_user(DUMMY_TEN_ID, DUMMY_USR_ID)

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/{DUMMY_TEN_ID}/{DUMMY_USR_URL}/{DUMMY_USR_ID}"
    assert call.method.name == "DELETE"
