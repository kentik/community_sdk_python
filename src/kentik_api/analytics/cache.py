# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""A disk cache of query DataFrames by time range (1.x `DFCache`).

Files are Parquet, read with pyarrow, which cannot run code. Each file is
named `<start>_<end>.parquet`: the range `fetch` asked for, or the first and
last index time for `store(df)`. Each time is ISO 8601 with `_` in place of
`:`, which Windows does not allow in a file name. Names with `:` still read.
A file with any other name is ignored.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, TextIO, cast

import pandas as pd

from kentik_api.analytics.definitions import MappedQueryFn

log = logging.getLogger(__name__)

_FILENAME = re.compile(r"(?P<start>.+?)_(?P<end>\d{4}-\d{2}-\d{2}.*)")


def dedup_data_frame(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """A copy of `df` with one row for each value of `columns`."""
    out = df.reset_index()
    missing = [c for c in columns if c not in out]
    if missing:
        raise ValueError(
            f"dedup_data_frame: columns '{','.join(missing)}' not in the DataFrame "
            f"(available columns: '{list(out.columns)}')"
        )
    out = out.set_index(columns).sort_index()
    out = out[~out.index.duplicated()].reset_index()
    index_names = [n for n in df.index.names if n is not None]
    if index_names:
        out = out.set_index(index_names)
    return out.sort_index()


def _require_aware(*times: datetime | None) -> None:
    if any(t is not None and t.tzinfo is None for t in times):
        raise ValueError("DFCache needs timezone-aware datetimes, such as UTC")


def _as_utc(t: datetime) -> datetime:
    return t if t.tzinfo is not None else t.replace(tzinfo=UTC)


def _time_steps(start: datetime, end: datetime, step: timedelta) -> Iterator[datetime]:
    t = start
    while t < end:
        yield t
        t += step


class DFCache:
    extension = ".parquet"
    separator = "_"
    filename_format = "{start}" + separator + "{end}" + extension

    @classmethod
    def parse_df_filename(
        cls, filename: Path
    ) -> tuple[datetime | None, datetime | None]:
        match = _FILENAME.fullmatch(filename.stem)
        if match is None:
            log.debug("Ignoring a file the cache did not write: %s", filename)
            return None, None
        try:
            return (
                _as_utc(datetime.fromisoformat(match["start"].replace("_", ":"))),
                _as_utc(datetime.fromisoformat(match["end"].replace("_", ":"))),
            )
        except ValueError:
            log.debug("Ignoring a file the cache did not write: %s", filename)
            return None, None

    def __init__(self, directory: Path) -> None:
        self.data_dir = Path(directory)
        if self.data_dir.exists() and not self.data_dir.is_dir():
            raise ValueError(f"{self.__class__.__name__}: not a directory: {directory}")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        return f"DFCache: dir: {self.data_dir.resolve()}"

    def _ranges(self) -> Iterator[tuple[Path, datetime, datetime]]:
        for path in sorted(self.data_dir.glob(f"*{self.separator}*{self.extension}")):
            start, end = self.parse_df_filename(path)
            if start is not None and end is not None:
                yield path, start, end

    @property
    def files(self) -> Iterator[Path]:
        for path, _, _ in self._ranges():
            yield path

    @property
    def file_count(self) -> int:
        return sum(1 for _ in self.files)

    @property
    def data_size(self) -> int:
        return sum(f.stat().st_size for f in self.files)

    @property
    def is_empty(self) -> bool:
        return self.file_count == 0

    @property
    def oldest(self) -> datetime | None:
        return min((start for _, start, _ in self._ranges()), default=None)

    @property
    def newest(self) -> datetime | None:
        return max((end for _, _, end in self._ranges()), default=None)

    def info(self, out: TextIO | None = None) -> None:
        print(
            f"files: {self.file_count}, total size: {self.data_size / 1000000} MB",
            file=out,
        )
        print(f"oldest data: {self.oldest}", file=out)
        print(f"newest data: {self.newest}", file=out)

    def files_in_range(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
        contained: bool = False,
    ) -> Iterator[Path]:
        """Files with data in the range, or, when `contained`, only data in it."""
        _require_aware(start, end)
        if start is not None and end is not None and not start < end:
            raise ValueError(f"Invalid arguments: start {start} >= end {end}")
        start = start or self.oldest
        end = end or self.newest
        if start is None or end is None:
            return
        for path, file_start, file_end in self._ranges():
            if contained:
                if file_start >= start and file_end <= end:
                    yield path
            elif file_start <= end and file_end >= start:
                yield path

    def covers(self, start: datetime, end: datetime) -> bool:
        """True when one cached file holds the whole range."""
        _require_aware(start, end)
        return any(s <= start and e >= end for _, s, e in self._ranges())

    def get(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
        dedup_columns: list[str] | None = None,
    ) -> pd.DataFrame | None:
        _require_aware(start, end)
        if self.is_empty:
            return None
        paths = list(self.files_in_range(start, end))
        start = start or self.oldest
        end = end or self.newest
        frames = [pd.read_parquet(f) for f in paths]
        if not frames:
            return None
        df = pd.concat(frames)
        out = pd.DataFrame(data=df.loc[(df.index >= start) & (df.index <= end)])
        return dedup_data_frame(out, dedup_columns) if dedup_columns else out

    def store(
        self,
        df: pd.DataFrame,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> None:
        """Writes `df`, named by `start` and `end`, or else by its index range."""
        out = self.data_dir / self.filename_format.format(
            start=(start or cast(pd.Timestamp, df.index[0]))
            .isoformat()
            .replace(":", "_"),
            end=(end or cast(pd.Timestamp, df.index[-1])).isoformat().replace(":", "_"),
        )
        df.to_parquet(out, index=True)

    def clear(self) -> None:
        self.drop(None, None)

    def drop(self, start: datetime | None, end: datetime | None) -> None:
        for path in list(self.files_in_range(start, end, contained=True)):
            path.unlink()

    def fetch(
        self,
        query_fn: MappedQueryFn,
        start: datetime,
        end: datetime,
        step: timedelta | None = None,
        dedup_columns: list[str] | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame | None:
        """Fetches the range with `query_fn`, stores it, and returns it.

        The range is fetched in steps (one step without `step`), and a step
        that one cached file already holds is not fetched again.
        """
        _require_aware(start, end)
        if step is not None and step <= timedelta(0):
            raise ValueError(f"step must be positive, got {step}")
        step = step or end - start
        for t in _time_steps(start, end, step):
            step_end = min(t + step, end)
            if self.covers(t, step_end):
                continue
            df = query_fn(start=t, end=step_end, **kwargs)
            if df is None or df.empty:
                log.warning("fetch: got no data for %s -> %s", t, step_end)
            else:
                self.store(df, t, step_end)
        return self.get(start, end, dedup_columns)

    def fetch_latest(
        self,
        query_fn: MappedQueryFn,
        step: timedelta | None = None,
        dedup_columns: list[str] | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame | None:
        """Fetches new data, or returns None when the cache is already current."""
        now = datetime.now(UTC).replace(second=0, microsecond=0)
        start = self.newest or now - timedelta(hours=23, minutes=59)
        if start >= now:
            return None
        return self.fetch(
            query_fn,
            start=start,
            end=now,
            step=step,
            dedup_columns=dedup_columns,
            **kwargs,
        )
