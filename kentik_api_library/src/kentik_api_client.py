# Standard library imports
from typing import Optional

# Local application imports
from .queries.query import Query


class KentikAPIClient:
    def __init__(self, auth_email: str, auth_token: str):
        pass

    def send_call(self, query: Query, payload: Optional[type]):
        pass

    @staticmethod
    def get_synchronous_client():
        pass

    @staticmethod
    def get_asynchronous_client(self):
        pass
