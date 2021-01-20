from typing import Optional

from kentik_api.api_calls.api_call_decorators import get, post, payload_type
from kentik_api.api_calls.api_call import APICall


@post
@payload_type(dict)
def create_manual_mitigation() -> APICall:
    """Creates a manual mitigation. A mitigation started manually will not clear on its own.
    It must be stopped manually from the active alerts page."""
    return APICall("/alerts/manual-mitigate")


@get
def get_active_alerts(
    startTime: str,
    endTime: str,
    filterBy: str,
    filterVal: str,
    showMitigations: int,
    showAlarms: int,
    showMatches: int,
    learningMode: int,
) -> APICall:
    """ Returns active alerts (alarms)."""
    return APICall(
        f"/alerts-active/alarms?startTime={startTime}&endTime={endTime}&filterBy={filterBy}&"
        f"filterVal={filterVal}&showMitigations={showMitigations}&showAlarms={showAlarms}&"
        f"showMatches={showMatches}&learningMode={learningMode}"
    )


@get
def get_alerts_history(
    startTime: str,
    endTime: str,
    filterBy: str,
    filterVal: str,
    sortOrder: Optional[str],
    showMitigations: int,
    showAlarms: int,
    showMatches: int,
    learningMode: int,
) -> APICall:
    """ Returns active alerts (alarms)."""
    return APICall(
        f"/alerts-active/alerts-history?startTime={startTime}&endTime={endTime}&filterBy={filterBy}&"
        f"filterVal={filterVal}&sortOrder={sortOrder}&showMitigations={showMitigations}&showAlarms={showAlarms}&"
        f"showMatches={showMatches}&learningMode={learningMode}"
    )
