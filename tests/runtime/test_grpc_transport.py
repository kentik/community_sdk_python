# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The gRPC transport bounds every call with a deadline (FR-001, FR-002, SC-001)."""

from __future__ import annotations

import socket
import threading
import time
from types import SimpleNamespace
from typing import Any

import grpc
import pytest

from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import call_grpc
from kentik_api.errors import ConfigurationError, TransportError
from kentik_api.transports.grpc_client import GrpcTransport, _DefaultDeadlineInterceptor


def _config(**kwargs) -> APIConfig:
    return APIConfig(auth_email="dev@example.com", auth_token="token", **kwargs)


def _details(timeout: float | None) -> Any:
    return SimpleNamespace(
        method="/svc.Service/Op",
        timeout=timeout,
        metadata=None,
        credentials=None,
        wait_for_ready=None,
        compression=None,
    )


def _intercepted_timeout(
    api_config: APIConfig, call_timeout: float | None
) -> float | None:
    seen = {}

    def continuation(details, request) -> Any:
        seen["timeout"] = details.timeout
        seen["method"] = details.method
        return "response"

    result = _DefaultDeadlineInterceptor(
        api_config, lambda: False
    ).intercept_unary_unary(continuation, _details(call_timeout), request=object())
    assert result == "response"
    assert seen["method"] == "/svc.Service/Op"
    return seen["timeout"]


def test_call_without_a_deadline_gets_the_configured_one():
    assert _intercepted_timeout(APIConfig(grpc_deadline=7.5), None) == 7.5


def test_deadline_derives_from_the_shared_timeout_by_default():
    assert _intercepted_timeout(APIConfig(timeout=12.0), None) == 12.0


def test_call_that_already_carries_a_deadline_keeps_it():
    assert _intercepted_timeout(APIConfig(grpc_deadline=7.5), 300.0) == 300.0


def test_transport_uses_the_config_it_is_given():
    config = _config(grpc_deadline=3.0)
    transport = GrpcTransport(config, target="127.0.0.1:1")
    try:
        assert transport.api_config is config
    finally:
        transport.close()


def test_transport_keeps_the_default_deadline_of_its_config():
    transport = GrpcTransport(_config(), target="127.0.0.1:1")
    try:
        assert transport.api_config.auth_email == "dev@example.com"
        assert transport.api_config.grpc_deadline == 60.0
    finally:
        transport.close()


def test_transport_without_credentials_raises_configuration_error():
    with pytest.raises(ConfigurationError, match="auth_email and auth_token"):
        GrpcTransport(APIConfig())


@pytest.fixture
def black_hole_target():
    """A local port that accepts connections and never replies."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen()
    accepted: list[socket.socket] = []
    stop = threading.Event()

    def accept_forever() -> None:
        server.settimeout(0.1)
        while not stop.is_set():
            try:
                accepted.append(server.accept()[0])
            except OSError:
                continue

    thread = threading.Thread(target=accept_forever, daemon=True)
    thread.start()
    yield f"127.0.0.1:{server.getsockname()[1]}"
    stop.set()
    thread.join()
    for conn in accepted:
        conn.close()
    server.close()


def test_unresponsive_server_fails_at_the_deadline_instead_of_hanging(
    black_hole_target,
):
    transport = GrpcTransport(_config(grpc_deadline=0.5), target=black_hole_target)
    stub = transport.channel.unary_unary(
        "/svc.Service/Op",
        request_serializer=lambda _: b"",
        response_deserializer=lambda raw: raw,
    )
    try:
        started = time.monotonic()
        with pytest.raises(TransportError, match="DEADLINE_EXCEEDED"):
            call_grpc(stub, object())
        assert time.monotonic() - started < 5.0
    finally:
        transport.close()


def test_init_wires_credentials_and_deadline_into_the_channel_and_close_releases_it(
    monkeypatch,
):
    calls = {}

    class _FakeChannel:
        closed = False

        def close(self):
            self.closed = True

    raw, intercepted = object(), _FakeChannel()

    def fake_secure_channel(target, creds, options=None):
        calls["target"] = target
        return raw

    def fake_intercept_channel(channel, interceptor):
        calls["inner"] = channel
        calls["interceptor"] = interceptor
        return intercepted

    monkeypatch.setattr(grpc, "secure_channel", fake_secure_channel)
    monkeypatch.setattr(grpc, "intercept_channel", fake_intercept_channel)

    config = _config(grpc_deadline=4.0)
    transport = GrpcTransport(config, target="grpc.example.com:443")

    assert calls["target"] == "grpc.example.com:443"
    assert calls["inner"] is raw
    assert isinstance(calls["interceptor"], _DefaultDeadlineInterceptor)
    assert calls["interceptor"]._api_config is config
    assert transport.channel is intercepted

    transport.close()
    assert intercepted.closed


def test_channel_options_raise_the_receive_limit_and_let_callers_override_it():
    from kentik_api.transports.grpc_client import channel_options

    assert dict(channel_options())["grpc.max_receive_message_length"] == 40 * 1024**2
    assert dict(channel_options([("grpc.max_receive_message_length", 1)])) == {
        "grpc.max_receive_message_length": 1
    }


def test_transport_passes_the_channel_options_to_grpc(monkeypatch):
    seen = {}

    def fake_secure_channel(target, creds, options=None):
        seen["options"] = dict(options or ())
        return object()

    monkeypatch.setattr(grpc, "secure_channel", fake_secure_channel)
    monkeypatch.setattr(grpc, "intercept_channel", lambda channel, _: channel)

    GrpcTransport(_config(), options=[("grpc.keepalive_time_ms", 5000)])

    assert seen["options"]["grpc.keepalive_time_ms"] == 5000
    assert seen["options"]["grpc.max_receive_message_length"] == 40 * 1024**2


def _serve_blob(size: int):
    handler = grpc.method_handlers_generic_handler(
        "svc.Service",
        {
            "Op": grpc.unary_unary_rpc_method_handler(
                lambda request, context: b"x" * size,
                request_deserializer=lambda raw: raw,
                response_serializer=lambda raw: raw,
            )
        },
    )
    from concurrent import futures

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1),
        options=[("grpc.max_send_message_length", -1)],
    )
    server.add_generic_rpc_handlers((handler,))
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    return server, port


def _call_blob(port: int, options):
    from kentik_api.transports.grpc_client import channel_options

    channel = grpc.insecure_channel(
        f"127.0.0.1:{port}", options=channel_options(options)
    )
    stub = channel.unary_unary(
        "/svc.Service/Op",
        request_serializer=lambda raw: raw,  # pyright: ignore[reportArgumentType]
        response_deserializer=lambda raw: raw,
    )
    try:
        return call_grpc(stub, b"")[0]
    finally:
        channel.close()


def test_a_five_megabyte_response_succeeds_with_the_default_limit():
    server, port = _serve_blob(5 * 1024**2)
    try:
        assert len(_call_blob(port, None)) == 5 * 1024**2
    finally:
        server.stop(0)


def test_a_response_over_the_limit_is_a_transport_error_not_a_quota_error():
    from kentik_api.errors import HTTPException

    server, port = _serve_blob(5 * 1024**2)
    try:
        with pytest.raises(TransportError, match="receive limit") as exc_info:
            _call_blob(port, [("grpc.max_receive_message_length", 1024)])
        assert not isinstance(exc_info.value, HTTPException)
    finally:
        server.stop(0)


AUDIT = "/kentik.audit.public.v202601.AuditService/ListAuditEvents"
LABEL = "/kentik.label.v202210.LabelService/ListLabels"


def _serve_recording_deadlines(seen: dict[str, float | None]):
    """Answers AUDIT and LABEL, and records the deadline each one received."""
    from concurrent import futures

    def handler(method: str):
        def respond(request, context):
            seen[method] = context.time_remaining()
            return b"ok"

        return grpc.unary_unary_rpc_method_handler(
            respond,
            request_deserializer=lambda raw: raw,
            response_serializer=bytes,
        )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    for method in (AUDIT, LABEL):
        service, _, name = method.lstrip("/").rpartition("/")
        server.add_generic_rpc_handlers(
            (grpc.method_handlers_generic_handler(service, {name: handler(method)}),)
        )
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    return server, port


def _intercepted_stub(target: str, method: str, config: APIConfig):
    channel = grpc.intercept_channel(
        grpc.insecure_channel(target),
        _DefaultDeadlineInterceptor(config, lambda: False),
    )
    stub = channel.unary_unary(
        method,
        request_serializer=lambda raw: raw,  # pyright: ignore[reportArgumentType]
        response_deserializer=lambda raw: raw,
    )
    return channel, stub


def test_affected_services_are_sent_no_deadline_and_others_still_are():
    seen: dict[str, float | None] = {}
    server, port = _serve_recording_deadlines(seen)
    try:
        for method in (AUDIT, LABEL):
            channel, stub = _intercepted_stub(
                f"127.0.0.1:{port}", method, APIConfig(grpc_deadline=30.0)
            )
            try:
                assert call_grpc(stub, b"")[0] == b"ok"
            finally:
                channel.close()
    finally:
        server.stop(0)

    # grpcio reports "no deadline" as an effectively infinite time remaining.
    no_deadline = seen[AUDIT]
    assert no_deadline is not None and no_deadline > 1e9
    remaining = seen[LABEL]
    assert remaining is not None
    assert remaining == pytest.approx(30.0, abs=1.0)


def test_affected_service_still_fails_at_the_deadline_instead_of_hanging(
    black_hole_target,
):
    channel, stub = _intercepted_stub(
        black_hole_target, AUDIT, APIConfig(grpc_deadline=0.5)
    )
    try:
        started = time.monotonic()
        with pytest.raises(TransportError, match="DEADLINE_EXCEEDED"):
            call_grpc(stub, b"")
        assert time.monotonic() - started < 5.0
    finally:
        channel.close()


def test_affected_service_honors_a_per_call_deadline(black_hole_target):
    config = APIConfig(grpc_deadline=60.0)
    channel, stub = _intercepted_stub(black_hole_target, AUDIT, config)
    try:
        started = time.monotonic()
        with pytest.raises(TransportError, match="DEADLINE_EXCEEDED"):
            call_grpc(stub, b"", api_config=config.with_timeout(grpc_deadline=0.5))
        assert time.monotonic() - started < 5.0
    finally:
        channel.close()
