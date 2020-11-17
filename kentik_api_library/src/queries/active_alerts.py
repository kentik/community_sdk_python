# Local application imports
from queries.query_decorators import get, payload_type
from queries.query import Query


@get
@payload_type(dict)
def get_active_alerts() -> Query:
    """Get the curently active alerts"""
    return Query("/alerts-active/alarms")


@get
@payload_type(dict)
def get_active_history() -> Query:
    """Get the curently active alerts"""
    return Query("/alerts-active/alerts-history")
