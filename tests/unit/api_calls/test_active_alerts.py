from kentik_api.api_calls.active_alerts import *
from kentik_api.api_calls.api_call import APICall, APICallMethods

DUMMY_API_URL = "/alerts-active"


def test_get_active_alerts__return_apiCall():

    # WHEN
    call = get_active_alerts()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/alarms"
    assert call.method.name == "GET"


def test_get_active_history__return_apiCall():

    # WHEN
    call = get_active_history()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/alerts-history"
    assert call.method.name == "GET"
