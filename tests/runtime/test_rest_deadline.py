# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""A numeric REST timeout bounds the whole call, not each read (R5)."""

from __future__ import annotations

import select
import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import httpx
import pytest

from kentik_api.client import KentikAPI
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from kentik_api.errors import AuthenticationError, HTTPException, TransportError
from kentik_api.gen.v5.error import (
    BatchStatusInternalServerErrorError,
    BatchStatusNotFoundError,
)
from kentik_api.v5_tools import BatchWaitTimeout, wait_for_batch

_DRIP_SECONDS = 0.2
_DRIP_CHUNKS = 15


class _DripServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _DripHandler)
        self.client_hung_up = threading.Event()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _DripHandler(BaseHTTPRequestHandler):
    """Answers at once, then sends the body one byte per interval."""

    def do_GET(self) -> None:
        assert isinstance(self.server, _DripServer)
        body = b" " * (_DRIP_CHUNKS - 2) + b"{}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            for index, byte in enumerate(body, start=1):
                self.wfile.write(bytes([byte]))
                self.wfile.flush()
                if index == len(body):
                    return
                readable, _, _ = select.select([self.connection], [], [], _DRIP_SECONDS)
                if readable and not self.connection.recv(1):
                    self.server.client_hung_up.set()
                    return
        except ConnectionError:
            self.server.client_hung_up.set()

    def log_message(self, format: str, *args: Any) -> None:
        pass


@pytest.fixture
def drip_server() -> Iterator[_DripServer]:
    server = _DripServer()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(autouse=True)
def _no_proxy(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)


def _config(base_path: str, **timeouts: Any) -> APIConfig:
    return APIConfig(
        base_path=base_path, auth_email="dev@example.com", auth_token="t", **timeouts
    )


def test_a_trickling_body_cannot_outlast_the_timeout(drip_server):
    config = _config(drip_server.url, timeout=1.0)
    with config.client:
        started = time.monotonic()
        with pytest.raises(TransportError, match="ReadTimeout"):
            request_json("GET", "/v1/test", api_config_override=config)
        assert time.monotonic() - started < 1.0 + _DRIP_SECONDS + 0.5
        assert drip_server.client_hung_up.wait(2.0)


def test_a_numeric_rest_timeout_is_the_deadline(drip_server):
    config = _config(drip_server.url, timeout=60.0, rest_timeout=1.0)
    with config.client:
        with pytest.raises(TransportError, match="ReadTimeout"):
            request_json("GET", "/v1/test", api_config_override=config)
        assert drip_server.client_hung_up.wait(2.0)


def test_a_per_phase_rest_timeout_bounds_each_read_only(drip_server):
    config = _config(drip_server.url, rest_timeout=httpx.Timeout(1.0))
    with config.client:
        started = time.monotonic()
        request_json("GET", "/v1/test", api_config_override=config)
        assert time.monotonic() - started > 1.0
        assert not drip_server.client_hung_up.is_set()


def test_with_timeout_keeps_the_deadline_it_does_not_change():
    base = APIConfig(timeout=60.0, rest_timeout=5.0)

    assert base.with_timeout(grpc_deadline=1.0).rest_deadline == 5.0
    assert base.with_timeout(300).rest_deadline == 300
    assert base.with_timeout(rest_timeout=httpx.Timeout(9.0)).rest_deadline is None


@pytest.mark.parametrize(
    ("rest_timeout", "first", "second", "deadlines"),
    [
        (60.0, (1.0, 1.0, 1.0, 1.0), (0.6, 0.6, 0.6, 0.6), (1.0, 1.0)),
        (0.25, (0.25, 0.25, 0.25, 0.25), (0.25, 0.25, 0.25, 0.25), (0.25, 0.65)),
        (
            httpx.Timeout(connect=0.1, read=5.0, write=0.2, pool=3.0),
            (0.1, 1.0, 0.2, 1.0),
            (0.1, 0.6, 0.2, 0.6),
            (1.0, 1.0),
        ),
    ],
)
def test_batch_budget_reaches_real_generated_requests(
    monkeypatch, batch_clock, rest_timeout, first, second, deadlines
):
    captured = []

    def request(self, method, url, *, timeout, extensions, **kwargs):
        captured.append(
            (tuple(timeout.as_dict().values()), extensions.get("kentik_deadline"))
        )
        return httpx.Response(
            200, json={"guid": "g", "is_complete": len(captured) == 2}
        )

    monkeypatch.setattr(httpx.Client, "request", request)
    with KentikAPI(
        email="dev@example.com", api_token="t", rest_timeout=rest_timeout, env_file=None
    ) as client:
        initial = client.v5_api_config.rest_timeout
        result = wait_for_batch(client, "g", timeout=1.0, interval=0.4)
        assert result.is_complete
        assert client.v5_api_config.rest_timeout == initial
    assert len(captured) == 2
    assert captured[0][0] == pytest.approx(first)
    assert captured[1][0] == pytest.approx(second)
    assert [deadline for _, deadline in captured] == pytest.approx(deadlines)
    assert batch_clock.sleeps == [0.4]


@pytest.mark.parametrize("preparation", [0.25, 1.0, 1.2])
def test_lazy_client_setup_does_not_restart_the_batch_budget(
    monkeypatch, batch_clock, preparation
):
    captured = []

    def transport(self, proxy=None):
        batch_clock.now += preparation
        return httpx.MockTransport(lambda request: httpx.Response(200, json={}))

    def request(self, method, url, *, timeout, extensions, **kwargs):
        captured.append((timeout, extensions))
        return httpx.Response(200, json={"guid": "g", "is_complete": True})

    monkeypatch.setattr(APIConfig, "_transport", transport)
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    monkeypatch.setattr(httpx.Client, "request", request)
    with KentikAPI(email="dev@example.com", api_token="t", env_file=None) as client:
        if preparation < 1.0:
            assert wait_for_batch(client, "g", timeout=1.0).is_complete
            assert captured[0][0] == httpx.Timeout(0.75)
            assert captured[0][1]["kentik_deadline"] == 1.0
        else:
            with pytest.raises(BatchWaitTimeout) as exc:
                wait_for_batch(client, "g", timeout=1.0)
            assert captured == []
            assert exc.value.last_status is None
            assert isinstance(exc.value.__cause__, TransportError)
            assert isinstance(exc.value.__cause__.__cause__, httpx.TimeoutException)


@pytest.mark.parametrize("duration", [0.5, 1.0, 1.2])
@pytest.mark.parametrize(
    ("status_code", "content", "error_type"),
    [
        (401, b'{"error":"fixture"}', AuthenticationError),
        (404, b'{"error":"fixture"}', BatchStatusNotFoundError),
        (500, b'{"error":"fixture"}', BatchStatusInternalServerErrorError),
        (200, b"not-json", HTTPException),
    ],
)
def test_received_batch_errors_keep_their_type_after_the_deadline(
    monkeypatch, batch_clock, duration, status_code, content, error_type
):
    calls = []

    def respond(self, request):
        calls.append(request)
        batch_clock.now += duration
        return httpx.Response(status_code, content=content)

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", respond)
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    with KentikAPI(email="dev@example.com", api_token="t", env_file=None) as client:
        with pytest.raises(error_type) as exc:
            wait_for_batch(client, "g", timeout=1.0)
        assert type(exc.value) is error_type
    assert len(calls) == 1
    assert batch_clock.sleeps == []


@pytest.mark.parametrize("duration", [0.5, 1.0, 1.2])
def test_received_batch_success_still_respects_the_deadline(
    monkeypatch, batch_clock, duration
):
    def respond(self, request):
        batch_clock.now += duration
        return httpx.Response(200, json={"guid": "g", "is_complete": True})

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", respond)
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    with KentikAPI(email="dev@example.com", api_token="t", env_file=None) as client:
        if duration < 1.0:
            assert wait_for_batch(client, "g", timeout=1.0).is_complete
        else:
            with pytest.raises(BatchWaitTimeout):
                wait_for_batch(client, "g", timeout=1.0)
    assert batch_clock.sleeps == []


@pytest.mark.parametrize("rest_timeout", [1.0, httpx.Timeout(1.0)])
def test_buffered_success_preserves_scalar_and_per_phase_timeout_meanings(
    monkeypatch, batch_clock, rest_timeout
):
    def respond(self, request):
        batch_clock.now += 1.2
        return httpx.Response(200, json={"guid": "g", "is_complete": True})

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", respond)
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    with KentikAPI(
        email="dev@example.com", api_token="t", rest_timeout=rest_timeout, env_file=None
    ) as client:
        if isinstance(rest_timeout, httpx.Timeout):
            assert client.v5.batch_status(guid="g").is_complete
        else:
            with pytest.raises(TransportError) as exc:
                client.v5.batch_status(guid="g")
            assert isinstance(exc.value.__cause__, httpx.ReadTimeout)


@pytest.mark.parametrize("duration", [0.5, 1.0, 1.2])
def test_native_batch_timeouts_keep_their_cause_through_the_runtime(
    monkeypatch, batch_clock, duration
):
    original = httpx.ReadTimeout("fixture timeout")

    def respond(self, request):
        batch_clock.now += duration
        raise original

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", respond)
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    expected = TransportError if duration < 1.0 else BatchWaitTimeout
    with (
        KentikAPI(email="dev@example.com", api_token="t", env_file=None) as client,
        pytest.raises(expected) as exc,
    ):
        wait_for_batch(client, "g", timeout=1.0)
    cause = exc.value.__cause__
    if isinstance(exc.value, BatchWaitTimeout):
        assert isinstance(cause, TransportError)
        cause = cause.__cause__
    assert cause is original
    assert batch_clock.sleeps == []


def test_batch_deadline_stops_a_controlled_response_stream(monkeypatch, batch_clock):
    class Stream(httpx.SyncByteStream):
        closed = False

        def __iter__(self):
            batch_clock.now += 0.6
            yield b'{"guid":"g",'
            batch_clock.now += 0.6
            yield b'"is_complete":true}'

        def close(self):
            self.closed = True

    stream = Stream()
    monkeypatch.setattr(
        httpx.HTTPTransport,
        "handle_request",
        lambda self, request: httpx.Response(200, stream=stream),
    )
    monkeypatch.setattr(APIConfig, "_proxy_mounts", lambda self: {})
    with (
        KentikAPI(email="dev@example.com", api_token="t", env_file=None) as client,
        pytest.raises(BatchWaitTimeout) as exc,
    ):
        wait_for_batch(client, "g", timeout=1.0)
    assert exc.value.last_status is None
    assert isinstance(exc.value.__cause__, TransportError)
    assert isinstance(exc.value.__cause__.__cause__, httpx.ReadTimeout)
    assert stream.closed
