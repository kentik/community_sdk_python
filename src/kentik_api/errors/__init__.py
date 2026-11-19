# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

from typing import Any, Optional

from kentik_api.core.rate_limit import RateLimit


class KentikError(Exception):
    """Base exception for all SDK-specific errors."""

    rate_limit: RateLimit | None = None


class ConfigurationError(KentikError):
    """Raised for invalid SDK configuration values."""


class AuthenticationError(KentikError):
    """Raised when the API rejects the credentials.

    That is a REST 401 or a gRPC UNAUTHENTICATED status.
    """


class TransportError(KentikError):
    """Raised when the transport fails before a valid response arrives.

    `may_have_reached_server` is false only when the SDK knows it did not send
    the request. True means the server may have received it, not that it did.
    """

    may_have_reached_server: bool = True


class HTTPException(KentikError):
    """Raised when an API HTTP response does not match expectations."""

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        method: str | None = None,
        path: str | None = None,
        details: dict[str, Any] | None = None,
        grpc_status_code: str | None = None,
    ):
        self.status_code = status_code
        self.grpc_status_code = grpc_status_code
        self.message = message
        self.method = method
        self.path = path
        self.details = details or {}
        super().__init__(f"{status_code}: {message}")

    def __reduce__(self):
        # Exception's default pickling replays args, which this signature rejects.
        return (_rebuild_http_exception, (type(self), self.__dict__.copy()))


def _rebuild_http_exception(cls: type[HTTPException], state: dict[str, Any]):
    error = cls.__new__(cls)
    error.__dict__.update(state)
    error.args = (f"{state['status_code']}: {state['message']}",)
    return error


__all__ = [
    "AuthenticationError",
    "ConfigurationError",
    "HTTPException",
    "KentikError",
    "TransportError",
]
