# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import os
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from kentik_api.client import _REGION_ENDPOINTS, KentikAPI
from kentik_api.errors import ConfigurationError, KentikError


def test_region_endpoints_us_urls():
    grpc_target, rest_url = _REGION_ENDPOINTS["us"]
    assert grpc_target == "grpc.api.kentik.com:443"
    assert rest_url == "https://grpc.api.kentik.com"


def test_region_endpoints_eu_urls():
    grpc_target, rest_url = _REGION_ENDPOINTS["eu"]
    assert grpc_target == "grpc.api.kentik.eu:443"
    assert rest_url == "https://grpc.api.kentik.eu"


def test_invalid_region_raises_configuration_error_naming_it():
    with pytest.raises(ConfigurationError, match="apac") as exc_info:
        KentikAPI(email="a@b.com", api_token="t", region="apac")

    assert isinstance(exc_info.value, KentikError)
    assert not isinstance(exc_info.value, ValueError)


def test_invalid_protocol_raises_configuration_error_naming_it():
    with pytest.raises(ConfigurationError, match="carrier-pigeon"):
        KentikAPI(email="a@b.com", api_token="t", protocol="carrier-pigeon")


def test_missing_credentials_raise_configuration_error(monkeypatch, tmp_path):
    # Run from a directory with no .env above it, so the real one is never loaded.
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("KENTIK_EMAIL", raising=False)
    monkeypatch.delenv("KENTIK_API_TOKEN", raising=False)

    with pytest.raises(KentikError, match="KENTIK_EMAIL") as exc_info:
        KentikAPI()

    assert type(exc_info.value) is ConfigurationError


@pytest.fixture
def no_env_credentials(monkeypatch, tmp_path):
    """A working directory with no .env above it and no credential env vars."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("KENTIK_EMAIL", raising=False)
    monkeypatch.delenv("KENTIK_API_TOKEN", raising=False)
    return tmp_path


def _credentials(client: KentikAPI) -> tuple[str, str]:
    return client.credentials.email, client.credentials.api_token


def test_env_file_is_read_without_touching_os_environ(no_env_credentials):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN=file-token\nOTHER=x\n"
    )

    with KentikAPI() as client:
        assert _credentials(client) == ("file@example.com", "file-token")

    # Secrets in os.environ would leak into every subprocess the caller starts.
    assert "KENTIK_EMAIL" not in os.environ
    assert "KENTIK_API_TOKEN" not in os.environ
    assert "OTHER" not in os.environ


def test_env_file_is_found_in_a_parent_directory(no_env_credentials, monkeypatch):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN=file-token\n"
    )
    child = no_env_credentials / "a" / "b"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)

    with KentikAPI() as client:
        assert _credentials(client) == ("file@example.com", "file-token")


def test_explicit_credentials_never_read_env_file(no_env_credentials, monkeypatch):
    (no_env_credentials / ".env").write_text("KENTIK_EMAIL=file@example.com\n")
    read = []
    monkeypatch.setattr(
        "kentik_api.client.dotenv_values", lambda path: read.append(path) or {}
    )

    with KentikAPI(email="arg@example.com", api_token="arg-token") as client:
        assert _credentials(client) == ("arg@example.com", "arg-token")
    assert read == []


def test_explicit_env_file_path_is_used(no_env_credentials):
    secrets = no_env_credentials / "elsewhere" / "kentik.env"
    secrets.parent.mkdir()
    secrets.write_text("KENTIK_EMAIL=path@example.com\nKENTIK_API_TOKEN=path-token\n")

    with KentikAPI(env_file=secrets) as client:
        assert _credentials(client) == ("path@example.com", "path-token")


# python-dotenv before 1.2.3 dropped the first variable after a byte order mark.
def test_env_file_with_byte_order_mark_keeps_first_variable(no_env_credentials):
    (no_env_credentials / ".env").write_text(
        "\ufeffKENTIK_EMAIL=bom@example.com\nKENTIK_API_TOKEN=bom-token\n",
        encoding="utf-8",
    )

    with KentikAPI() as client:
        assert _credentials(client) == ("bom@example.com", "bom-token")


# python-dotenv before 1.2.4 read the comment text as the value.
def test_env_file_empty_value_with_comment_is_missing(no_env_credentials):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN= # set me\n"
    )

    with pytest.raises(ConfigurationError, match="Missing Kentik credentials"):
        KentikAPI()


def test_env_file_none_disables_file_lookup(no_env_credentials):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN=file-token\n"
    )

    with pytest.raises(ConfigurationError, match="KENTIK_EMAIL") as exc_info:
        KentikAPI(env_file=None)
    assert ".env" not in str(exc_info.value)


def test_environment_beats_env_file_and_args_beat_both(no_env_credentials, monkeypatch):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN=file-token\n"
    )
    monkeypatch.setenv("KENTIK_EMAIL", "env@example.com")

    with KentikAPI() as client:
        assert _credentials(client) == ("env@example.com", "file-token")
    with KentikAPI(api_token="arg-token") as client:
        assert _credentials(client) == ("env@example.com", "arg-token")


@pytest.mark.parametrize("field", ["email", "api_token"])
@pytest.mark.parametrize("value", ["", "  "])
def test_an_explicit_empty_credential_is_refused(no_env_credentials, field, value):
    (no_env_credentials / ".env").write_text(
        "KENTIK_EMAIL=file@example.com\nKENTIK_API_TOKEN=file-token\n"
    )
    args: dict[str, Any] = {
        "email": "arg@example.com",
        "api_token": "arg-token",
        field: value,
    }

    with pytest.raises(ConfigurationError, match=field):
        KentikAPI(**args)


def test_client_mounts_selected_services():
    client = KentikAPI(
        email="dev@example.com",
        api_token="token",
        protocol="rest",
        region="us",
    )
    try:
        assert hasattr(client, "asset_tags")
        assert hasattr(client, "custom_dimension")
        assert hasattr(client, "user")
    finally:
        client.close()


def test_smoke_wrapper_call_through_client(monkeypatch):
    client = KentikAPI(
        email="dev@example.com",
        api_token="token",
        protocol="rest",
        region="us",
    )

    try:
        sentinel = object()

        import kentik_api.gen.asset_tags.services.AssetTagsService as asset_tags_rest

        def _fake_list_tag_keys(**kwargs):
            return sentinel

        monkeypatch.setattr(asset_tags_rest, "ListTagKeys", _fake_list_tag_keys)

        result = client.asset_tags.list_tag_keys()
        assert result is sentinel
    finally:
        client.close()


def test_client_timeout_defaults_to_sixty_seconds_on_both_transports():
    for protocol in ("rest", "grpc"):
        with KentikAPI(email="a@b.com", api_token="t", protocol=protocol) as client:
            config = client._transport.api_config
            assert config.rest_timeout == httpx.Timeout(60.0)
            assert config.grpc_deadline == 60.0


@pytest.mark.parametrize("protocol", ["rest", "grpc"])
def test_client_timeout_reaches_the_transport(protocol):
    with KentikAPI(
        email="a@b.com", api_token="t", protocol=protocol, timeout=5.0
    ) as client:
        config = client._transport.api_config
        assert config.rest_timeout == httpx.Timeout(5.0)
        assert config.grpc_deadline == 5.0
        assert config.base_path == "https://grpc.api.kentik.com"
        assert (config.auth_email, config.auth_token) == ("a@b.com", "t")


def test_client_accepts_per_transport_refinements():
    phases = httpx.Timeout(connect=2.0, read=300.0, write=10.0, pool=5.0)

    with KentikAPI(
        email="a@b.com", api_token="t", rest_timeout=phases, grpc_deadline=120.0
    ) as client:
        assert client._transport.api_config.rest_timeout == phases
        assert client._transport.api_config.rest_timeout is not phases
        assert client._transport.api_config.grpc_deadline == 120.0


def test_client_rejects_a_non_positive_timeout():
    with pytest.raises(ConfigurationError, match="timeout"):
        KentikAPI(email="a@b.com", api_token="t", timeout=0)


@pytest.mark.parametrize("phase", ["connect", "read", "write", "pool"])
@pytest.mark.parametrize("protocol", ["rest", "grpc"])
def test_client_timeout_values_are_isolated_between_v5_and_v6(phase, protocol):
    supplied = httpx.Timeout(connect=2.0, read=3.0, write=5.0, pool=7.0)
    with KentikAPI(
        email="a@b.com",
        api_token="t",
        protocol=protocol,
        rest_timeout=supplied,
        env_file=None,
    ) as client:
        setattr(supplied, phase, None)
        setattr(client.api_config.rest_timeout, phase, 11.0)
        setattr(client.v5_api_config.rest_timeout, phase, 13.0)

        for config in (client.api_config, client.v5_api_config):
            assert config.rest_timeout == httpx.Timeout(
                connect=2.0, read=3.0, write=5.0, pool=7.0
            )
            assert config.rest_deadline is None
            assert config.grpc_deadline == 60.0


def test_client_exposes_its_config_read_only():
    with KentikAPI(email="a@b.com", api_token="t", timeout=30.0) as client:
        assert client.api_config is client._transport.api_config
        assert client.api_config.grpc_deadline == 30.0
        with pytest.raises(AttributeError):
            client.api_config = None  # type: ignore[misc]


def test_one_call_can_override_the_timeout_without_affecting_the_next(monkeypatch):
    sent = []

    def _capture(self, *args, timeout=None, **kwargs):
        sent.append((self, timeout))
        return httpx.Response(200, json={"devices": []})

    monkeypatch.setattr(httpx.Client, "request", _capture)

    with KentikAPI(email="a@b.com", api_token="t") as client:
        client.device.list(api_config_override=client.api_config.with_timeout(300))
        client.device.list()

    (slow_client, slow_timeout), (normal_client, normal_timeout) = sent
    assert slow_timeout == httpx.Timeout(300)
    assert normal_timeout == httpx.Timeout(60.0)
    assert slow_client is normal_client


def test_result_carries_the_quota_of_the_call_that_produced_it(monkeypatch):
    from kentik_api import rate_limit_of

    headers = {"x-ratelimit-limit": "60, 60;w=60", "x-ratelimit-remaining": "17"}
    monkeypatch.setattr(
        httpx.Client,
        "request",
        lambda self, *a, **k: httpx.Response(
            200, json={"devices": []}, headers=headers
        ),
    )

    with KentikAPI(email="a@b.com", api_token="t") as client:
        result = client.device.list()

    rate_limit = rate_limit_of(result)
    assert rate_limit is not None
    assert rate_limit.remaining == 17
    assert "_kentik_rate_limit" not in result.model_dump()


@pytest.mark.parametrize("region", ["us", "eu"])
def test_region_selects_the_rest_and_grpc_hosts(
    region, monkeypatch, no_env_credentials
):
    import grpc

    targets = []
    monkeypatch.setattr(
        grpc,
        "secure_channel",
        lambda target, creds, **kw: targets.append(target) or MagicMock(),
    )
    monkeypatch.setattr(grpc, "intercept_channel", lambda channel, _: channel)
    grpc_target, rest_url = _REGION_ENDPOINTS[region]

    rest = KentikAPI("a@b.com", "t", region=region, env_file=None)
    assert rest.api_config.base_path == rest_url

    KentikAPI("a@b.com", "t", protocol="grpc", region=region, env_file=None)
    assert targets == [grpc_target]
    assert grpc_target.endswith(".eu:443") == (region == "eu")


@pytest.mark.parametrize("protocol", ["rest", "grpc"])
def test_v5_calls_go_over_rest_to_the_v5_host_on_either_protocol(
    protocol, monkeypatch, no_env_credentials
):
    import grpc
    import respx

    from kentik_api.gen.v5.models import Query, QueryItem, QueryRequest
    from kentik_api.transports.rest_client import RestTransport

    monkeypatch.setattr(grpc, "secure_channel", lambda *a, **k: MagicMock())
    monkeypatch.setattr(grpc, "intercept_channel", lambda channel, _: channel)
    client = KentikAPI("a@b.com", "t", protocol=protocol, env_file=None)
    query = Query(metric="bytes", dimension=["Proto"], device_name="router1")

    with respx.mock:
        route = respx.post("https://api.kentik.com/api/v5/query/topXdata").respond(
            200, json={"results": [{"bucket": "a", "data": [{"key": "TCP"}]}]}
        )
        result = client.v5.top_x_data(
            data=QueryRequest(queries=[QueryItem(query=query, bucket="a")])
        )

    assert isinstance(client.v5._transport, RestTransport)
    assert route.called
    assert result.results is not None
    bucket = result.results[0]
    assert bucket is not None
    assert bucket.data == [{"key": "TCP"}]
