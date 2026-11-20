# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The V5 REST transport that every KentikAPI client has (spec 005, FR-006a)."""

from __future__ import annotations

import httpx
import pytest
import respx

from kentik_api import KentikAPI
from kentik_api.core.rest_runtime import request_json
from kentik_api.errors import ConfigurationError
from kentik_api.transports.rest_client import RestTransport

_REAL_CLIENT = httpx.Client


def _client(**kwargs) -> KentikAPI:
    return KentikAPI("dev@example.com", "token", env_file=None, **kwargs)


@pytest.mark.parametrize(
    ("region", "protocol", "url"),
    [
        ("us", "rest", "https://api.kentik.com/api/v5"),
        ("eu", "rest", "https://api.kentik.eu/api/v5"),
        ("us", "grpc", "https://api.kentik.com/api/v5"),
        ("EU", "grpc", "https://api.kentik.eu/api/v5"),
    ],
)
def test_the_region_picks_the_v5_host_for_either_protocol(region, protocol, url):
    client = _client(region=region, protocol=protocol)
    try:
        assert client.v5_api_config.base_path == url
        assert isinstance(client._v5_transport, RestTransport)
    finally:
        client.close()


def test_v5_base_url_overrides_the_region():
    client = _client(region="eu", v5_base_url="https://kentik.internal/api/v5")
    try:
        assert client.v5_api_config.base_path == "https://kentik.internal/api/v5"
        assert client.api_config.base_path == "https://grpc.api.kentik.eu"
    finally:
        client.close()


def test_a_v5_base_url_without_https_is_refused():
    with pytest.raises(ConfigurationError, match="must start with https://"):
        _client(v5_base_url="http://kentik.internal/api/v5")


def test_the_v5_config_shares_credentials_and_timeouts():
    client = _client(timeout=12.0, rest_timeout=7.0)
    try:
        v5, v6 = client.v5_api_config, client.api_config
        assert (v5.auth_email, v5.auth_token) == (v6.auth_email, v6.auth_token)
        assert v5.timeout == v6.timeout == 12.0
        assert v5.rest_timeout == v6.rest_timeout
    finally:
        client.close()


def test_close_closes_both_transports():
    client = _client()
    client.close()

    for config in (client.api_config, client.v5_api_config):
        with pytest.raises(ConfigurationError, match="closed"):
            _ = config.client


def test_close_closes_the_v5_transport_when_the_main_one_fails(monkeypatch):
    client = _client()

    def fail():
        raise RuntimeError("boom")

    monkeypatch.setattr(client._transport, "close", fail)
    with pytest.raises(RuntimeError, match="boom"):
        client.close()

    with pytest.raises(ConfigurationError, match="closed"):
        _ = client.v5_api_config.client
    client.api_config.close()


@respx.mock
def test_a_relative_path_joins_the_v5_base_path():
    route = respx.post("https://api.kentik.com/api/v5/query/topXdata").respond(
        200, json={"results": []}
    )
    client = _client()
    try:
        body = request_json(
            "POST", "/query/topXdata", api_config_override=client.v5_api_config
        )
    finally:
        client.close()

    assert route.called
    assert body == {"results": []}


def test_v5_calls_follow_the_proxy_variables(monkeypatch: pytest.MonkeyPatch):
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"):
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)
    monkeypatch.setenv("HTTPS_PROXY", "proxy.internal:3128")
    monkeypatch.setenv("NO_PROXY", "api.kentik.com")
    built: list[dict] = []

    def _spy(*args, **kwargs):
        built.append(kwargs)
        return _REAL_CLIENT(*args, **kwargs)

    monkeypatch.setattr(httpx, "Client", _spy)
    client = _client()
    try:
        _ = client.v5_api_config.client
    finally:
        client.close()

    mounts = built[0]["mounts"]
    assert built[0]["base_url"] == "https://api.kentik.com/api/v5"
    assert mounts["all://*api.kentik.com"] is None
    assert mounts["https://"] is not None
