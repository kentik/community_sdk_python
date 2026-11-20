# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The V5 description in the local schema base (spec 005, FR-001, FR-010, FR-010a).

The local schema base holds only V5 endpoints that have no V6 equivalent, and
declares no enum, so an unknown value from the API never fails a call.
"""

from __future__ import annotations

import json
from pathlib import Path

_DESCRIPTION = (
    Path(__file__).resolve().parents[2]
    / "schema"
    / "openapi"
    / "v5"
    / "v5"
    / "v5.swagger.json"
)
_SCHEMA = json.loads(_DESCRIPTION.read_text(encoding="utf-8"))

EXPECTED_OPERATIONS = {
    "POST /query/topXdata",
    "POST /query/topXchart",
    "POST /query/url",
    "POST /batch/tags",
    "POST /batch/customdimensions/{dimensionName}/populators",
    "GET /batch/{guid}/status",
}


def _operations() -> set[str]:
    return {
        f"{method.upper()} {path}"
        for path, item in _SCHEMA["paths"].items()
        for method in item
    }


def test_the_description_declares_exactly_the_v5_only_operations():
    assert _operations() == EXPECTED_OPERATIONS


def test_the_retired_sql_endpoint_is_not_declared():
    assert not any("sql" in path.lower() for path in _SCHEMA["paths"])


def test_the_description_declares_no_enum():
    assert '"enum"' not in _DESCRIPTION.read_text(encoding="utf-8")


def test_every_operation_declares_the_v5_error_statuses():
    for item in _SCHEMA["paths"].values():
        for operation in item.values():
            assert {"400", "401", "403", "404", "429", "500"} <= set(
                operation["responses"]
            ), operation["operationId"]
