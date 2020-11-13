# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query

@post
@payload_type(dict)
def create_manual_mitigation() -> Query:
    """Creates a manual mitigation. A mitigation started manually will not clear on its own. 
    It must be stopped manually from the active alerts page."""
    return Query("/alerts/manual-mitigate")
