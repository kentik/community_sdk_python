from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.query_methods import *

DUMMY_API_URL = "/query"


def test_query_sql__return_apiCall():

    # WHEN
    call = query_sql()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/sql"
    assert call.method.name == "POST"


def test_query_url__return_apiCall():

    # WHEN
    call = query_url()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/url"
    assert call.method.name == "POST"


def test_query_data__return_apiCall():

    # WHEN
    call = query_data()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/topXdata"
    assert call.method.name == "POST"


def test_query_chart__return_apiCall():

    # WHEN
    call = query_chart()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/topXchart"
    assert call.method.name == "POST"
