from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.plans import get_plans

DUMMY_API_URL = "/plans"


def test_get_plans__return_apiCall():

    # WHEN
    call = get_plans()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}"
    assert call.method.name == "GET"
