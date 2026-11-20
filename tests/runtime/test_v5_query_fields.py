# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Every V5 SDK query field reaches the API unchanged (spec 005, FR-002)."""

from __future__ import annotations

import json
from pathlib import Path

from kentik_api.gen.v5.models import Query, QueryItem

_FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "v5_query_fields.json").read_text()
)


def test_every_v5_sdk_query_field_round_trips():
    fields = _FIXTURE["fields"]

    query = Query.model_validate(fields)

    assert query.model_dump(by_alias=True, exclude_unset=True) == fields


def test_query_item_keeps_fields_it_does_not_type():
    item = QueryItem.model_validate(
        {"query": {"metric": "bytes", "dimension": ["Proto"]}, "bucketIndex": 0, "x": 1}
    )

    assert item.model_dump(by_alias=True, exclude_unset=True)["x"] == 1
