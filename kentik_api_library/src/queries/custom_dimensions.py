# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query


@get
def get_custom_dimensions() -> Query:
    """Returns an array of custom dimensions objects that each contain information about an individual custom dimension."""
    return Query("/customdimensions")

@get
def get_custom_dimension_info(custom_dimension_id: int) -> Query:
    """Returns a custom dimension object containing information about an individual custom dimension"""
    url_path = f"/customdimension/{custom_dimension_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_custom_dimension() -> Query:
    """Creates and returns a custom dimension object containing information about an individual custom dimension"""
    return Query("/customdimension")

@put
@payload_type(dict)
def update_custom_dimension(custom_dimension_id: int) -> Query:
    """Updates and returns a custom dimension object containing information about an individual custom dimension"""
    url_path = f"/customdimension/{custom_dimension_id}"
    return Query(url_path)

@delete
def delete_custom_dimension(custom_dimension_id: int) -> Query:
    """Deletes a custom dimension."""
    url_path = f"/customdimension/{custom_dimension_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_populator() -> Query:
    """Creates and returns a populator object containing information about an individual populator"""
    return Query("/customdimension/{custom_dimension_id}/populator")

@put
@payload_type(dict)
def update_populator(custom_dimension_id: int, populator_id: int) -> Query:
    """Updates and returns a populator object containing information about an individual populator"""
    url_path = f"/customdimension/{custom_dimension_id}/populator/{populator_id}"
    return Query(url_path)

@delete
def delete_populator(custom_dimension_id: int, populator_id: int) -> Query:
    """Deletes a populator"""
    url_path = f"/customdimension/{custom_dimension_id}/populator/{populator_id}"
    return Query(url_path)
