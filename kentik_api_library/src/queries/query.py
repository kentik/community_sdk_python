from enum import Enum


class QueryType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Query:
    def __init__(self, url_path: str, additional_headers: dict = None, method: QueryType = None, payload_type=None):
        self.url_path = url_path
        self.additional_headers = additional_headers
        self.method = method
        self.payload_type = payload_type
