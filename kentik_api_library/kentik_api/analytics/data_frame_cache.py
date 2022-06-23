import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator, List, Optional, Tuple

import pandas as pd

from kentik_api.utils.time_sequence import time_seq

from .mapped_query import MappedQueryFn

log = logging.getLogger("DFCache")


def dedup_data_frame(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Helper function for de-duplicating DataFrame on specified columns
    :param df: input DataFrame (not modified)
    :param columns: list of column names on which to deduplicate
    :return: DataFrame
    """
    out = df.reset_index()
    missing = [c for c in columns if c not in out]
    if missing:
        _m = ",".join(missing)
        raise RuntimeError(
            f"dedup_data_frame: columns '{_m}' not in input DataFrame " f"(available columns: '{out.columns}')"
        )
    out.set_index(columns, inplace=True)
    out.sort_index(inplace=True)
    duplicates = out.index.duplicated()
    if duplicates.any():
        out = out[~duplicates]
    out.reset_index(inplace=True)
    orig_index_names = [n for n in df.index.names if n is not None]
    if orig_index_names:
        out.set_index(orig_index_names, inplace=True)
    out.sort_index(inplace=True)
    return out


class DFCache:
    extension = ".parquet"
    separator = "_"
    filename_format = "{start}" + separator + "{end}" + extension

    @classmethod
    def parse_df_filename(cls, filename: Path) -> Tuple[Optional[datetime], Optional[datetime]]:
        name = filename.stem
        # Google drive replaces colons in file names with underscores during download (bad Google!)
        # We have to handle this case to make collaboration easier
        if name.count("_") == 1:
            # happy default case, 1 underscore => no mangling
            try:
                s, e = name.split(cls.separator)
            except ValueError as exc:
                log.critical("Invalid filename: %s (e: %s)", filename.name, exc)
                return None, None
            try:
                start = datetime.fromisoformat(s)
                end = datetime.fromisoformat(e)
                return start, end
            except ValueError as exc:
                log.critical("Invalid filename component %s", exc)
                return None, None
        else:
            # Assume that all colons in the original name which is composed of 2 ISO datetime strings with timezone
            # offset were replaced by underscores
            # ISO format datetime with timezone offset is always exactly 25 characters
            # So, the name must be exactly 51 characters to contain 2 valid ISO datetime strings separated by '_'
            # and the character in the middle (index 25) must be '_'
            log.debug("Got mangled name: %s", filename)
            if len(name) != 51 or name[25] != cls.separator:
                log.critical("Invalid filename: %s", filename)
                return None, None
            try:
                start = datetime.fromisoformat(name[:25].replace("_", ":"))
                end = datetime.fromisoformat(name[26:].replace("_", ":"))
                return start, end
            except ValueError as exc:
                log.critical("Invalid (mangled) filename component %s", exc)
                return None, None

    def __init__(self, directory: Path) -> None:
        self.data_dir = directory
        if not self.data_dir.exists():
            self.data_dir.mkdir()
        else:
            if not directory.is_dir():
                raise RuntimeError("{}: Path is not a directory: {}".format(self.__class__, directory))
        log.debug("data_dir: %s", self.data_dir)
        log.debug("oldest: %s newest: %s", self.oldest, self.newest)

    def __repr__(self) -> str:
        return f"DFCache: dir: {self.data_dir.resolve()}"

    @property
    def files(self) -> Generator[Path, None, None]:
        for f in sorted(self.data_dir.glob(self.filename_format.format(start="*", end="*"))):
            yield f

    @property
    def file_count(self) -> int:
        return len(list(self.files))

    @property
    def data_size(self) -> int:
        return sum(f.stat().st_size for f in self.files)

    @property
    def is_empty(self) -> bool:
        return self.file_count == 0

    @property
    def oldest(self) -> Optional[datetime]:
        match = self.filename_format.format(start="*", end="*")
        try:
            first = sorted(list(self.data_dir.glob(match)))[0]
        except IndexError:
            log.debug("No match for %s in data directory %s", match, self.data_dir)
            return None
        start, end = self.parse_df_filename(first)
        if start is None or end is None:
            log.critical("Invalid filename %s in data directory %s", first, self.data_dir)
            return None
        return start

    @property
    def newest(self) -> Optional[datetime]:
        match = self.filename_format.format(start="*", end="*")
        try:
            first = sorted(list(self.data_dir.glob(match)))[-1]
        except IndexError:
            log.debug("No match for %s in data directory %s", match, self.data_dir)
            return None
        start, end = self.parse_df_filename(first)
        if start is None or end is None:
            log.critical("Invalid filename %s in data directory %s", first, self.data_dir)
            return None
        return end

    def info(self, out=None):
        if out is None:
            out = sys.stdout
        print(f"files: {self.file_count}, total size: {self.data_size / 1000000} MB")
        print(f"oldest data: {self.oldest}", file=out)
        print(f"newest data: {self.newest}", file=out)

    def files_in_range(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        contained: bool = False,
    ) -> Generator[Path, None, None]:
        """
        Generator yielding files with data in specific time interval
        :param start - timestamp of the beginning of the interval
        :param end - timestamp of the end of the interval
        :param contained: if True yield only files with all data points in specified interval
                          if False, yield files with any data point within the interval
        """
        if start is not None and end is not None and not start < end:
            raise RuntimeError(f"Invalid arguments start {start} >= end {end}")
        if self.is_empty:
            log.debug("files_in_range: No files in data directory: %s", self.data_dir)
            return
        if start is None:
            start = self.oldest
        if end is None:
            end = self.newest
        for f in self.files:
            fs, fe = self.parse_df_filename(f)
            if fs is None or fe is None:
                continue
            if contained:
                # consider only files containing only data points in the interval
                if fs >= start and fe <= end:  # type: ignore
                    yield f
            # consider all files with any data in the specified interval
            elif fs <= end and fe > start:  # type: ignore
                yield f

    def get(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        dedup_columns: Optional[List[str]] = None,
    ) -> Optional[pd.DataFrame]:
        if self.is_empty:
            log.debug("get: cache is empty")
            return None
        if start is None:
            start = self.oldest
        if end is None:
            end = self.newest
        log.debug("get: start: %s end: %s", start, end)
        df = pd.concat([pd.read_parquet(f) for f in self.files_in_range(start, end)])
        out = pd.DataFrame(data=df.loc[(df.index >= start) & (df.index <= end)])
        if dedup_columns:
            # Deduplicate the data based on specified columns
            return dedup_data_frame(out, dedup_columns)
        else:
            return out

    def store(self, df: pd.DataFrame) -> None:
        out = self.data_dir / self.filename_format.format(start=df.index[0].isoformat(), end=df.index[-1].isoformat())
        log.debug("store: writing df (%s) to %s", " x ".join(str(_d) for _d in df.shape), out)
        df.to_parquet(out, index=True)

    def clear(self) -> None:
        log.debug("clear: all data be gone")
        self.drop(None, None)

    def drop(self, start: Optional[datetime], end: Optional[datetime]) -> None:
        log.debug("drop: start: %s end: %s", start, end)
        for f in self.files_in_range(start, end, contained=True):
            log.debug("drop: deleting %s", f.name)
            f.unlink()

    def fetch(
        self,
        query_fn: MappedQueryFn,
        start: datetime,
        end: datetime,
        step: Optional[timedelta] = None,
        dedup_columns: Optional[List[str]] = None,
        **kwargs,
    ) -> Optional[pd.DataFrame]:
        """
        Retrieve data using specified query definition and time period
        Newly retrieved data are added to the cache
        :param query_fn: function performing Kentik API query and returning DataFrame
        :param start: timestamp of the beginning of the target time period
        :param end: timestamp of the end of the target time period
        :param step: time chunks in which to retrieve new data (longer time periods result in lower time resolution)
        :param dedup_columns: list of column names used for row deduplication
        :param kwargs: addition key/value args passed to QuerySQL.from_query_definition
        :return: DataFrame containing new data
        """
        if step is None:
            log.debug("fetch: fetching from: %s to: %s", start, end)
            df = query_fn(start=start, end=end, **kwargs)
            if df is None:
                log.warning("fetch: got no data for %s -> %s", start, end)
                return None
            else:
                log.debug("fetch: got %d rows for %s -> %s", df.shape[0], start, end)
                self.store(df)
                return df
        else:
            log.debug("fetch: fetching from: %s to: %s, step: %s", start, end, step)
            last = start
            for t in time_seq(start, end, step):
                s = min(t, last)
                log.debug("fetch: fetching from: %s to: %s", s, t + step)
                df = query_fn(start=s, end=t + step, **kwargs)
                if df is None:
                    log.debug("fetch: got no data for %s -> %s", t, t + step)
                    last = t + step
                else:
                    last = df.index[-1]
                    log.debug("fetch: got %d rows for %s -> %s", df.shape[0], s, last)
                    self.store(df)
            return self.get(start, end, dedup_columns)

    def fetch_latest(
        self,
        query_fn: MappedQueryFn,
        step: Optional[timedelta] = None,
        dedup_columns: Optional[List[str]] = None,
        **kwargs,
    ) -> Optional[pd.DataFrame]:
        """
        Retrieve data using specified query definition with start time = newest in cache and end time = now
        If the cache is empty, last day of data is retrieved. More precisely 23 hours and 59 minutes of data are
        retrieved in order to get 5 minute resolution.
        Newly retrieved data are added to the cache
        :param query_fn: function performing Kentik API query and returning DataFrame
        :param step: time chunks in which to retrieve new data (longer time periods result in lower time resolution)
        :param dedup_columns: list of column names used for row deduplication
        :param kwargs: addition key/value args passed to QuerySQL.from_query_definition
        :return: DataFrame containing new data
        """
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        if self.is_empty:
            log.debug("fetch_latest: cache is empty")
            start = now - timedelta(hours=23, minutes=59)
        else:
            start = self.newest  # type: ignore
        return self.fetch(
            query_fn,
            start=start,
            end=now,
            step=step,
            dedup_columns=dedup_columns,
            **kwargs,
        )
