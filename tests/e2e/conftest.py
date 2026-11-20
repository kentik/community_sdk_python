# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

from collections.abc import Iterator

import pytest
from ledger import Ledger, sweep

from kentik_api.client import KentikAPI
from kentik_api.errors import ConfigurationError


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-live-e2e",
        action="store_true",
        default=False,
        help=(
            "Run live end-to-end tests against the real Kentik API. "
            "Disabled by default to avoid accidental credential use."
        ),
    )


@pytest.fixture(scope="session")
def real_client(request: pytest.FixtureRequest) -> Iterator[KentikAPI]:
    """A real KentikAPI client backed by whatever credentials are configured.

    Credential loading is delegated entirely to KentikAPI itself (project-root
    .env or KENTIK_EMAIL/KENTIK_API_TOKEN env vars) rather than duplicated
    here. If none are configured, the whole e2e suite skips rather than
    fails, since these tests are opt-in and not everyone running the mocked
    suites has (or should need) a live Kentik account.
    """
    if not request.config.getoption("--run-live-e2e"):
        pytest.skip(
            "Live e2e tests are disabled by default. Re-run with --run-live-e2e "
            "to allow real API calls."
        )

    try:
        client = KentikAPI(protocol="rest")
    except ConfigurationError:
        pytest.skip(
            "No KENTIK_EMAIL/KENTIK_API_TOKEN available. End-to-end tests "
            "require real credentials in a project-root .env and are opt-in "
            "only (see AGENTS.md's end-to-end testing requirement)."
        )
    try:
        yield client
    finally:
        client.close()


@pytest.fixture(scope="session")
def grpc_real_client(request: pytest.FixtureRequest) -> Iterator[KentikAPI]:
    """Same as real_client, but over the gRPC transport (protocol="grpc")."""
    if not request.config.getoption("--run-live-e2e"):
        pytest.skip(
            "Live e2e tests are disabled by default. Re-run with --run-live-e2e "
            "to allow real API calls."
        )

    try:
        client = KentikAPI(protocol="grpc")
    except ConfigurationError:
        pytest.skip(
            "No KENTIK_EMAIL/KENTIK_API_TOKEN available. End-to-end tests "
            "require real credentials in a project-root .env and are opt-in "
            "only (see AGENTS.md's end-to-end testing requirement)."
        )
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def ledger(real_client: KentikAPI) -> Iterator[Ledger]:
    """Records every object a mutating test creates; deletes that test's leftovers after it."""
    ledger = Ledger()
    yield ledger
    leftovers = [e for e in ledger.outstanding() if e.run == ledger.run]
    failures = sweep(real_client, ledger, leftovers)
    if failures:
        pytest.fail(
            "Some e2e test objects were not cleaned up. They stay in "
            f"{ledger.path}; run `uv run poe e2e-cleanup`.\n" + "\n".join(failures)
        )


@pytest.fixture(params=["rest", "grpc"])
def any_client(request: pytest.FixtureRequest) -> KentikAPI:
    """The REST and the gRPC client in turn, so a lifecycle test covers both transports."""
    name = "real_client" if request.param == "rest" else "grpc_real_client"
    return request.getfixturevalue(name)
