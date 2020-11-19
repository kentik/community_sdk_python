from src.api_calls.api_call import APICall
from src.api_calls.api_call import APICallMethods
from src.api_calls.plan import *

DUMMY_API_URL = "/plans"


def test_get_plans__return_apiCall():

    # WHEN
    call = get_plans()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}"
    assert call.method.name == "GET"
