# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""flatness_analysis gives the 1.x result on the same input (FR-020, SC-003)."""

from __future__ import annotations

import json
from datetime import timedelta
from io import StringIO
from pathlib import Path

import pandas as pd

from kentik_api.analytics import flatness_analysis

FIXTURES = Path(__file__).parent / "fixtures"


class _OneGigabitLinks:
    def get_link_speeds(self, links=None) -> dict[str, float]:
        return {link: 1e9 for link in links or []}


def _input() -> pd.DataFrame:
    text = (FIXTURES / "flatness_input.json").read_text()
    data = pd.read_json(StringIO(text), orient="table")
    return data.set_index("ts") if "ts" in data else data


def test_flatness_matches_the_v1_result():
    speeds = _OneGigabitLinks()

    results = flatness_analysis(
        speeds, _input(), flatness_limit=2, window=timedelta(hours=1)
    )

    golden = json.loads((FIXTURES / "golden_flatness.json").read_text())
    assert json.loads(results.to_json()) == {
        link: [list(interval) for interval in intervals]
        for link, intervals in golden.items()
    }
    assert results.affected_links == ["router1:eth0"]


def test_no_flat_traffic_gives_no_events():
    data = _input()
    data = data.loc[data["link"] == "router2:eth1"]
    speeds = _OneGigabitLinks()

    results = flatness_analysis(
        speeds, data, flatness_limit=2, window=timedelta(hours=1)
    )

    assert results.stats == {"total_events": 0, "max_per_link": 0}
