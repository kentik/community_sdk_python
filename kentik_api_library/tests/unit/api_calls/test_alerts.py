from kentik_api.api_calls.alerts import *
from kentik_api.api_calls.api_call import APICall

DUMMY_API_URL = "/alerts"
DUMMY_START_DATE = "2018-10-15T22:15:00"
DUMMY_END_DATE = "2020-10-15T22:15:00"
DUMMY_FILTER_BY = "old_state"
DUMMY_FILTER_VALUE = "state_val"
DUMMY_SHOW_MITIGATIONS = 1
DUMMY_SHOW_ALARMS = 1
DUMMY_SHOW_MATCHES = 0
DUMMY_LEARNING_MODE = 0
DUMMY_SORT_ORDER = 2


def test_create_manual_mitigation__return_apiCall():

    # WHEN
    call = create_manual_mitigation()

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == f"{DUMMY_API_URL}/manual-mitigate"
    assert call.method.name == "POST"


def test_get_active_alerts_return_apiCall():

    # WHEN
    call = get_active_alerts(
        DUMMY_START_DATE,
        DUMMY_END_DATE,
        DUMMY_FILTER_BY,
        DUMMY_FILTER_VALUE,
        DUMMY_SHOW_MITIGATIONS,
        DUMMY_SHOW_ALARMS,
        DUMMY_SHOW_MATCHES,
        DUMMY_LEARNING_MODE,
    )

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == (
        "/alerts-active/alarms?startTime=2018-10-15T22:15:00&endTime=2020-10-15T22:15:00&"
        "filterBy=old_state&filterVal=state_val&showMitigations=1&showAlarms=1&showMatches=0&learningMode=0"
    )
    assert call.method.name == "GET"


def test_get_alerts_history_return_apiCall():

    # WHEN
    call = get_alerts_history(
        DUMMY_START_DATE,
        DUMMY_END_DATE,
        DUMMY_FILTER_BY,
        DUMMY_FILTER_VALUE,
        DUMMY_SORT_ORDER,
        DUMMY_SHOW_MITIGATIONS,
        DUMMY_SHOW_ALARMS,
        DUMMY_SHOW_MATCHES,
        DUMMY_LEARNING_MODE,
    )

    # THEN
    assert isinstance(call, APICall)
    assert call.url_path == (
        "/alerts-active/alerts-history?startTime=2018-10-15T22:15:00&endTime=2020-10-15T22:15:00&"
        "filterBy=old_state&filterVal=state_val&sortOrder=2&showMitigations=1&showAlarms=1&showMatches=0&learningMode=0"
    )
    assert call.method.name == "GET"
