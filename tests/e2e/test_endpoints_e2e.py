# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""End-to-end coverage against the real Kentik API.

Every other suite under tests/generated/ proves the SDK is internally
self-consistent using mocked HTTP responses. This module is the one place
that calls the real API, so it can catch the one thing mocks structurally
cannot: the real API's behavior drifting from what the schema (and therefore
the generated code) assumes.

Scope, by design (see AGENTS.md's end-to-end testing requirement):
  - Only GET (read-only, non-mutating) operations are auto-covered and
    actually called here. Discovered the same way as every other generated
    suite (via tests/_discovery.py), so new read endpoints get e2e
    coverage automatically as the schema grows.
  - Create/Update/Delete operations are intentionally NOT auto-covered
    (see test_mutating_endpoint_excluded_from_e2e below): they are hard to
    reverse against a real account and need a purpose-built, cleaned-up
    fixture per operation, added deliberately rather than as a side effect
    of this file existing.
  - A read call passes if it returns a correctly-typed response OR raises a
    generated 4xx HTTPException. Both prove the real request/response/
    error path still matches the schema. A 5xx is a server failure, and
    any other exception is an SDK failure. We don't control what data
    exists in the real account, so a 4xx for a sample ID is expected.
    A 404 on a path with no parameters fails: there is no ID to miss, so
    the server does not serve that route.

Opt-in only: excluded from `uv run poe test`/`uv run poe all` by the `e2e` pytest marker
(see pyproject.toml's addopts) and only actually run via `uv run poe test-e2e` or
`pytest -m e2e --run-live-e2e`. The `real_client` fixture (tests/e2e/conftest.py) skips the
whole module if no real credentials are configured.
"""

from __future__ import annotations

import inspect

import pytest
from _discovery import (
    EndpointCase,
    build_required_kwargs,
    case_label,
    discover_endpoint_cases,
    service_attr,
)
from pydantic import BaseModel
from upstream_bugs import server_error

from kentik_api.errors import HTTPException, KentikError

pytestmark = pytest.mark.e2e

_ALL_ENDPOINT_CASES = discover_endpoint_cases()
READ_CASES = [c for c in _ALL_ENDPOINT_CASES if c.method == "get"]
MUTATING_CASES = [c for c in _ALL_ENDPOINT_CASES if c.method != "get"]


@pytest.mark.parametrize(
    "case",
    READ_CASES,
    ids=[f"{c.wrapper.wrapper_class}.{c.wrapper.method_name}" for c in READ_CASES],
)
def test_read_endpoint_against_real_api(
    case: EndpointCase, real_client, request: pytest.FixtureRequest
):
    if reason := server_error(request.node.callspec.id, "rest"):
        request.applymarker(
            pytest.mark.xfail(raises=HTTPException, strict=True, reason=reason)
        )
    service_client = getattr(real_client, service_attr(case))
    method = getattr(service_client, case.wrapper.method_name)
    # Placeholder filters are not valid input, and the API answers some with a
    # 500, so live reads send only what the call requires. Mocked suites cover
    # every option.
    kwargs = build_required_kwargs(method)

    assert real_client.api_config.base_path != "https://api.example.com"
    assert "api_config_override" not in kwargs

    label = f"{case_label(case.wrapper)} ({case.operation_name})"
    print(f'E2E: calling "{label}" against the real API. START')
    try:
        result = method(**kwargs)
    except HTTPException as exc:
        if exc.status_code >= 500:
            print(f'E2E: "{label}" failed on the server. RESULT=FAIL')
            raise
        if exc.status_code == 404 and "{" not in case.path:
            # No ID to miss, so a 404 means the server does not serve this route.
            print(f'E2E: "{label}" has no route on the server. RESULT=FAIL')
            raise
        print(
            f'E2E: "{label}" raised {type(exc).__name__} '
            f"(status={getattr(exc, 'status_code', 'n/a')}). A generated "
            "HTTP error response is a valid outcome. RESULT=PASS"
        )
        return
    except KentikError as exc:
        pytest.fail(
            "Expected a typed response or HTTPException from live REST e2e call, "
            f"got unexpected KentikError subtype {type(exc).__name__}: {exc}"
        )
    except Exception:
        print(f'E2E: "{label}" raised an UNEXPECTED exception. RESULT=FAIL')
        raise

    return_annotation = inspect.signature(method).return_annotation
    if isinstance(return_annotation, type) and issubclass(return_annotation, BaseModel):
        assert isinstance(result, return_annotation)

    print(f'E2E: "{label}" returned a typed response. RESULT=PASS')


@pytest.mark.skip(
    reason=(
        "Mutating (non-GET) operations are intentionally excluded from "
        "automatic e2e coverage. See AGENTS.md's end-to-end testing "
        "requirement. Add a dedicated test with real setup/teardown for this "
        "specific operation if you need live coverage here."
    )
)
@pytest.mark.parametrize(
    "case",
    MUTATING_CASES,
    ids=[f"{c.wrapper.wrapper_class}.{c.wrapper.method_name}" for c in MUTATING_CASES],
)
def test_mutating_endpoint_excluded_from_e2e(case: EndpointCase, real_client):
    raise NotImplementedError(
        "Not auto-implemented by design. See the skip reason above."
    )
