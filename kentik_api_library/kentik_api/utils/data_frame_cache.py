import logging
import sys
import pandas as pd
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator, List, Optional, Tuple
from kentik_api import KentikAPI
from kentik_api.public import QuerySQL, QueryDefinition
from .time_sequence import time_seq

log = logging.getLogger('DFCache')


class DFCache:
    extension = '.parquet'
    separator = '_'
    filename_format = '{start}' + separator + '{end}' + extension

    @classmethod
    def parse_df_filename(cls, filename: Path) -> Tuple[Optional[datetime], Optional[datetime]]:
        name = filename.stem
        # Google drive replaces colons in file names with underscores during download (bad Google!)
        # We have to handle this case to make collaboration easier
        if name.count('_') == 1:
            # happy default case, 1 underscore => no mangling
            try:
                s, e = name.split(cls.separator)
            except ValueError as exc:
                log.critical('Invalid filename: %s (e: %s)', filename.name, exc)
                return None, None
            try:
                start = datetime.fromisoformat(s)
                end = datetime.fromisoformat(e)
                return start, end
            except ValueError as exc:
                log.critical('Invalid filename component %s', exc)
                return None, None
        else:
            # Assume that all colons in the original name which is composed of 2 ISO datetime strings with timezone
            # offset were replaced by underscores
            # ISO format datetime with timezone offset is always exactly 25 characters
            # So, the name must be exactly 51 characters to contain 2 valid ISO datetime strings separated by '_'
            # and the character in the middle (index 25) must be '_'
            log.debug('Got mangled name: %s', filename)
            if len(name) != 51 or name[25] != cls.separator:
                log.critical('Invalid filename: %s', filename)
                return None, None
            try:
                start = datetime.fromisoformat(name[:25].replace('_', ':'))
                end = datetime.fromisoformat(name[26:].replace('_', ':'))
                return start, end
            except ValueError as exc:
                log.critical('Invalid (mangled) filename component %s', exc)
                return None, None

    def __init__(self, directory: Path) -> None:
        self.data_dir = directory
        if not self.data_dir.exists():
            self.data_dir.mkdir()
        else:
            if not directory.is_dir():
                raise RuntimeError('{}: Path is not a directory: {}'.format(self.__class__, directory))
        log.debug('data_dir: %s', self.data_dir)
        log.debug('oldest: %s newest: %s', self.oldest, self.newest)

    def __repr__(self) -> str:
        return f'DFCache: dir: {self.data_dir.resolve()}'

    @property
    def files(self) -> Generator[Path, None, None]:
        for f in sorted(self.data_dir.glob(self.filename_format.format(start='*', end='*'))):
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
        match = self.filename_format.format(start='*', end='*')
        try:
            first = sorted(list(self.data_dir.glob(match)))[0]
        except IndexError:
            log.debug('No match for %s in data directory %s', match, self.data_dir)
            return None
        start, end = self.parse_df_filename(first)
        if start is None or end is None:
            log.critical('Invalid filename %s in data directory %s', first, self.data_dir)
            return None
        return start

    @property
    def newest(self) -> Optional[datetime]:
        match = self.filename_format.format(start='*', end='*')
        try:
            first = sorted(list(self.data_dir.glob(match)))[-1]
        except IndexError:
            log.debug('No match for %s in data directory %s', match, self.data_dir)
            return None
        start, end = self.parse_df_filename(first)
        if start is None or end is None:
            log.critical('Invalid filename %s in data directory %s', first, self.data_dir)
            return None
        return end

    def info(self, out=None):
        if out is None:
            out = sys.stdout
        print(f'files: {self.file_count}, total size: {self.data_size / 1000000} MB')
        print(f'oldest data: {self.oldest}', file=out)
        print(f'newest data: {self.newest}', file=out)

    def files_in_range(self, start: Optional[datetime] = None,
                       end: Optional[datetime] = None,
                       contained: bool = False) -> Generator[Path, None, None]:
        if start is not None and end is not None and not start < end:
            raise RuntimeError(f'Invalid arguments start {start} >= end {end}')
        if self.is_empty:
            log.debug('files_in_range: No files data directory: %s', self.data_dir)
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
                if fs >= start and fe <= end:
                    yield f
            elif fs <= end and fe > start:
                yield f

    def get(self, start: Optional[datetime] = None, end: Optional[datetime] = None,
            dedup_columns: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        if self.is_empty:
            log.debug('get: cache is empty')
            return None
        log.debug('get: start: %s end: %s', start, end)
        out = pd.concat([pd.read_parquet(f) for f in self.files_in_range(start, end)])[start:end]
        if dedup_columns:
            # Deduplicate the data based on specified columns
            # Remember current index fields
            orig_index_columns = out.index.names
            out.reset_index(inplace=True)
            missing = set(dedup_columns).difference(set(out.columns))
            if missing:
                log.warning('get: Cannot deduplicate. %s column(s) not in data', ','.join(missing))
            else:
                out.drop_duplicates(subset=dedup_columns, inplace=True)
            out.set_index(orig_index_columns, inplace=True)
        return out

    def store(self, df: pd.DataFrame) -> None:
        out = self.data_dir / self.filename_format.format(start=df.index[0].isoformat(), end=df.index[-1].isoformat())
        log.debug('store: writing df (%s) to %s', ' x '.join(str(_d) for _d in df.shape), out)
        df.to_parquet(out, index=True)

    def clear(self) -> None:
        log.debug('clear: all data be gone')
        self.drop(None, None)

    def drop(self, start: Optional[datetime], end: Optional[datetime]) -> None:
        log.debug('drop: start: %s end: %s', start, end)
        for f in self.files_in_range(start, end, contained=True):
            log.debug('drop: deleting %s', f.name)
            f.unlink()

    def fetch_latest(self, api: KentikAPI, query_def: QueryDefinition,
                     step: Optional[timedelta] = None, **kwargs) -> Optional[pd.DataFrame]:
        """
        Retrieve data using specified query definition with start time = newest in cache and end time = now
        If the cache is empty, last day of data is retrieved
        Newly retrieved data are added to the cache
        :param api: KentikAPI instance to use to fetch data
        :param query_def: query definition dictionary (see KTAPIClient.sql_to_df)
        :param step: time chunks in which to retrieve new data (longer time periods result in lower time resolution)
        :param kwargs: addition key/value args passed to KTAPIClient.sql_to_df
        :return: DataFrame containing new data
        """
        now = datetime.now(timezone.utc)
        if self.is_empty:
            log.debug('fetch_latest: cache is empty')
            start = now - timedelta(days=1)
        else:
            start = self.newest
        if step is None:
            log.debug('fetch_latest: fetching from: %s to: %s', start, now)
            query = QuerySQL.from_query_definition(query_def, start=start, end=now, **kwargs)
            df = api.query.sql(query).to_dataframe(query_def)
            if df is None:
                log.warning('fetch_latest: got no data for %s -> %s', start, now)
                return None
            else:
                log.debug('fetch_latest: got %d rows for %s -> %s', df.shape[0], start, now)
                self.store(df)
                return df
        else:
            log.debug('fetch_latest: fetching from: %s to: %s in %s steps', start, now, step)
            for t in time_seq(start, now, step):
                log.debug('fetch_latest: fetching from: %s to: %s', t, t + step)
                query = QuerySQL.from_query_definition(query_def, start=start, end=t + step, **kwargs)
                df = api.query.sql(query).to_dataframe(query_def)
                if df is None:
                    log.debug('fetch_latest: got no data for %s -> %s', t, t + step)
                else:
                    log.debug('fetch_latest: got %d rows for %s -> %s', df.shape[0], t, t + step)
                    self.store(df)
            return self.get(start, now)
