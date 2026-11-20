# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Live batch round trip. MUTATING: it writes to the real account.

Opt-in like every e2e test, and also behind its own marker, so `uv run poe test-e2e`
never runs it: `pytest -m e2e_mutating --run-live-e2e tests/e2e/test_v5_batch_e2e.py`.
It upserts one flow tag with a unique, disposable name on a TEST-NET-1 address
(RFC 5737, never routed), then deletes it in a second batch in `finally`.
`replace_all` stays False, so no other tag can be touched (constitution
Principle V).
"""

from __future__ import annotations

import uuid

import pytest

from kentik_api.gen.v5.models import BatchCriterion, BatchDelete, BatchUpsert
from kentik_api.v5_tools import send_batch, split_batch, wait_for_batch

pytestmark = pytest.mark.e2e_mutating


def test_a_flow_tag_batch_upserts_then_deletes_a_disposable_tag(real_client):
    tag = f"sdk-e2e-{uuid.uuid4().hex[:8]}"
    upsert = BatchUpsert(value=tag, criteria=[BatchCriterion(addr=["192.0.2.1/32"])])
    try:
        parts = split_batch([upsert], replace_all=False)
        assert all(part.replace_all is False for part in parts)
        guid = send_batch(real_client.v5.batch_tags, parts)
        status = wait_for_batch(real_client, guid, timeout=300, interval=5)
        assert status.upserts is not None
        assert status.upserts.applied == 1
    finally:
        cleanup = split_batch([], [BatchDelete(value=tag)], replace_all=False)
        guid = send_batch(real_client.v5.batch_tags, cleanup)
        status = wait_for_batch(real_client, guid, timeout=300, interval=5)
    assert status.deletes is not None
    assert status.deletes.applied == 1
