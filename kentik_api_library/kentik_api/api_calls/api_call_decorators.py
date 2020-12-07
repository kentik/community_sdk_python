# Standard library imports
from functools import wraps

# Local application imports
from kentik_api.api_calls.api_call import APICallMethods


def get(func):
    @wraps(func)
    def add_get(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = APICallMethods.GET
        return query
    return add_get


def post(func):
    @wraps(func)
    def add_post(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = APICallMethods.POST
        # print(query.method)
        return query
    return add_post


def put(func):
    @wraps(func)
    def add_put(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = APICallMethods.PUT
        return query
    return add_put


def delete(func):
    @wraps(func)
    def add_delete(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = APICallMethods.DELETE
        return query
    return add_delete


def payload_type(_type: type):
    def actual_decorator(func):
        @wraps(func)
        def add_payload_type(*args, **kwargs):
            query = func(*args, **kwargs)
            query.payload_type = _type
            return query
        return add_payload_type
    return actual_decorator
