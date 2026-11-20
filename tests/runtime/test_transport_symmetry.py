# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The same failure raises the same SDK exception on both transports (FR-040, SC-002).

Each case drives one failure through both shared chokepoints, `request_json()`
and `call_grpc()`, so a caller's `except` clauses survive flipping `protocol`.
"""

from __future__ import annotations

import grpc
import httpx
import pytest

from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import call_grpc
from kentik_api.core.rest_runtime import request_json
from kentik_api.errors import (
    AuthenticationError,
    HTTPException,
    KentikError,
    TransportError,
)

_REQUEST = httpx.Request("GET", "https://api.example.com/device/v202504beta2/device")

CASES = {
    "auth rejected": (
        httpx.Response(
            401, json={"code": 16, "message": "bad token"}, request=_REQUEST
        ),
        grpc.StatusCode.UNAUTHENTICATED,
        AuthenticationError,
    ),
    "client-side timeout": (
        httpx.ReadTimeout("timed out", request=_REQUEST),
        grpc.StatusCode.DEADLINE_EXCEEDED,
        TransportError,
    ),
    "unreachable host": (
        httpx.ConnectError("connection refused", request=_REQUEST),
        grpc.StatusCode.UNAVAILABLE,
        TransportError,
    ),
}


def _rest_call(
    monkeypatch: pytest.MonkeyPatch, outcome: httpx.Response | Exception
) -> None:
    def _fake_request(self, *args, **kwargs):
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    monkeypatch.setattr(httpx.Client, "request", _fake_request)
    request_json(
        "GET",
        "/device/v202504beta2/device",
        api_config_override=APIConfig(
            base_path="https://api.example.com",
            auth_email="dev@example.com",
            auth_token="t",
        ),
        operation_name="ListDevices",
    )


def _grpc_call(rpc_error, code: grpc.StatusCode) -> None:
    def _stub(_request):
        raise rpc_error(code, "simulated")

    call_grpc(_stub, object())


@pytest.mark.parametrize("failure", CASES, ids=str)
def test_same_failure_raises_same_type_on_both_transports(
    monkeypatch, rpc_error, failure
):
    rest_outcome, grpc_code, expected = CASES[failure]

    with pytest.raises(KentikError) as rest_exc:
        _rest_call(monkeypatch, rest_outcome)
    with pytest.raises(KentikError) as grpc_exc:
        _grpc_call(rpc_error, grpc_code)

    assert type(rest_exc.value) is expected
    assert type(grpc_exc.value) is expected


@pytest.mark.parametrize(
    ("failure", "may_have_reached_server"),
    [
        (httpx.ConnectError("refused", request=_REQUEST), False),
        (httpx.ConnectTimeout("timed out", request=_REQUEST), False),
        (httpx.PoolTimeout("pool timed out", request=_REQUEST), False),
        (httpx.ReadTimeout("timed out", request=_REQUEST), True),
        (httpx.WriteTimeout("timed out", request=_REQUEST), True),
    ],
)
def test_rest_transport_error_reports_server_reachability(
    monkeypatch, failure, may_have_reached_server
):
    with pytest.raises(TransportError) as exc_info:
        _rest_call(monkeypatch, failure)

    assert exc_info.value.may_have_reached_server is may_have_reached_server


@pytest.mark.parametrize(
    "grpc_code",
    [
        grpc.StatusCode.CANCELLED,
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.UNAVAILABLE,
    ],
)
def test_grpc_transport_error_conservatively_reports_server_reachability(
    rpc_error, grpc_code
):
    with pytest.raises(TransportError) as exc_info:
        _grpc_call(rpc_error, grpc_code)

    assert exc_info.value.may_have_reached_server is True


def test_api_fault_reaches_the_same_except_branch_on_both_transports(
    monkeypatch, rpc_error
):
    fault = httpx.Response(
        404, json={"code": 5, "message": "no such device"}, request=_REQUEST
    )

    with pytest.raises(HTTPException) as rest_exc:
        _rest_call(monkeypatch, fault)
    with pytest.raises(HTTPException) as grpc_exc:
        _grpc_call(rpc_error, grpc.StatusCode.NOT_FOUND)

    assert rest_exc.value.status_code == grpc_exc.value.status_code == 404


def test_rpc_status_details_are_the_same_on_both_transports(monkeypatch, rpc_error):
    from google.protobuf.json_format import ParseDict
    from google.rpc import status_pb2

    from kentik_api.gen.device.error import ListError

    status = {
        "code": 3,
        "message": "bad",
        "details": [
            {
                "@type": "type.googleapis.com/google.rpc.BadRequest",
                "fieldViolations": [{"field": "limit", "description": "too big"}],
            }
        ],
    }
    fault = httpx.Response(400, json=status, request=_REQUEST)
    monkeypatch.setattr(httpx.Client, "request", lambda self, *a, **k: fault)
    error = rpc_error(grpc.StatusCode.INVALID_ARGUMENT, "bad")
    error.trailing_metadata = lambda: [
        (
            "grpc-status-details-bin",
            ParseDict(status, status_pb2.Status()).SerializeToString(),
        )
    ]

    with pytest.raises(HTTPException) as rest_exc:
        request_json(
            "GET",
            "/device/v202504beta2/device",
            api_config_override=APIConfig(
                base_path="https://api.example.com",
                auth_email="dev@example.com",
                auth_token="t",
            ),
            error_cls=ListError,
        )

    def _stub(_request):
        raise error

    with pytest.raises(HTTPException) as grpc_exc:
        call_grpc(_stub, object(), error_cls=ListError)

    assert rest_exc.value.details["rpc_status"] == status
    assert grpc_exc.value.details["rpc_status"] == status


def test_a_non_region_value_is_a_configuration_error():
    from kentik_api import KentikAPI
    from kentik_api.errors import ConfigurationError

    with pytest.raises(ConfigurationError):
        KentikAPI("a@b.c", "token", region=None, env_file=None)  # ty: ignore[invalid-argument-type]  # pyright: ignore[reportArgumentType]
