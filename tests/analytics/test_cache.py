# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""DFCache stores Parquet by time range and fetches only what it lacks (FR-019)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from kentik_api.analytics import DFCache, dedup_data_frame
from kentik_api.analytics import cache as cache_module

START = datetime(2025, 10, 16, tzinfo=UTC)


def _frame(start: datetime, end: datetime) -> pd.DataFrame:
    index = pd.date_range(start, end, freq="1min", inclusive="left", name="ts")
    return pd.DataFrame({"link": "router1:eth0", "bps": range(len(index))}, index=index)


class _Query:
    def __init__(self):
        self.calls: list[tuple[datetime, datetime]] = []

    def __call__(self, *, start, end):
        self.calls.append((start, end))
        return _frame(start, end)


def test_fetch_stores_parquet_files_and_returns_the_range(tmp_path: Path):
    cache = DFCache(tmp_path)
    query = _Query()

    df = cache.fetch(query, START, START + timedelta(hours=2), step=timedelta(hours=1))

    assert len(query.calls) == 2
    assert df is not None and len(df) == 120
    assert all(path.suffix == ".parquet" for path in cache.files)
    assert cache.file_count == 2


def test_a_second_fetch_fetches_only_the_missing_steps(tmp_path: Path):
    cache = DFCache(tmp_path)
    cache.fetch(_Query(), START, START + timedelta(hours=1), step=timedelta(hours=1))
    query = _Query()

    df = cache.fetch(query, START, START + timedelta(hours=3), step=timedelta(hours=1))

    assert query.calls == [
        (START + timedelta(hours=1), START + timedelta(hours=2)),
        (START + timedelta(hours=2), START + timedelta(hours=3)),
    ]
    assert df is not None
    assert len(df) == 180


def test_a_fetch_without_step_skips_a_cached_range(tmp_path: Path):
    cache = DFCache(tmp_path)
    cache.fetch(_Query(), START, START + timedelta(hours=2))
    query = _Query()

    df = cache.fetch(query, START, START + timedelta(hours=1))

    assert query.calls == []
    assert df is not None
    assert len(df) == 61


def test_fetch_removes_duplicate_rows(tmp_path: Path):
    cache = DFCache(tmp_path)
    cache.store(_frame(START, START + timedelta(minutes=30)))
    query = _Query()

    df = cache.fetch(
        query,
        START + timedelta(minutes=20),
        START + timedelta(minutes=50),
        dedup_columns=["ts", "link"],
    )

    assert query.calls == [
        (START + timedelta(minutes=20), START + timedelta(minutes=50))
    ]
    assert df is not None
    assert df.index.is_unique
    assert len(df) == 30


def test_get_includes_file_ending_at_start(tmp_path: Path):
    cache = DFCache(tmp_path)
    end = START + timedelta(minutes=2)
    frame = _frame(START, end)
    cache.store(frame)

    result = cache.get(end - timedelta(minutes=1), end)

    assert result is not None
    pd.testing.assert_frame_equal(result, frame.tail(1), check_freq=False)


def test_get_removes_duplicate_rows(tmp_path: Path):
    cache = DFCache(tmp_path)
    cache.store(_frame(START, START + timedelta(minutes=30)))
    cache.store(_frame(START + timedelta(minutes=20), START + timedelta(minutes=50)))

    df = cache.get(dedup_columns=["ts", "link"])

    assert df is not None
    assert df.index.is_unique
    assert len(df) == 50


def test_files_the_cache_did_not_write_are_ignored(tmp_path: Path):
    (tmp_path / "notes.parquet").write_bytes(b"not parquet")
    (tmp_path / "evil.pickle").write_bytes(b"\x80\x04K.")
    (tmp_path / "a_b.parquet").write_bytes(b"not parquet either")
    cache = DFCache(tmp_path)

    assert cache.is_empty
    assert cache.get() is None


def test_file_names_have_no_colon(tmp_path: Path):
    # Windows does not allow `:` in a file name.
    cache = DFCache(tmp_path)
    cache.store(_frame(START, START + timedelta(minutes=2)))

    assert [p.name for p in cache.files] == [
        "2025-10-16T00_00_00+00_00_2025-10-16T00_01_00+00_00.parquet"
    ]


@pytest.mark.parametrize(
    ("name", "start", "end"),
    [
        (
            "2025-10-16T00:00:00+00:00_2025-10-16T01:00:00+00:00.parquet",
            START,
            START + timedelta(hours=1),
        ),
        (
            "2025-10-16T00_00_00_2025-10-16T01_00_00.parquet",
            START,
            START + timedelta(hours=1),
        ),
    ],
)
def test_file_names_parse_with_or_without_colons(name: str, start, end):
    assert DFCache.parse_df_filename(Path(name)) == (start, end)


def test_a_file_name_without_an_offset_reads_as_utc(tmp_path: Path):
    cache = DFCache(tmp_path)
    cache.store(_frame(START, START + timedelta(minutes=2)))
    (tmp_path / "2025-10-16T02_00_00_2025-10-16T03_00_00.parquet").write_bytes(b"")

    assert cache.newest == START + timedelta(hours=3)


def test_naive_datetimes_are_refused(tmp_path: Path):
    cache = DFCache(tmp_path)
    naive = START.replace(tzinfo=None)

    with pytest.raises(ValueError, match="timezone-aware"):
        cache.fetch(_Query(), naive, naive + timedelta(hours=1))
    with pytest.raises(ValueError, match="timezone-aware"):
        cache.get(naive, START + timedelta(hours=1))


@pytest.mark.parametrize("step", [timedelta(0), timedelta(hours=-1)])
def test_a_step_that_is_not_positive_is_refused(tmp_path: Path, step):
    with pytest.raises(ValueError, match="step must be positive"):
        DFCache(tmp_path).fetch(_Query(), START, START + timedelta(hours=1), step=step)


def test_dedup_needs_the_named_columns():
    with pytest.raises(ValueError, match="not in the DataFrame"):
        dedup_data_frame(_frame(START, START + timedelta(minutes=2)), ["nope"])


@pytest.fixture
def cache_clock(monkeypatch):
    state = SimpleNamespace(now=START + timedelta(days=1, seconds=20))

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            assert tz is UTC
            return state.now

    monkeypatch.setattr(cache_module, "datetime", FrozenDateTime)
    return state


def test_fetch_latest_is_a_noop_until_the_next_minute(tmp_path, cache_clock):
    cache = DFCache(tmp_path)
    query = _Query()
    cutoff = START + timedelta(days=1)
    first = cache.fetch_latest(query)
    assert first is not None
    assert query.calls == [(START + timedelta(minutes=1), cutoff)]
    files = {path.name: path.read_bytes() for path in cache.files}
    cache_clock.now += timedelta(seconds=20)

    assert cache.fetch_latest(query) is None
    assert len(query.calls) == 1
    assert {path.name: path.read_bytes() for path in cache.files} == files
    got = cache.get()
    assert got is not None
    pd.testing.assert_frame_equal(got, first)

    cache_clock.now += timedelta(minutes=1)
    latest = cache.fetch_latest(query)
    assert latest is not None and len(latest) == 1
    assert query.calls[-1] == (cutoff, cutoff + timedelta(minutes=1))
    assert len(query.calls) == 2


@pytest.mark.parametrize("ahead", [0, 1, 60])
def test_fetch_latest_never_queries_a_current_or_future_range(
    tmp_path, cache_clock, ahead
):
    cache = DFCache(tmp_path)
    end = START + timedelta(days=1, minutes=ahead)
    frame = _frame(START, START + timedelta(minutes=2))
    cache.store(frame, START, end)
    files = {path.name: path.read_bytes() for path in cache.files}
    query = _Query()

    assert cache.fetch_latest(query) is None

    assert query.calls == []
    assert {path.name: path.read_bytes() for path in cache.files} == files
    assert cache.get() is not None


def test_latest_refresh_does_not_relax_explicit_range_validation(tmp_path, cache_clock):
    cache = DFCache(tmp_path)
    end = START + timedelta(days=1)
    cache.store(_frame(START, START + timedelta(minutes=2)), START, end)
    for start, stop in ((end, end), (end, START)):
        with pytest.raises(ValueError, match="Invalid arguments"):
            cache.fetch(_Query(), start, stop)
        with pytest.raises(ValueError, match="Invalid arguments"):
            cache.get(start, stop)


def test_fetch_latest_keeps_stepping_deduplication_and_query_keywords(
    tmp_path, cache_clock
):
    cache = DFCache(tmp_path)
    cutoff = START + timedelta(days=1)
    cache.store(
        _frame(cutoff - timedelta(minutes=2), cutoff - timedelta(minutes=1)),
        cutoff - timedelta(minutes=2),
        cutoff - timedelta(minutes=1),
    )
    calls = []

    def query(*, start, end, threshold):
        calls.append((start, end, threshold))
        frame = _frame(start, end)
        return pd.concat([frame, frame])

    result = cache.fetch_latest(
        query, step=timedelta(seconds=30), dedup_columns=["ts", "link"], threshold=7
    )

    assert result is not None and result.index.is_unique and len(result) == 2
    assert calls == [
        (cutoff - timedelta(minutes=1), cutoff - timedelta(seconds=30), 7),
        (cutoff - timedelta(seconds=30), cutoff, 7),
    ]


def test_fetch_latest_keeps_empty_query_handling(tmp_path, cache_clock):
    cache = DFCache(tmp_path)
    calls = []

    def query(**kwargs):
        calls.append(kwargs)

    assert cache.fetch_latest(query) is None
    assert len(calls) == 1
    assert cache.is_empty


def test_get_returns_a_cache_that_holds_one_timestamp(tmp_path):
    cache = DFCache(tmp_path)
    frame = _frame(START, START + timedelta(minutes=1))
    cache.store(frame)

    got = cache.get()

    assert got is not None
    # Parquet does not keep the index frequency.
    pd.testing.assert_frame_equal(got, frame, check_freq=False)
