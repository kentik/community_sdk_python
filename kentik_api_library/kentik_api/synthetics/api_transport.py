import json
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


class KentikAPIRequestError(Exception):
    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return f"APIRequestError:{self.message}"

    def __str__(self):
        return f"{self.message}"

    @property
    def message(self) -> str:
        return (
            f"{self.response.request.method} {self.response.request.url} failed - "
            f"status: {self.response.status_code} error: {self.response.content.decode()}"
        )

    @property
    def error(self) -> dict:
        try:
            return json.loads(self.response.content.decode())
        except json.decoder.JSONDecodeError:
            return {}


class KentikAPITransport(ABC):
    # noinspection PyUnusedLocal
    @abstractmethod
    def __init__(self, credentials: Tuple[str, str], url: str, proxy: Optional[str]):
        raise NotImplementedError

    @abstractmethod
    def req(self, op: str, **kwargs) -> Any:
        return NotImplementedError
