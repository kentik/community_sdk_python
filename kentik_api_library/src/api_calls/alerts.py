# Local application imports
from api_calls.api_call_decorators import get, post, put, delete, payload_type
from api_calls.api_call import APICall

@post
@payload_type(dict)
def create_manual_mitigation() -> APICall:
    """Creates a manual mitigation. A mitigation started manually will not clear on its own. 
    It must be stopped manually from the active alerts page."""
    return APICall("/alerts/manual-mitigate")
