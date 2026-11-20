# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

from typing import Any

import httpx
import pytest

from kentik_api.core.api_config import APIConfig, HTTPException
from kentik_api.core.grpc_runtime import call_grpc
from kentik_api.core.rest_runtime import path_segment, request_json
from kentik_api.errors import ConfigurationError, TransportError
from kentik_api.transports.grpc_client import GrpcTransport


def _config(**kwargs) -> APIConfig:
    return APIConfig(
        base_path="https://api.example.com",
        auth_email="dev@example.com",
        auth_token="token",
        **kwargs,
    )


def test_request_json_success_builds_headers_and_filters_query(
    monkeypatch: pytest.MonkeyPatch,
):
    captured = {}

    def _fake_request(self, method, url, headers=None, params=None, json=None, **_):
        captured["method"] = method
        captured["url"] = str(url)
        captured["headers"] = headers
        captured["params"] = params
        captured["json"] = json
        return httpx.Response(200, json={"ok": True})

    monkeypatch.setattr(httpx.Client, "request", _fake_request)

    cfg = APIConfig(
        base_path="https://api.example.com",
        auth_email="dev@example.com",
        auth_token="token",
        verify=True,
    )

    result = request_json(
        method="POST",
        path="/v1/test",
        api_config_override=cfg,
        query_params={"keep": 1, "drop": None},
        json_body={"hello": "world"},
        expected_status=200,
        operation_name="UnitTest",
    )

    assert result == {"ok": True}
    assert captured["method"] == "post"
    assert captured["url"] == "/v1/test?keep=1"
    assert captured["headers"]["X-CH-Auth-Email"] == "dev@example.com"
    assert captured["headers"]["X-CH-Auth-API-Token"] == "token"
    assert captured["params"] is None
    assert captured["json"] == {"hello": "world"}


def test_query_values_encode_a_space_as_percent_20(monkeypatch: pytest.MonkeyPatch):
    # Envoy's transcoder does not decode "+" by default, so it would reach the
    # gRPC service as a literal plus sign.
    sent = []
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, method, url, **_: (
            sent.append(str(url)) or httpx.Response(200, json={})
        ),
    )

    request_json(
        "GET",
        "/v1/test",
        api_config_override=_config(),
        query_params={"prompt": "a b+c", "flag": True, "ids": [1, 2]},
    )

    assert sent == ["/v1/test?prompt=a%20b%2Bc&flag=true&ids=1&ids=2"]


def test_request_json_returns_none_for_204(monkeypatch: pytest.MonkeyPatch):
    def _fake_request(self, method, url, headers=None, params=None, json=None, **_):
        return httpx.Response(204)

    monkeypatch.setattr(httpx.Client, "request", _fake_request)

    result = request_json(
        method="GET",
        path="/v1/no-content",
        api_config_override=_config(),
        expected_status=204,
    )
    assert result is None


def test_request_json_raises_http_exception_on_unexpected_status(
    monkeypatch: pytest.MonkeyPatch,
):
    def _fake_request(self, method, url, headers=None, params=None, json=None, **_):
        return httpx.Response(500, json={"error": "boom"})

    monkeypatch.setattr(httpx.Client, "request", _fake_request)

    with pytest.raises(HTTPException) as exc:
        request_json(
            method="GET",
            path="/v1/fail",
            api_config_override=_config(),
            expected_status=200,
            operation_name="FailingOp",
        )

    assert exc.value.status_code == 500
    assert "FailingOp failed with status code: 500" in str(exc.value)


def test_request_json_applies_the_configured_rest_timeout_per_request(
    monkeypatch: pytest.MonkeyPatch,
):
    captured = {}

    def _fake_request(self, *args, timeout=None, **kwargs):
        captured["timeout"] = timeout
        return httpx.Response(200, json={})

    monkeypatch.setattr(httpx.Client, "request", _fake_request)
    phases = httpx.Timeout(connect=2.0, read=300.0, write=10.0, pool=5.0)

    request_json("GET", "/v1/test", api_config_override=_config(rest_timeout=phases))

    assert captured["timeout"] == phases
    assert captured["timeout"] is not phases


def test_config_without_credentials_is_rejected_before_sending(
    monkeypatch: pytest.MonkeyPatch,
):
    def _must_not_send(self, *args, **kwargs):
        raise AssertionError("an unauthenticated request was sent")

    monkeypatch.setattr(httpx.Client, "request", _must_not_send)

    for config in (None, APIConfig(base_path="https://api.example.com")):
        with pytest.raises(ConfigurationError, match="no credentials"):
            request_json(
                "GET", "/v1/test", api_config_override=config, operation_name="Op"
            )


@pytest.mark.parametrize("phase", ["connect", "read", "write", "pool"])
@pytest.mark.parametrize("exposure", ["input", "getter"])
@pytest.mark.parametrize("warm", [False, True])
def test_timeout_mutation_never_reaches_a_request(monkeypatch, phase, exposure, warm):
    captured = []

    def capture(self, *args, timeout, extensions, **kwargs):
        captured.append((timeout.as_dict(), extensions))
        return httpx.Response(200, json={})

    monkeypatch.setattr(httpx.Client, "request", capture)
    supplied = httpx.Timeout(connect=2.0, read=3.0, write=5.0, pool=7.0)
    config = _config(rest_timeout=supplied)
    try:
        if warm:
            request_json("GET", "/fixture", api_config_override=config)
        exposed = supplied if exposure == "input" else config.rest_timeout
        setattr(exposed, phase, None)

        request_json("GET", "/fixture", api_config_override=config)
        request_json(
            "GET", "/fixture", api_config_override=config.with_timeout(grpc_deadline=9)
        )

        assert all(
            limits == {"connect": 2.0, "read": 3.0, "write": 5.0, "pool": 7.0}
            for limits, _ in captured
        )
        assert all(extensions == {} for _, extensions in captured)
    finally:
        config.close()


SOFT_LIMIT_DELAY_SECONDS = 1.5


def test_default_timeout_absorbs_the_soft_limit_delay():
    import threading
    import time
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class _ThrottledHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            time.sleep(SOFT_LIMIT_DELAY_SECONDS + 0.1)
            body = b'{"ok": true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), _ThrottledHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    config = APIConfig(
        base_path=f"http://127.0.0.1:{server.server_address[1]}",
        auth_email="dev@example.com",
        auth_token="token",
    )
    try:
        assert request_json("GET", "/v1/test", api_config_override=config) == {
            "ok": True
        }
    finally:
        config.close()
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("value", "segment"),
    [
        ("../../user/7", "..%2F..%2Fuser%2F7"),
        ("a?b#c d%", "a%3Fb%23c%20d%25"),
        # grpc-gateway leaves reserved characters encoded, so they must stay raw.
        ("2024-01-01T00:00:00Z", "2024-01-01T00:00:00Z"),
        (42, "42"),
    ],
)
def test_path_segment_keeps_the_value_inside_its_segment(value, segment):
    assert path_segment(value) == segment


@pytest.mark.parametrize("value", ["", ".", ".."])
def test_path_segment_refuses_values_that_change_the_route(value):
    with pytest.raises(ValueError, match="path parameter"):
        path_segment(value)


def test_request_json_rejects_control_char_credentials_before_request(
    monkeypatch: pytest.MonkeyPatch,
):
    def _must_not_send(self, *args, **kwargs):
        raise AssertionError("request should not be sent")

    monkeypatch.setattr(httpx.Client, "request", _must_not_send)

    with pytest.raises(ConfigurationError, match="contains control characters"):
        request_json(
            "GET",
            "/v1/test",
            api_config_override=APIConfig(
                base_path="https://api.example.com",
                auth_email="dev@example.com",
                auth_token="tok\x1bn",
            ),
            operation_name="ListUsers",
        )


def test_transport_error_message_does_not_leak_header_values(
    monkeypatch: pytest.MonkeyPatch,
):
    sensitive_token = "s3cr3t-token-value"

    def _raise_local_protocol_error(
        self, method, url, headers=None, params=None, json=None, **_
    ):
        raise httpx.LocalProtocolError(f"Illegal header value b'{sensitive_token}\\n'")

    monkeypatch.setattr(httpx.Client, "request", _raise_local_protocol_error)

    with pytest.raises(TransportError) as exc_info:
        request_json(
            "GET",
            "/v1/test",
            api_config_override=APIConfig(
                base_path="https://api.example.com",
                auth_email="dev@example.com",
                auth_token=sensitive_token,
            ),
            operation_name="ListUsers",
        )

    message = str(exc_info.value)
    assert sensitive_token not in message
    assert "Illegal header value" not in message


def test_grpc_call_after_close_raises_configuration_error_not_process_crash():
    transport = GrpcTransport(
        APIConfig(auth_email="dev@example.com", auth_token="token"),
        target="127.0.0.1:1",
    )
    stub = transport.channel.unary_unary(
        "/svc.Service/Op",
        request_serializer=lambda _: b"",
        response_deserializer=lambda raw: raw,
    )
    transport.close()

    with pytest.raises(ConfigurationError, match="closed"):
        call_grpc(stub, object())


@pytest.mark.parametrize("status", [200, 500])
def test_non_utf8_body_raises_an_sdk_error_not_unicode_decode_error(
    monkeypatch: pytest.MonkeyPatch, status: int
):
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, *a, **k: httpx.Response(status, content=b"\xff\xfe\x00bad"),
    )

    with pytest.raises(HTTPException):
        request_json("GET", "/v1/x", api_config_override=_config(), operation_name="Op")


@pytest.mark.parametrize("bad", [float("inf"), float("nan"), 0, -1])
def test_timeout_must_be_finite_and_positive(bad: float):
    with pytest.raises(ConfigurationError):
        _config(timeout=bad)


def test_http_exception_survives_pickling():
    import pickle

    original = HTTPException(
        404,
        "gone",
        method="GET",
        path="/v1/x",
        details={"k": 1},
        grpc_status_code="NOT_FOUND",
    )

    restored = pickle.loads(pickle.dumps(original))

    assert type(restored) is HTTPException
    assert (restored.status_code, restored.message, restored.path) == (
        404,
        "gone",
        "/v1/x",
    )
    assert restored.details == {"k": 1}
    assert str(restored) == str(original)


@pytest.mark.parametrize(
    ("response", "problem"),
    [
        (
            httpx.Response(200, text="<html/>", headers={"content-type": "text/html"}),
            "a non-JSON body (content-type=text/html)",
        ),
        (
            httpx.Response(
                200, content=b"null", headers={"content-type": "application/json"}
            ),
            "a null body",
        ),
        (httpx.Response(200, json=[{"site": {}}]), "data that does not match"),
    ],
)
def test_a_success_status_with_an_unusable_body_raises_502(
    monkeypatch: pytest.MonkeyPatch, response: httpx.Response, problem: str
):
    from kentik_api import KentikAPI

    monkeypatch.setattr(httpx.Client, "request", lambda self, *a, **k: response)
    client = KentikAPI(email="dev@example.com", api_token="token", env_file=None)
    try:
        with pytest.raises(HTTPException) as exc:
            client.site.get(id="1")
    finally:
        client.close()

    assert type(exc.value) is HTTPException
    assert exc.value.status_code == 502
    assert f"GetSite returned {problem}" in str(exc.value)
    assert "status code" not in str(exc.value)


def test_a_response_without_quota_headers_records_no_quota(
    monkeypatch: pytest.MonkeyPatch,
):
    responses = iter(
        [httpx.Response(200, json={"ok": True}), httpx.Response(429, json={})]
    )
    monkeypatch.setattr(httpx.Client, "request", lambda self, *a, **k: next(responses))
    from kentik_api.core.rate_limit import rate_limit_of

    cfg = _config()
    body = request_json("POST", "/query/topXdata", api_config_override=cfg)
    with pytest.raises(HTTPException) as exc:
        request_json("POST", "/query/topXdata", api_config_override=cfg)

    assert rate_limit_of(body) is None
    assert exc.value.status_code == 429
    assert exc.value.rate_limit is None
    assert cfg.rate_limits == {}


def test_a_v5_error_body_gives_the_message_and_keeps_the_error_id(
    monkeypatch: pytest.MonkeyPatch,
):
    body = {"error": "The device_name is required", "errorxid": "mvbc0s95qc"}
    monkeypatch.setattr(
        httpx.Client, "request", lambda self, *a, **k: httpx.Response(400, json=body)
    )

    with pytest.raises(HTTPException) as exc:
        request_json("POST", "/query/topXdata", api_config_override=_config())

    assert exc.value.message.endswith(": The device_name is required")
    assert exc.value.details["response_json"]["errorxid"] == "mvbc0s95qc"


def test_a_generated_v5_error_keeps_the_v5_error_text(monkeypatch: pytest.MonkeyPatch):
    from kentik_api.gen.v5.error import TopXDataBadRequestError, TopXDataError

    body = {"error": "The device_name is required", "errorxid": "mvbc0s95qc"}
    monkeypatch.setattr(
        httpx.Client, "request", lambda self, *a, **k: httpx.Response(400, json=body)
    )

    with pytest.raises(TopXDataBadRequestError) as exc:
        request_json(
            "POST",
            "/query/topXdata",
            api_config_override=_config(),
            error_cls=TopXDataError,
        )

    assert exc.value.message.endswith(": The device_name is required")
    assert exc.value.details["response_json"]["errorxid"] == "mvbc0s95qc"
