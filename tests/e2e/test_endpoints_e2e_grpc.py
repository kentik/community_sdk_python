# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""End-to-end gRPC coverage against the real Kentik API.

Mirrors test_endpoints_e2e.py but drives every discovered read (GET)
operation through protocol="grpc" instead of REST. Endpoint discovery and
the GET-vs-mutating split are shared with the REST suite via
tests/_discovery.py (discover_endpoint_cases()), so both suites classify
the same operations the same way.

gRPC coverage is per-operation, not per-service (see AGENTS.md's "gRPC
transport is fully implemented" section): a wrapper method raises
NotImplementedError when the service's proto companions failed to import,
or when no RPC shares that REST operation's HTTP rule. Neither case is a
bug. Both count as a passing outcome here, same as a correctly-typed
response or a 4xx HTTPException. A 5xx or any other exception fails, as in
the REST suite.

Opt-in only: excluded from `uv run poe test`/`all`/`test-e2e` by the
`e2e_grpc` pytest marker (see pyproject.toml's addopts) and only actually
run via `uv run poe test-e2e-grpc` or `pytest -m e2e_grpc --run-live-e2e`. The
`grpc_real_client` fixture (tests/e2e/conftest.py) skips the whole module
if no real credentials are configured.
"""

from __future__ import annotations

import importlib
import inspect

import pytest
from _discovery import (
    EndpointCase,
    build_required_kwargs,
    case_label,
    discover_endpoint_cases,
    proto_field,
    proto_sample_value,
    service_attr,
)
from pydantic import BaseModel
from upstream_bugs import server_error

from kentik_api.errors import HTTPException, KentikError

pytestmark = pytest.mark.e2e_grpc

_ALL_ENDPOINT_CASES = discover_endpoint_cases()
READ_CASES = [c for c in _ALL_ENDPOINT_CASES if c.method == "get"]
MUTATING_CASES = [c for c in _ALL_ENDPOINT_CASES if c.method != "get"]


@pytest.mark.parametrize(
    "case",
    READ_CASES,
    ids=[f"{c.wrapper.wrapper_class}.{c.wrapper.method_name}" for c in READ_CASES],
)
def test_read_endpoint_against_real_api_grpc(
    case: EndpointCase,
    grpc_real_client,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
):
    if reason := server_error(request.node.callspec.id, "grpc"):
        request.applymarker(
            pytest.mark.xfail(raises=HTTPException, strict=True, reason=reason)
        )
    service_client = getattr(grpc_real_client, service_attr(case))
    method = getattr(service_client, case.wrapper.method_name)
    kwargs = build_required_kwargs(method)
    _send_samples_the_proto_accepts(monkeypatch, case)

    label = f"{case_label(case.wrapper)} ({case.operation_name})"
    print(f'E2E-gRPC: calling "{label}" against the real API. START')
    try:
        result = method(**kwargs)
    except NotImplementedError as exc:
        print(
            f'E2E-gRPC: "{label}" has no gRPC translation yet ({exc}). This is '
            "expected, not a bug. RESULT=PASS"
        )
        return
    except HTTPException as exc:
        if exc.status_code >= 500:
            print(f'E2E-gRPC: "{label}" failed on the server. RESULT=FAIL')
            raise
        print(
            f'E2E-gRPC: "{label}" raised {type(exc).__name__} '
            f"(status={exc.status_code}). A generated HTTP error response is "
            "a valid outcome. RESULT=PASS"
        )
        return
    except KentikError as exc:
        pytest.fail(
            "Expected a typed response or HTTPException from live gRPC e2e call, "
            f"got unexpected KentikError subtype {type(exc).__name__}: {exc}"
        )
    except Exception:
        print(f'E2E-gRPC: "{label}" raised an UNEXPECTED exception. RESULT=FAIL')
        raise

    return_annotation = inspect.signature(method).return_annotation
    if isinstance(return_annotation, type) and issubclass(return_annotation, BaseModel):
        assert isinstance(result, return_annotation)

    print(f'E2E-gRPC: "{label}" returned a typed response. RESULT=PASS')


def _send_samples_the_proto_accepts(monkeypatch: pytest.MonkeyPatch, case) -> None:
    module = importlib.import_module(case.wrapper.module_path)
    real_build = getattr(module, "build_grpc_request", None)
    if real_build is None:
        return

    def _build(message_cls, body, fields):
        descriptor = message_cls.DESCRIPTOR
        return real_build(
            message_cls,
            body,
            {
                path: None
                if value is None
                else proto_sample_value(proto_field(descriptor, path), value)
                for path, value in fields.items()
            },
        )

    monkeypatch.setattr(module, "build_grpc_request", _build)


@pytest.mark.skip(
    reason=(
        "Mutating (non-GET) operations are intentionally excluded from "
        "automatic e2e coverage, gRPC included. See AGENTS.md's "
        "end-to-end testing requirement. Add a dedicated test with real "
        "setup/teardown for this specific operation if you need live gRPC "
        "coverage here."
    )
)
@pytest.mark.parametrize(
    "case",
    MUTATING_CASES,
    ids=[f"{c.wrapper.wrapper_class}.{c.wrapper.method_name}" for c in MUTATING_CASES],
)
def test_mutating_endpoint_excluded_from_e2e_grpc(case: EndpointCase, grpc_real_client):
    raise NotImplementedError(
        "Not auto-implemented by design. See the skip reason above."
    )
