# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Make the golden outputs of the 1.x analytics code (spec 005, SC-003).

Runs the 1.x functions themselves, read from git, on the inputs in this folder,
so the 2.x tests compare against real 1.x output. Run it once, offline, from the
repository root, in an environment without this repo's packages:

    uv run --no-project --with pandas==2.3.3 --with pyyaml \
        python tests/analytics/fixtures/make_golden.py

It writes golden_*.json and flatness_input.json next to this file. The 1.x
modules import kentik_api only for types, so stubs replace those imports.
"""

from __future__ import annotations

import json
import subprocess
import sys
import types
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pandas as pd

COMMIT = "b48cfd912b162f99290ff00170916abf9cd67d23"  # origin/main, kentik-api 1.0.7
HERE = Path(__file__).resolve().parent


def _v1_module(name: str, path: str, replacements: dict[str, str]) -> types.ModuleType:
    source = subprocess.run(
        ["git", "show", f"{COMMIT}:{path}"], check=True, capture_output=True, text=True
    ).stdout
    for old, new in replacements.items():
        assert old in source, old
        source = source.replace(old, new)
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(compile(source, path, "exec"), module.__dict__)  # noqa: S102 - runs the patched V5 source to record golden output
    return module


def _table_json(df: pd.DataFrame) -> str:
    text = df.to_json(orient="table", indent=2)
    assert text is not None
    return text


def topx_golden() -> None:
    mapped_query = _v1_module(
        "v1_mapped_query",
        "kentik_api/analytics/mapped_query.py",
        {
            "from kentik_api import KentikAPI\n": "KentikAPI = object\n",
            "from kentik_api.public import QueryDataResult, QueryObject, QuerySQL, QuerySQLResult\n": (
                "QueryDataResult = QueryObject = QuerySQL = QuerySQLResult = object\n"
            ),
        },
    )
    definition = mapped_query.DataQueryDefinition.from_file(
        str(HERE / "topx_definition.yaml")
    )
    response = json.loads((HERE / "topx_response.json").read_text())
    frames = mapped_query.data_result_to_df(
        definition.mappings, types.SimpleNamespace(results=response["results"])
    )
    for bucket, frame in frames.items():
        slug = bucket.lower().replace(" ", "_").replace("+", "plus")
        (HERE / f"golden_topx_{slug}.json").write_text(_table_json(frame))
    start = datetime(2025, 10, 16, tzinfo=UTC)
    expanded = definition.expand_query(start=start, end=start + timedelta(hours=1))
    (HERE / "golden_topx_expanded_query.json").write_text(
        json.dumps(expanded, indent=2)
    )


def flatness_golden() -> None:
    flatness = _v1_module(
        "v1_flatness",
        "kentik_api/analytics/flatness.py",
        {"from kentik_api.utils import DeviceCache\n": "DeviceCache = object\n"},
    )
    index = pd.date_range("2025-10-16T00:00:00Z", periods=72, freq="5min", name="ts")
    flat_bytes = 0.5e9 * 300 / 8  # 50% of 1 Gbit/s for 5 minutes
    frames = []
    for n, link in enumerate(["router1:eth0", "router2:eth1"]):
        values = [
            flat_bytes
            if (link == "router1:eth0" and 12 <= i < 48)
            else flat_bytes * (0.2 + 0.1 * ((i * (n + 3)) % 7))
            for i in range(len(index))
        ]
        frames.append(pd.DataFrame({"link": link, "bytes_out": values}, index=index))
    data = pd.concat(frames).sort_index()
    (HERE / "flatness_input.json").write_text(_table_json(data))

    speeds = types.SimpleNamespace(
        get_link_speeds=lambda links: {link: 1e9 for link in links}
    )
    results = flatness.flatness_analysis(
        speeds, data, flatness_limit=2, window=timedelta(hours=1)
    )
    (HERE / "golden_flatness.json").write_text(results.to_json(indent=2))


if __name__ == "__main__":
    topx_golden()
    flatness_golden()
    print(f"Golden outputs written to {HERE} with pandas {pd.__version__}.")
