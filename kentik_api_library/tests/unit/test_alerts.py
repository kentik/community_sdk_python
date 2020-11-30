from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_calls.alerts import *


DUMMY_API_URL = "/alerts"


def test_create_manual_mitigation__return_apiCall():

    # WHEN
    call = create_manual_mitigation()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/manual-mitigate"
    assert call.method.name == "POST"
