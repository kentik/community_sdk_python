# Local application imports
from queries.query_decorators import get
from queries.query import Query

@get
def get_plans() -> Query:
    """Returns an array of plans objects that each contain information about an individual plan."""
    return Query("/plans")
