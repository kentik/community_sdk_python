from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call_decorators import get, payload_type, post


@post
@payload_type(dict)
def create_manual_mitigation() -> APICall:
    """Creates a manual mitigation. A mitigation started manually will not clear on its own.
    It must be stopped manually from the active alerts page."""
    return APICall("/alerts/manual-mitigate")


@get
def get_active_alerts(
    start_time: str,
    end_time: str,
    filter_by: str,
    filter_val: str,
    show_mitigations: int,
    show_alarms: int,
    show_matches: int,
    learning_mode: int,
) -> APICall:
    """Returns active alerts (alarms)."""
    return APICall(
        f"/alerts-active/alarms?startTime={start_time}&endTime={end_time}&filterBy={filter_by}&"
        f"filterVal={filter_val}&showMitigations={show_mitigations}&showAlarms={show_alarms}&"
        f"showMatches={show_matches}&learningMode={learning_mode}"
    )


@get
def get_alerts_history(
    start_time: str,
    end_time: str,
    filter_by: str,
    filter_val: str,
    sort_order: str,
    show_mitigations: int,
    show_alarms: int,
    show_matches: int,
    learning_mode: int,
) -> APICall:
    """Returns active alerts (alarms)."""
    return APICall(
        f"/alerts-active/alerts-history?startTime={start_time}&endTime={end_time}&filterBy={filter_by}&"
        f"filterVal={filter_val}&sortOrder={sort_order}&showMitigations={show_mitigations}&showAlarms={show_alarms}&"
        f"showMatches={show_matches}&learningMode={learning_mode}"
    )
