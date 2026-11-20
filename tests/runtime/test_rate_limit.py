# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Quota parsing and capture on both transports (FR-029, FR-030, FR-031)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import grpc
import httpx
import pytest
from pydantic import BaseModel

from kentik_api.core import grpc_runtime
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import call_grpc
from kentik_api.core.rate_limit import RateLimit, rate_limit_of_rpc
from kentik_api.core.rest_runtime import parse_response_model, request_json
from kentik_api.errors import AuthenticationError, HTTPException, TransportError
from kentik_api.transports.grpc_client import _DefaultDeadlineInterceptor

MEASURED = {
    "x-ratelimit-limit": "60, 60;w=60",
    "x-ratelimit-remaining": "59",
    "x-ratelimit-reset": "40",
}


def test_parses_the_measured_kentik_form():
    assert RateLimit.from_headers(MEASURED) == RateLimit(
        limit=60, remaining=59, reset_seconds=40, window_seconds=60, raw="60, 60;w=60"
    )


def test_accepts_the_window_spelling_and_any_header_case():
    rl = RateLimit.from_headers({"X-RateLimit-Limit": "100;window=60"})
    assert rl is not None

    assert (rl.limit, rl.window_seconds) == (100, 60)


def test_multiple_windows_model_the_binding_one_and_keep_the_rest_raw():
    raw = "100, 1000;w=3600, 100;w=60"

    rl = RateLimit.from_headers({"x-ratelimit-limit": raw})
    assert rl is not None

    assert (rl.limit, rl.window_seconds, rl.raw) == (100, 60, raw)


@pytest.mark.parametrize(
    "headers",
    [
        None,
        {},
        {"content-type": "application/json"},
        {"x-ratelimit-limit": "lots", "x-ratelimit-remaining": "?"},
    ],
    ids=["none", "empty", "absent", "malformed"],
)
def test_absent_or_malformed_headers_yield_none(headers):
    assert RateLimit.from_headers(headers) is None


def test_partially_malformed_headers_keep_what_parsed():
    rl = RateLimit.from_headers(
        {"x-ratelimit-limit": "garbage", "x-ratelimit-remaining": "7"}
    )
    assert rl is not None

    assert (rl.limit, rl.remaining, rl.window_seconds) == (None, 7, None)


def test_parser_never_raises_on_hostile_input():
    class Exploding(dict):
        def items(self):
            raise RuntimeError("boom")

    assert RateLimit.from_headers(Exploding(a="b")) is None
    assert RateLimit.from_metadata([("x-ratelimit-limit",)]) is None  # ty: ignore[invalid-argument-type]  # pyright: ignore[reportArgumentType]


def test_grpc_metadata_parses_like_headers_including_bytes_values():
    metadata = [("x-ratelimit-limit", b"60, 60;w=60"), ("x-ratelimit-remaining", "3")]

    rl = RateLimit.from_metadata(metadata)
    assert rl is not None

    assert (rl.limit, rl.remaining, rl.window_seconds) == (60, 3, 60)
    assert RateLimit.from_metadata(None) is None


def test_rate_limit_of_rpc_tolerates_objects_without_metadata():
    assert rate_limit_of_rpc(object()) is None


def _rest_config() -> APIConfig:
    return APIConfig(
        base_path="https://api.example.com",
        auth_email="dev@example.com",
        auth_token="t",
    )


def _rest(
    monkeypatch, response: httpx.Response, config: APIConfig, path="/device/v1/device"
):
    monkeypatch.setattr(httpx.Client, "request", lambda self, *a, **k: response)
    return request_json("GET", path, api_config_override=config, operation_name="Op")


def test_rest_success_records_quota_per_path(monkeypatch):
    config = _rest_config()

    _rest(monkeypatch, httpx.Response(200, json={}, headers=MEASURED), config, "/a")
    _rest(
        monkeypatch,
        httpx.Response(
            200, json={}, headers={**MEASURED, "x-ratelimit-remaining": "12"}
        ),
        config,
        "/b",
    )

    assert config.rate_limits["GET /a"].remaining == 59
    assert config.rate_limits["GET /b"].remaining == 12


def test_rest_quota_has_one_key_per_endpoint_not_per_id(monkeypatch):
    config = _rest_config()
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, *a, **k: httpx.Response(200, json={}, headers=MEASURED),
    )

    for method, device_id in (("GET", "1"), ("GET", "2"), ("DELETE", "1")):
        request_json(
            method,
            f"/device/v1/device/{device_id}",
            path_template="/device/v1/device/{device.id}",
            api_config_override=config,
        )

    assert set(config.rate_limits) == {
        "GET /device/v1/device/{device.id}",
        "DELETE /device/v1/device/{device.id}",
    }


@pytest.mark.parametrize(
    ("status", "expected"),
    [(401, AuthenticationError), (429, HTTPException), (500, HTTPException)],
)
def test_rest_errors_carry_the_quota_of_the_failing_call(monkeypatch, status, expected):
    config = _rest_config()
    headers = {**MEASURED, "x-ratelimit-remaining": "0"}

    with pytest.raises(expected) as exc_info:
        _rest(
            monkeypatch,
            httpx.Response(status, json={"message": "no"}, headers=headers),
            config,
        )

    rate_limit = exc_info.value.rate_limit
    assert rate_limit is not None
    assert rate_limit.remaining == 0


def test_rest_response_without_quota_headers_leaves_the_error_slot_empty(monkeypatch):
    with pytest.raises(HTTPException) as exc_info:
        _rest(
            monkeypatch,
            httpx.Response(404, json={}),
            _rest_config(),
        )

    assert exc_info.value.rate_limit is None


class _Strict(BaseModel):
    id: int


def test_a_rest_body_that_fails_its_model_keeps_the_quota(monkeypatch):
    body = _rest(
        monkeypatch,
        httpx.Response(200, json={"id": "x"}, headers=MEASURED),
        _rest_config(),
    )

    with pytest.raises(HTTPException) as exc_info:
        parse_response_model(
            _Strict, body, operation_name="Op", method="GET", path="/a"
        )

    assert exc_info.value.status_code == 502
    assert exc_info.value.rate_limit == RateLimit.from_headers(MEASURED)


def test_a_grpc_response_that_fails_its_model_keeps_the_quota(monkeypatch):
    monkeypatch.setattr(grpc_runtime, "grpc_response_body", lambda _r: {"id": "x"})
    quota = RateLimit.from_headers(MEASURED)

    with pytest.raises(HTTPException) as exc_info:
        grpc_runtime.parse_grpc_response(
            _Strict, object(), quota, stub_method=object(), operation_name="Op"
        )

    assert exc_info.value.status_code == 502
    assert exc_info.value.rate_limit == quota


def test_transport_failure_has_no_quota_because_no_response_arrived(monkeypatch):
    def _fail(self, *a, **k):
        raise httpx.ConnectError("refused")

    monkeypatch.setattr(httpx.Client, "request", _fail)

    with pytest.raises(TransportError) as exc_info:
        request_json("GET", "/a", api_config_override=_rest_config())

    assert exc_info.value.rate_limit is None


def test_grpc_error_carries_quota_from_initial_metadata(rpc_error):
    error = rpc_error(grpc.StatusCode.RESOURCE_EXHAUSTED, "slow down")
    error.initial_metadata = lambda: [
        ("x-ratelimit-limit", "60, 60;w=60"),
        ("x-ratelimit-remaining", "0"),
    ]

    def _stub(_request):
        raise error

    with pytest.raises(HTTPException) as exc_info:
        call_grpc(_stub, object())

    rate_limit = exc_info.value.rate_limit
    assert rate_limit is not None
    assert rate_limit.remaining == 0


def test_grpc_error_reads_quota_from_trailers_only_responses(rpc_error):
    # A gRPC error with no body is "Trailers-Only": every header arrives as
    # trailing metadata, and the initial metadata is empty.
    error = rpc_error(grpc.StatusCode.RESOURCE_EXHAUSTED, "slow down")
    error.initial_metadata = lambda: ()
    error.trailing_metadata = lambda: [("x-ratelimit-remaining", "0")]

    rate_limit = rate_limit_of_rpc(error)

    assert rate_limit is not None
    assert rate_limit.remaining == 0


def _details(method: str | bytes = "/svc.Service/Op") -> Any:
    return SimpleNamespace(
        method=method,
        timeout=None,
        metadata=None,
        credentials=None,
        wait_for_ready=None,
        compression=None,
    )


def test_interceptor_records_quota_per_method_on_success():
    config = APIConfig()
    outcome: Any = SimpleNamespace(
        exception=lambda: None,
        initial_metadata=lambda: [("x-ratelimit-remaining", "41")],
    )

    result = _DefaultDeadlineInterceptor(config, lambda: False).intercept_unary_unary(
        lambda details, request: outcome, _details(), object()
    )

    assert result is outcome
    assert config.rate_limits["/svc.Service/Op"].remaining == 41


def test_interceptor_records_quota_from_a_failed_calls_error(rpc_error):
    config = APIConfig()
    error = rpc_error(grpc.StatusCode.RESOURCE_EXHAUSTED)
    error.initial_metadata = lambda: [("x-ratelimit-remaining", "0")]
    outcome: Any = SimpleNamespace(
        exception=lambda: error, initial_metadata=lambda: None
    )

    _DefaultDeadlineInterceptor(config, lambda: False).intercept_unary_unary(
        lambda details, request: outcome, _details(b"/svc.Service/Op"), object()
    )

    assert config.rate_limits["/svc.Service/Op"].remaining == 0


def test_interceptor_ignores_calls_without_quota():
    config = APIConfig()
    outcome: Any = SimpleNamespace(
        exception=lambda: None, initial_metadata=lambda: None
    )

    _DefaultDeadlineInterceptor(config, lambda: False).intercept_unary_unary(
        lambda details, request: outcome, _details(), object()
    )

    assert config.rate_limits == {}


from kentik_api.core.rate_limit import attach_rate_limit, rate_limit_of  # noqa: E402
from kentik_api.gen.device.models import ListDevicesResponse  # noqa: E402

QUOTA = RateLimit(limit=60, remaining=41, reset_seconds=12, window_seconds=60, raw="60")


def test_quota_attached_to_a_generated_model_is_readable():
    model = attach_rate_limit(ListDevicesResponse(), QUOTA)

    assert rate_limit_of(model) is QUOTA


def test_attachment_leaves_model_dump_and_equality_unchanged():
    plain = ListDevicesResponse()
    tagged = attach_rate_limit(ListDevicesResponse(), QUOTA)

    assert tagged.model_dump() == plain.model_dump()
    assert (
        tagged.model_dump(by_alias=True).keys()
        == plain.model_dump(by_alias=True).keys()
    )
    assert tagged == plain


def test_results_that_cannot_carry_quota_come_back_unchanged():
    assert attach_rate_limit(None, QUOTA) is None
    items = [1, 2]
    assert attach_rate_limit(items, QUOTA) is items
    assert rate_limit_of(items) is None
    assert rate_limit_of(ListDevicesResponse()) is None


def test_rest_body_carries_the_quota_to_the_model_built_from_it(monkeypatch):
    body = _rest(
        monkeypatch,
        httpx.Response(200, json={"devices": []}, headers=MEASURED),
        _rest_config(),
    )

    assert body == {"devices": []}
    model = attach_rate_limit(ListDevicesResponse(**body), rate_limit_of(body))
    rate_limit = rate_limit_of(model)
    assert rate_limit is not None
    assert rate_limit.remaining == 59
