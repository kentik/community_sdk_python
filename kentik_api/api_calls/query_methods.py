# Local application imports
from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call_decorators import payload_type, post


@post
@payload_type(dict)
def query_sql() -> APICall:
    """This method allows to run a SQL command against all configured devices.
    Returns top X datasets."""
    return APICall("/query/sql")


@post
@payload_type(dict)
def query_url() -> APICall:
    """Returns a URL which a logged in user can use to directly access this query
    in Data Explorer in the Kentik Detect portal."""
    return APICall("/query/url")


@post
@payload_type(dict)
def query_data() -> APICall:
    """A Top X Query in Kentik Detect’s KDE (see KDE Tables).
    Returns results in a JSON results array."""
    return APICall("/query/topXdata")


@post
@payload_type(dict)
def query_chart() -> APICall:
    """Returns an image of a graph similar to what is seen in the Kentik portal's Data Explorer
    in JSON object with one dataURI member,
    the value of which is a base64 encoded string that represents a file."""
    return APICall("/query/topXchart")
