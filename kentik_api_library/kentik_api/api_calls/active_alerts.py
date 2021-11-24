# Local application imports
from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call_decorators import get, payload_type


@get
@payload_type(dict)
def get_active_alerts() -> APICall:
    """Get the curently active alerts"""
    return APICall("/alerts-active/alarms")


@get
@payload_type(dict)
def get_active_history() -> APICall:
    """Get the curently active alerts"""
    return APICall("/alerts-active/alerts-history")
