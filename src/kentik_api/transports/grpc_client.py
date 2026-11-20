# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
import collections
import threading
from collections.abc import Callable, Sequence
from typing import Any

import grpc

from kentik_api.auth.credentials import KentikCredentials
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rate_limit import RateLimit, rate_limit_of_rpc
from kentik_api.errors import ConfigurationError
from kentik_api.transports.base import BaseTransport

# grpcio keeps a 4 MiB receive limit, which a large account's list call exceeds.
# 1.0.7 allowed 40 MiB, and REST has no such limit.
_MAX_RECEIVE_BYTES = 40 * 1024 * 1024

# Upstream bug: these services fail every call that carries a deadline with a
# server RangeError. Their calls are sent without one and ended by the client
_NO_SERVER_DEADLINE = frozenset(
    {
        "alerting",
        "audit",
        "custom_application",
        "custom_dimension",
        "plan",
        "saved_filter",
    }
)


def _service_of(method: str | bytes) -> str:
    """`audit` for `/kentik.audit.public.v202601.AuditService/ListAuditEvents`."""
    if isinstance(method, bytes):
        method = method.decode("utf-8", errors="replace")
    package, _, rest = method.lstrip("/").partition(".")
    return rest.partition(".")[0] if package == "kentik" else ""


def _cancel_after(call, seconds: float) -> None:
    timer = threading.Timer(seconds, call.cancel)
    timer.daemon = True
    timer.start()
    call.add_done_callback(lambda _: timer.cancel())


def channel_options(
    extra: Sequence[tuple[str, Any]] | None = None,
) -> list[tuple[str, Any]]:
    """Channel options with the SDK defaults; a caller's option wins on the same key."""
    merged = {"grpc.max_receive_message_length": _MAX_RECEIVE_BYTES}
    merged.update(dict(extra or ()))
    return list(merged.items())


class _CallDetails(
    collections.namedtuple(
        "_CallDetails",
        (
            "method",
            "timeout",
            "metadata",
            "credentials",
            "wait_for_ready",
            "compression",
        ),
    ),
    grpc.ClientCallDetails,
):
    """grpc.ClientCallDetails is abstract; interceptors must supply their own."""


class _DefaultDeadlineInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Bounds every call on the channel without touching generated call sites.

    Generated wrappers call stubs with no timeout, and gRPC's default is to
    wait forever. A deadline the call already carries is left alone, so a
    per-call override takes precedence over the client-wide default.
    """

    def __init__(self, api_config: APIConfig, is_closed: Callable[[], bool]) -> None:
        self._api_config = api_config
        self._is_closed = is_closed

    def intercept_unary_unary(self, continuation, client_call_details, request):
        if self._is_closed():
            raise ConfigurationError(
                "This client was closed with close(); create a new KentikAPI to make more calls."
            )

        deadline = client_call_details.timeout
        if deadline is None:
            deadline = self._api_config.grpc_deadline
        client_side = _service_of(client_call_details.method) in _NO_SERVER_DEADLINE
        sent = None if client_side else deadline
        if sent != client_call_details.timeout:
            client_call_details = _CallDetails(
                method=client_call_details.method,
                timeout=sent,
                metadata=client_call_details.metadata,
                credentials=client_call_details.credentials,
                wait_for_ready=client_call_details.wait_for_ready,
                compression=client_call_details.compression,
            )
        outcome = continuation(client_call_details, request)
        if client_side:
            # Bounds only a future(); call_grpc uses one for this reason.
            _cancel_after(outcome, deadline)
        self._record_rate_limit(client_call_details.method, outcome)
        return outcome

    def _record_rate_limit(self, method, outcome) -> None:
        # A failed outcome reports no metadata itself; the RpcError it holds does.
        try:
            failure = outcome.exception() if hasattr(outcome, "exception") else None
        except grpc.FutureCancelledError:
            return
        rate_limit = rate_limit_of_rpc(failure if failure is not None else outcome)
        if rate_limit is not None:
            key = (
                method.decode("utf-8", errors="replace")
                if isinstance(method, bytes)
                else str(method)
            )
            self._api_config.rate_limits[key] = rate_limit


class GrpcTransport(BaseTransport):
    channel: grpc.Channel  # set by __init__; declared here so mock spec includes it
    api_config: APIConfig

    def __init__(
        self,
        api_config: APIConfig,
        target: str = "grpc.api.kentik.com:443",
        options: Sequence[tuple[str, Any]] | None = None,
    ):
        if not api_config.auth_email or not api_config.auth_token:
            raise ConfigurationError(
                "GrpcTransport needs an APIConfig with auth_email and auth_token."
            )
        self.api_config = api_config

        credentials = KentikCredentials(api_config.auth_email, api_config.auth_token)
        auth_plugin = credentials.get_grpc_plugin()
        call_creds = grpc.metadata_call_credentials(auth_plugin)
        channel_creds = grpc.ssl_channel_credentials()
        composite_creds = grpc.composite_channel_credentials(channel_creds, call_creds)

        self.channel = grpc.intercept_channel(
            grpc.secure_channel(
                target, composite_creds, options=channel_options(options)
            ),
            _DefaultDeadlineInterceptor(self.api_config, self._is_closed),
        )
        self._closed = False

    @property
    def rate_limits(self) -> dict[str, RateLimit]:
        """Quota per gRPC method, as of the last call to each."""
        return self.api_config.rate_limits

    def close(self):
        if self._closed:
            return
        self.channel.close()
        self._closed = True

    def _is_closed(self) -> bool:
        return self._closed
