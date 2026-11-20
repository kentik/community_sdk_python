# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Query definitions give the same DataFrames as 1.x (spec 005, FR-016 to FR-018)."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest
import respx

from kentik_api import KentikAPI
from kentik_api.analytics import (
    DataQueryDefinition,
    SQLQueryDefinition,
    data_result_to_df,
)

FIXTURES = Path(__file__).parent / "fixtures"
RESPONSE = json.loads((FIXTURES / "topx_response.json").read_text())
START = datetime(2025, 10, 16, tzinfo=UTC)


def _golden(bucket_slug: str) -> pd.DataFrame:
    text = (FIXTURES / f"golden_topx_{bucket_slug}.json").read_text()
    return pd.read_json(StringIO(text), orient="table")


def _comparable(df: pd.DataFrame) -> pd.DataFrame:
    # A non-unique index comes back from orient="table" as a column, so compare
    # flat frames. Text is object dtype in the file and str in pandas 3.
    flat = df.reset_index(drop=df.index.name is None)
    return flat.astype(
        {c: object for c in flat.select_dtypes(exclude="number").columns}
    )


@pytest.mark.parametrize(
    ("bucket", "slug", "index"),
    [("Left +Y Axis", "left_plusy_axis", "ts"), ("Top", "top", "protocol")],
)
def test_a_v1_definition_gives_the_v1_dataframes(bucket: str, slug: str, index: str):
    definition = DataQueryDefinition.from_file(FIXTURES / "topx_definition.yaml")

    frames = data_result_to_df(definition.mappings, RESPONSE["results"])

    produced = frames[bucket]
    pd.testing.assert_frame_equal(_comparable(produced), _comparable(_golden(slug)))
    assert produced.index.name == index


def test_placeholders_are_filled_as_v1_filled_them():
    definition = DataQueryDefinition.from_file(FIXTURES / "topx_definition.yaml")

    expanded = definition.expand_query(start=START, end=START + timedelta(hours=1))

    golden = json.loads((FIXTURES / "golden_topx_expanded_query.json").read_text())
    assert expanded == golden


@pytest.mark.parametrize("placeholder", ["{start.__class__}", "{start[0]}", "{}"])
def test_a_placeholder_must_be_a_plain_name(placeholder: str):
    definition = DataQueryDefinition(query={"q": placeholder}, mappings={})

    with pytest.raises(ValueError, match="must be a plain name"):
        definition.expand_query(start=START)


@respx.mock
def test_get_data_sends_the_filled_query_and_maps_the_response():
    route = respx.post("https://api.kentik.com/api/v5/query/topXdata").respond(
        200, json=RESPONSE
    )
    definition = DataQueryDefinition.from_file(FIXTURES / "topx_definition.yaml")
    client = KentikAPI("dev@example.com", "token", env_file=None)
    try:
        frames = definition.get_data(
            client, start=START, end=START + timedelta(hours=1)
        )
    finally:
        client.close()

    sent = json.loads(route.calls.last.request.content)
    assert sent["queries"][0]["query"]["starting_time"] == "2025-10-16 00:00"
    assert set(frames) == {"Left +Y Axis", "Top"}
    assert frames["Top"].shape == (3, 1)


def test_an_empty_bucket_gives_an_empty_dataframe_with_the_columns():
    definition = DataQueryDefinition.from_file(FIXTURES / "topx_definition.yaml")

    frames = data_result_to_df(definition.mappings, [{"bucket": "Top", "data": []}])

    assert frames["Top"].empty
    assert frames["Top"].index.name == "protocol"
    assert list(frames["Top"].columns) == ["avg_bps"]


@pytest.mark.parametrize(
    "definition",
    [
        {"query": "SELECT i_start_time FROM all_devices", "mapping": {}},
        {"query": "  select 1", "mappings": {"all": {"a": {"source": "{a}"}}}},
    ],
)
def test_a_sql_definition_fails_with_the_retirement_reason(definition: dict):
    with pytest.raises(ValueError, match="retired the V5 SQL query endpoint"):
        DataQueryDefinition.from_dict(definition)
    with pytest.raises(ValueError, match="retired the V5 SQL query endpoint"):
        SQLQueryDefinition.from_dict(definition)


def test_a_fixup_mapping_is_refused_without_running_it(tmp_path: Path):
    marker = tmp_path / "ran"
    definition = {
        "query": {"queries": []},
        "mappings": {
            "all": {
                "x": {
                    "source": "{key}",
                    "type": f"@fixup: lambda v: open({str(marker)!r}, 'w')",
                }
            }
        },
    }

    with pytest.raises(ValueError, match="'@fixup:' column type ran Python code"):
        DataQueryDefinition.from_dict(definition)
    assert not marker.exists()


def test_a_yaml_tag_that_builds_an_object_is_refused(tmp_path: Path):
    path = tmp_path / "evil.yaml"
    path.write_text("query: !!python/object/apply:os.getcwd []\nmappings: {}\n")

    with pytest.raises(Exception, match="python/object"):
        DataQueryDefinition.from_file(path)
