"""APIConfig timeout derivation and validation (FR-002, FR-015, FR-016, FR-017)."""

import math
from typing import Any

import httpx
import pytest

from kentik_api.core.api_config import APIConfig
from kentik_api.errors import ConfigurationError, HTTPException, KentikError


def test_defaults_keep_the_previous_sixty_seconds_on_both_transports():
    config = APIConfig()

    assert config.timeout == 60.0
    assert config.rest_timeout == httpx.Timeout(60.0)
    assert config.grpc_deadline == 60.0


def test_omitted_refinements_derive_from_the_shared_timeout():
    config = APIConfig(timeout=5.0)

    assert config.rest_timeout == httpx.Timeout(5.0)
    assert config.grpc_deadline == 5.0


def test_scalar_rest_timeout_sets_all_four_phases():
    config = APIConfig(rest_timeout=7.0)

    assert (config.rest_timeout.connect, config.rest_timeout.read) == (7.0, 7.0)
    assert (config.rest_timeout.write, config.rest_timeout.pool) == (7.0, 7.0)


def test_phase_bounds_are_honoured_independently():
    phases = httpx.Timeout(connect=2.0, read=300.0, write=10.0, pool=5.0)

    config = APIConfig(rest_timeout=phases)

    assert config.rest_timeout == phases
    assert config.rest_timeout is not phases
    assert config.grpc_deadline == 60.0


def test_grpc_deadline_is_independent_of_rest_timeout():
    config = APIConfig(timeout=30.0, rest_timeout=2.0, grpc_deadline=120.0)

    assert config.rest_timeout == httpx.Timeout(2.0)
    assert config.grpc_deadline == 120.0


@pytest.mark.parametrize("phase", ["connect", "read", "write", "pool"])
@pytest.mark.parametrize(
    "value", [11.0, None, 0.0, -1.0, math.nan, math.inf, -math.inf]
)
@pytest.mark.parametrize(
    "target", ["input", "base", "sibling", "child", "grandchild", "refined"]
)
def test_external_timeout_mutation_cannot_change_accepted_settings(
    phase, value, target
):
    supplied = httpx.Timeout(connect=2.0, read=3.0, write=5.0, pool=7.0)
    base = APIConfig(rest_timeout=supplied)
    child = base.with_timeout(grpc_deadline=8.0)
    configs = {
        "base": base,
        "sibling": APIConfig(rest_timeout=supplied),
        "child": child,
        "grandchild": child.with_timeout(grpc_deadline=9.0),
        "refined": base.with_timeout(rest_timeout=supplied),
    }
    exposed = supplied if target == "input" else configs[target].rest_timeout

    setattr(exposed, phase, value)

    for config in configs.values():
        assert config.rest_timeout == httpx.Timeout(
            connect=2.0, read=3.0, write=5.0, pool=7.0
        )
        assert config.rest_deadline is None
    assert base.grpc_deadline == 60.0
    assert child.grpc_deadline == 8.0


@pytest.mark.parametrize("bad", [0, -1.0, math.nan])
@pytest.mark.parametrize(
    ("kwargs_for", "field"),
    [
        (lambda v: {"timeout": v}, "timeout"),
        (lambda v: {"grpc_deadline": v}, "grpc_deadline"),
        (lambda v: {"rest_timeout": v}, "rest_timeout.connect"),
        (
            lambda v: {"rest_timeout": httpx.Timeout(5.0, connect=v)},
            "rest_timeout.connect",
        ),
        (lambda v: {"rest_timeout": httpx.Timeout(5.0, read=v)}, "rest_timeout.read"),
        (lambda v: {"rest_timeout": httpx.Timeout(5.0, write=v)}, "rest_timeout.write"),
        (lambda v: {"rest_timeout": httpx.Timeout(5.0, pool=v)}, "rest_timeout.pool"),
    ],
    ids=[
        "timeout",
        "grpc_deadline",
        "rest_timeout-scalar",
        "rest_timeout-connect",
        "rest_timeout-read",
        "rest_timeout-write",
        "rest_timeout-pool",
    ],
)
def test_non_positive_bounds_are_rejected_naming_field_and_value(
    kwargs_for, field, bad
):
    with pytest.raises(ConfigurationError) as exc_info:
        APIConfig(**kwargs_for(bad))

    assert field in str(exc_info.value)
    assert repr(bad) in str(exc_info.value)


def test_unbounded_rest_phase_is_rejected():
    with pytest.raises(ConfigurationError, match="rest_timeout.read"):
        APIConfig(rest_timeout=httpx.Timeout(5.0, read=None))


def test_every_sdk_error_carries_a_rate_limit_slot():
    assert KentikError("x").rate_limit is None
    assert ConfigurationError("x").rate_limit is None


def test_http_exception_keeps_the_verbatim_grpc_code():
    exc = HTTPException(404, "not found", grpc_status_code="NOT_FOUND")

    assert exc.grpc_status_code == "NOT_FOUND"
    assert HTTPException(404, "not found").grpc_status_code is None


import ast  # noqa: E402
import inspect  # noqa: E402
from pathlib import Path  # noqa: E402

_BASE: dict[str, Any] = {
    "base_path": "https://grpc.api.kentik.com",
    "auth_email": "dev@example.com",
    "auth_token": "token",
    "timeout": 60.0,
}


def test_with_timeout_scalar_resets_both_transports():
    slow = APIConfig(**_BASE).with_timeout(300)

    assert slow.rest_timeout == httpx.Timeout(300)
    assert slow.grpc_deadline == 300


def test_with_timeout_refines_one_transport_and_keeps_the_rest():
    base = APIConfig(**_BASE, grpc_deadline=90.0)
    phases = httpx.Timeout(connect=2.0, read=300.0, write=10.0, pool=5.0)

    slow = base.with_timeout(rest_timeout=phases)

    assert slow.rest_timeout == phases
    assert slow.rest_timeout is not phases
    assert slow.grpc_deadline == 90.0
    assert base.with_timeout(grpc_deadline=5).rest_timeout == base.rest_timeout


def test_with_timeout_leaves_the_original_untouched():
    base = APIConfig(**_BASE)

    base.with_timeout(300)

    assert base.rest_timeout == httpx.Timeout(60.0)
    assert base.grpc_deadline == 60.0


def test_with_timeout_validates_like_the_constructor():
    with pytest.raises(ConfigurationError, match="grpc_deadline"):
        APIConfig(**_BASE).with_timeout(grpc_deadline=0)
    with pytest.raises(ConfigurationError, match="at least one"):
        APIConfig(**_BASE).with_timeout()


def test_with_timeout_copies_the_security_fields_and_cannot_change_them():
    base = APIConfig(**_BASE)
    slow = base.with_timeout(300)

    for field in ("base_path", "auth_email", "auth_token", "verify"):
        assert getattr(slow, field) == getattr(base, field)
    params = set(inspect.signature(APIConfig.with_timeout).parameters) - {"self"}
    assert params == {"timeout", "rest_timeout", "grpc_deadline"}
    with pytest.raises(TypeError):
        base.with_timeout(300, base_path="https://attacker.example")  # ty: ignore[unknown-argument]  # pyright: ignore[reportCallIssue]


def test_no_test_fixture_disables_tls_verification():
    tests_root = Path(__file__).resolve().parents[1]
    offenders = []
    for path in tests_root.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.keyword)
                and node.arg == "verify"
                and isinstance(node.value, ast.Constant)
                and node.value.value is False
            ):
                offenders.append(f"{path.relative_to(tests_root)}:{node.value.lineno}")
    assert offenders == []


def test_override_replaces_the_client_config_rather_than_merging(monkeypatch):
    """An override naming only a new host must not inherit the client's credentials."""
    from kentik_api.core.rest_runtime import request_json

    sent = []
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, *a, **k: sent.append(k) or httpx.Response(200, json={}),
    )
    redirected = APIConfig(base_path="https://elsewhere.example")

    with pytest.raises(ConfigurationError, match="no credentials"):
        request_json("GET", "/v1/test", api_config_override=redirected)

    assert sent == []


def test_omitting_the_override_uses_the_client_config_unchanged(monkeypatch):
    from kentik_api.core.rest_runtime import request_json

    sent = []
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, *a, **k: (
            sent.append((str(self.base_url), k)) or httpx.Response(200, json={})
        ),
    )
    config = APIConfig(**_BASE)

    request_json("GET", "/v1/test", api_config_override=config)

    base_url, kwargs = sent[0]
    assert base_url == "https://grpc.api.kentik.com"
    assert kwargs["timeout"] == config.rest_timeout
    assert kwargs["headers"]["X-CH-Auth-Email"] == "dev@example.com"


def test_proxy_routing_uses_no_private_httpx_import():
    import inspect

    from kentik_api.core import api_config

    assert "httpx._" not in inspect.getsource(api_config)


@pytest.mark.parametrize(
    "field",
    [
        "base_path",
        "auth_email",
        "auth_token",
        "verify",
        "timeout",
        "rest_timeout",
        "rest_deadline",
        "grpc_deadline",
    ],
)
def test_settings_are_read_only(field):
    config = APIConfig(**_BASE)

    with pytest.raises(AttributeError, match="read-only"):
        setattr(config, field, getattr(config, field))


def test_credentials_are_read_only():
    from kentik_api.auth.credentials import KentikCredentials

    credentials = KentikCredentials("dev@example.com", "token")

    for field in ("email", "api_token"):
        with pytest.raises(AttributeError):
            setattr(credentials, field, "other")


def test_environment_proxies_follow_the_proxy_variables(monkeypatch):
    from kentik_api.core.api_config import _environment_proxies

    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"):
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)
    monkeypatch.setenv("HTTPS_PROXY", "proxy.internal:3128")
    monkeypatch.setenv("NO_PROXY", "api.example.com, localhost,10.0.0.1")

    assert _environment_proxies() == {
        "https://": "http://proxy.internal:3128",
        "all://*api.example.com": None,
        "all://localhost": None,
        "all://10.0.0.1": None,
    }

    monkeypatch.setenv("NO_PROXY", "*")
    assert _environment_proxies() == {}
