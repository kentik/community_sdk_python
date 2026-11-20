# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""split_batch() packs a batch into parts the API accepts (spec 005, FR-013)."""

from __future__ import annotations

import json

import pytest

from kentik_api.gen.v5.models import BatchCriterion, BatchDelete, BatchUpsert
from kentik_api.v5_tools import split_batch


def _upsert(n: int) -> BatchUpsert:
    return BatchUpsert(
        value=f"tag-{n}", criteria=[BatchCriterion(addr=[f"10.0.{n // 256}.{n % 256}"])]
    )


def _wire_size(part) -> int:
    return len(json.dumps(part.model_dump(by_alias=True, exclude_unset=True)).encode())


def _values(items) -> list[str]:
    return [item.value for item in items or [] if item is not None]


def test_every_part_fits_and_only_the_last_is_complete():
    parts = split_batch([_upsert(n) for n in range(500)], max_bytes=4_000)

    assert len(parts) > 1
    assert all(_wire_size(part) <= 4_000 for part in parts)
    assert [part.complete for part in parts] == [False] * (len(parts) - 1) + [True]
    assert [v for part in parts for v in _values(part.upserts)] == [
        f"tag-{n}" for n in range(500)
    ]


def test_deletes_follow_every_upsert_and_replace_all_is_on_every_part():
    upserts = [_upsert(n) for n in range(200)]
    deletes = [BatchDelete(value=f"old-{n}") for n in range(50)]

    parts = split_batch(upserts, deletes, replace_all=True, max_bytes=2_000)

    seen = [("u", v) for part in parts for v in _values(part.upserts)] + [
        ("d", v) for part in parts for v in _values(part.deletes)
    ]
    assert len(seen) == 250
    last_upsert = max(i for i, part in enumerate(parts) if part.upserts)
    first_delete = min(i for i, part in enumerate(parts) if part.deletes)
    assert first_delete >= last_upsert
    assert all(part.replace_all for part in parts)


def test_a_small_set_is_one_complete_part():
    parts = split_batch([_upsert(1)])

    assert len(parts) == 1
    assert parts[0].complete is True
    assert parts[0].guid is None


def test_one_upsert_larger_than_a_part_is_refused():
    huge = BatchUpsert(value="x" * 5_000)

    with pytest.raises(ValueError, match="larger than max_bytes"):
        split_batch([huge], max_bytes=4_000)


def test_ten_thousand_flow_tags_fit_in_at_most_one_hundred_parts():
    parts = split_batch([_upsert(n) for n in range(10_000)])

    assert len(parts) <= 100
