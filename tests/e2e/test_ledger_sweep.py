# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The e2e cleanup keeps going when one object's lookup or delete fails in transit."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest
from ledger import KINDS, Kind, Ledger, sweep

from kentik_api.client import KentikAPI
from kentik_api.errors import TransportError


@pytest.mark.parametrize("failing", ["get", "delete"])
def test_sweep_continues_after_a_transport_failure(tmp_path, monkeypatch, failing):
    ledger = Ledger(tmp_path / "objects.jsonl", run="t")
    ledger.created("label", "first", "sdk-e2e-test-first")
    ledger.created("label", "second", "sdk-e2e-test-second")
    deleted = []

    def get(client, id):
        if failing == "get" and id == "first":
            raise TransportError("timeout")
        return SimpleNamespace(name=f"sdk-e2e-test-{id}")

    def delete(client, id):
        if failing == "delete" and id == "first":
            raise TransportError("timeout")
        deleted.append(id)

    monkeypatch.setitem(KINDS, "label", Kind(get, "name", delete))

    failures = sweep(cast(KentikAPI, SimpleNamespace()), ledger, ledger.outstanding())

    assert len(failures) == 1
    assert deleted == ["second"]
