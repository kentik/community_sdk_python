# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Exact auth wire format for both transports (FR-039).

Kentik rejects a request whose auth key is misspelled with the same 401 as a
wrong token, so these keys are asserted verbatim rather than loosely.
"""

from __future__ import annotations

from typing import Any

from kentik_api.auth.credentials import KentikCredentials, auth_headers
from kentik_api.core.api_config import APIConfig

CREDENTIALS = KentikCredentials(email="dev@example.com", api_token="secret-token")


def test_grpc_plugin_emits_exact_auth_metadata():
    received = []
    plugin: Any = CREDENTIALS.get_grpc_plugin()

    plugin(context=None, callback=lambda md, err: received.append((md, err)))

    assert received == [
        (
            (
                ("x-ch-auth-email", "dev@example.com"),
                ("x-ch-auth-api-token", "secret-token"),
            ),
            None,
        )
    ]


def test_rest_auth_headers_carry_exact_keys():
    assert auth_headers("dev@example.com", "secret-token") == {
        "X-CH-Auth-Email": "dev@example.com",
        "X-CH-Auth-API-Token": "secret-token",
    }


def test_grpc_transport_attaches_the_credentials_plugin_to_the_channel(monkeypatch):
    import grpc

    from kentik_api.transports.grpc_client import GrpcTransport

    seen = {}
    monkeypatch.setattr(
        grpc,
        "metadata_call_credentials",
        lambda plugin: seen.setdefault("plugin", plugin) and object(),
    )
    monkeypatch.setattr(grpc, "composite_channel_credentials", lambda *a, **k: object())
    monkeypatch.setattr(grpc, "secure_channel", lambda *a, **k: object())
    monkeypatch.setattr(grpc, "intercept_channel", lambda channel, _: channel)

    GrpcTransport(
        APIConfig(auth_email=CREDENTIALS.email, auth_token=CREDENTIALS.api_token),
        target="grpc.example.com:443",
    )

    received = []
    seen["plugin"](context=None, callback=lambda md, err: received.append(md))
    assert received == [
        (
            ("x-ch-auth-email", "dev@example.com"),
            ("x-ch-auth-api-token", "secret-token"),
        )
    ]
