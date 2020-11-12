from functools import wraps
from .query import QueryType


def get(func):
    @wraps(func)
    def add_get(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = QueryType.GET
        return query
    return add_get


def post(func):
    @wraps(func)
    def add_post(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = QueryType.POST
        return query
    return add_post


def put(func):
    @wraps(func)
    def add_put(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = QueryType.PUT
        return query
    return add_put


def delete(func):
    @wraps(func)
    def add_delete(*args, **kwargs):
        query = func(*args, **kwargs)
        query.method = QueryType.DELETE
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


def query(tmp):
    return tmp
