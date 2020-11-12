from .query_decorators import get, post, put, delete, payload_type
from .query import Query

@get
def get_plans() -> Query:
    """Returns an array of plans objects that each contain information about an individual plan."""
    return Query("/plans")
