# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Saved top-X query definitions that return pandas DataFrames.

Ported from 1.x `kentik_api.analytics.mapped_query`. Two 1.x features are
gone: SQL definitions (Kentik retired the SQL endpoint on 2025-05-01) and the
`@fixup:` column type, which ran Python code from the definition file.
"""

from __future__ import annotations

import json
import logging
import os
import re
import string
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any

import yaml
from pandas import DataFrame, to_datetime

from kentik_api.gen.v5.models import QueryRequest

if TYPE_CHECKING:
    from kentik_api.client import KentikAPI

log = logging.getLogger(__name__)

MappedQueryFn = Callable[..., DataFrame | None]


class _PlainNameFormatter(string.Formatter):
    # `{start.__class__}` or `{x[0]}` would read into the values passed in.
    def get_field(self, field_name: str, args: Any, kwargs: Any) -> Any:
        if not field_name.isidentifier():
            raise ValueError(
                f"Query template placeholder '{{{field_name}}}' must be a plain name"
            )
        return super().get_field(field_name, args, kwargs)


_FORMATTER = _PlainNameFormatter()

TIME_SERIES_PREFIX = "@TS"
TIME_SERIES_FIELDS = ("timestamp", "value", "period")
TIME_SERIES_REGEX = re.compile(
    rf"{TIME_SERIES_PREFIX}[.]([^.]+)[.]({'|'.join(TIME_SERIES_FIELDS)})"
)

_SQL_RETIRED = (
    "Kentik retired the V5 SQL query endpoint on 2025-05-01. "
    "Use a top-X definition (DataQueryDefinition) instead."
)
_FIXUP_REMOVED = (
    "The '@fixup:' column type ran Python code from the query definition, so it "
    "is removed. Use 'source' to build the column, 'type' to convert it, or "
    "change the DataFrame in your own code after get_data()."
)


class MappingEntry:
    """How to build one DataFrame column from a result row.

    `source` is a `str.format` template over the row's fields, or
    `@TS.<series>.<timestamp|value|period>` for a time series value. `data_type`
    is a pandas dtype, or `time`, `unix_timestamp`, or `unix_timestamp_millis`.
    """

    def __init__(
        self, source: str, data_type: str | None = None, is_index: bool = False
    ):
        if data_type is not None and data_type.startswith("@fixup:"):
            raise ValueError(_FIXUP_REMOVED)
        self.source = source
        self.data_type = data_type
        self.is_index = is_index
        match = TIME_SERIES_REGEX.match(source)
        if match is None:
            self.time_series_name: str | None = None
            self.time_series_field: str | None = None
            self.time_series_field_idx: int | None = None
        else:
            self.time_series_name = match.group(1)
            self.time_series_field = match.group(2)
            self.time_series_field_idx = TIME_SERIES_FIELDS.index(
                self.time_series_field
            )
            if self.time_series_field_idx == 0:
                if self.data_type is not None:
                    log.warning(
                        "Overriding 'data_type: %s' for time series timestamp (source: %s)",
                        self.data_type,
                        source,
                    )
                self.data_type = "unix_timestamp_millis"

    @property
    def is_time_series_key(self) -> bool:
        return self.time_series_field is not None


def set_data_types_and_index(
    df: DataFrame, mapping: Iterator[tuple[str, MappingEntry]]
) -> DataFrame:
    """Returns `df` with the mapping's data types and index applied."""
    index_columns = []
    for column, entry in mapping:
        if column not in df:
            log.debug(
                "mapping column %s not in DataFrame (columns: %s)",
                column,
                ",".join(df.columns),
            )
            continue
        if entry.data_type == "time":
            df[column] = to_datetime(df[column])
        elif entry.data_type == "unix_timestamp":
            df[column] = to_datetime(df[column], unit="s", utc=True)
        elif entry.data_type == "unix_timestamp_millis":
            df[column] = to_datetime(df[column] / 1000, unit="s", utc=True)
        elif entry.data_type is not None:
            df[column] = df[column].astype(entry.data_type)
        if entry.is_index:
            index_columns.append(column)
    if index_columns:
        df = df.set_index(index_columns).sort_index()
    return df


class ResultMapping:
    """The column mapping of one result bucket, keyed by DataFrame column name."""

    @classmethod
    def from_dict(cls, data: dict | None = None) -> ResultMapping:
        if data is None:
            return cls()
        mapping: dict[str, MappingEntry] = {}
        for column, entry in data.items():
            if not isinstance(entry, dict) or "source" not in entry:
                raise ValueError(
                    f"'source' is missing in the mapping of column {column} ({data})"
                )
            mapping[column] = MappingEntry(
                source=entry["source"],
                data_type=entry.get("type"),
                is_index=entry.get("index", False),
            )
        return cls(entries=mapping)

    def __init__(self, entries: dict[str, MappingEntry] | None = None) -> None:
        self._entries: dict[str, MappingEntry] = dict(entries or {})

    def __getitem__(self, column: str) -> MappingEntry | None:
        return self._entries.get(column)

    def has(self, column: str) -> bool:
        return column in self._entries

    @property
    def has_aggregate_keys(self) -> bool:
        return any(not e.is_time_series_key for e in self._entries.values())

    @property
    def has_time_series_keys(self) -> bool:
        return any(e.is_time_series_key for e in self._entries.values())

    @property
    def items(self) -> Iterator[tuple[str, MappingEntry]]:
        yield from self._entries.items()

    @property
    def entries(self) -> Iterator[MappingEntry]:
        yield from self._entries.values()

    @property
    def is_empty(self) -> bool:
        return not self._entries


class SQLQueryDefinition:
    """Kept so that loading a 1.x SQL definition fails with a clear reason."""

    @classmethod
    def from_file(cls, filename: str | os.PathLike[str]) -> SQLQueryDefinition:
        raise ValueError(_SQL_RETIRED)

    @classmethod
    def from_dict(cls, qd: dict) -> SQLQueryDefinition:
        raise ValueError(_SQL_RETIRED)


class DataQueryDefinition:
    """A top-X query template with a column mapping for each result bucket.

    The query is a dict or JSON text. Its strings may hold `str.format`
    placeholders, such as `{start}` and `{end}`, filled at run time. A
    definition file is read with `yaml.safe_load`.
    """

    @classmethod
    def from_file(cls, filename: str | os.PathLike[str]) -> DataQueryDefinition:
        with open(filename, encoding="utf-8") as f:
            return cls.from_dict(yaml.safe_load(f))

    @classmethod
    def from_dict(cls, qd: dict) -> DataQueryDefinition:
        if "query" not in qd:
            raise ValueError(f"No query template in query definition: {qd}")
        if isinstance(qd["query"], str) and not qd["query"].lstrip().startswith("{"):
            raise ValueError(_SQL_RETIRED)
        if "mappings" not in qd:
            raise ValueError(f"No 'mappings' in query definition: {qd}")
        mappings = {k: ResultMapping.from_dict(d) for k, d in qd["mappings"].items()}
        if not mappings:
            raise ValueError(f"No valid 'mappings' in query definition: {qd}")
        return cls(query=qd["query"], mappings=mappings)

    def __init__(self, query: str | dict, mappings: dict[str, ResultMapping]) -> None:
        self.query = json.loads(query) if isinstance(query, str) else query
        self.mappings = mappings

    def expand_query(self, **kwargs: Any) -> dict:
        """The query with every string's placeholders filled from `kwargs`."""

        def _expand(data: Any) -> Any:
            if isinstance(data, dict):
                return {k: _expand(v) for k, v in data.items()}
            if isinstance(data, list):
                return [_expand(v) for v in data]
            if isinstance(data, str):
                try:
                    return _FORMATTER.vformat(data, (), kwargs)
                except KeyError as exc:
                    raise ValueError(
                        f"No value for query template parameter(s) "
                        f"'{','.join(map(str, exc.args))}' (given: '{','.join(kwargs)}')"
                    ) from None
            return data

        return _expand(self.query)

    def query_request(self, **kwargs: Any) -> QueryRequest:
        return QueryRequest.model_validate(self.expand_query(**kwargs))

    def get_data(self, client: KentikAPI, **kwargs: Any) -> dict[str, DataFrame]:
        response = client.v5.top_x_data(data=self.query_request(**kwargs))
        results = response.model_dump(mode="json", by_alias=True, exclude_none=True)
        return data_result_to_df(self.mappings, results.get("results", []))

    def make_query_fn(self, client: KentikAPI, result_bucket: str) -> MappedQueryFn:
        """A function returning one bucket's DataFrame, for `DFCache.fetch`."""

        def data_mapped_query(**kwargs: Any) -> DataFrame | None:
            return self.get_data(client, **kwargs).get(result_bucket)

        return data_mapped_query


def data_result_to_df(
    mappings: dict[str, ResultMapping], results: list[dict]
) -> dict[str, DataFrame]:
    """Maps top-X result buckets to DataFrames, one for each bucket.

    A bucket uses the mapping with its name, else the `all` mapping. With
    `@TS` columns, each row of a bucket gives one row per time series point, and
    its other columns repeat on each of them.
    """
    out: dict[str, DataFrame] = {}
    for i, result in enumerate(results):
        mapping = mappings.get(result["bucket"], mappings.get("all"))
        if mapping is None or mapping.is_empty:
            log.critical(
                "No mapping for result[%d] bucket: %s. Result ignored",
                i,
                result["bucket"],
            )
            continue
        label = result["bucket"]
        n = 0
        while label in out:
            n += 1
            label = f"{result['bucket']}_{n}"
        rows = result.get("data", [])
        out_data: dict[str, list[Any]] = {}
        if mapping.has_time_series_keys:
            out_data = _time_series_columns(i, label, mapping, rows)
        else:
            for column, entry in mapping.items:
                try:
                    out_data[column] = [entry.source.format(**row) for row in rows]
                except KeyError as exc:
                    _log_missing(i, label, column, entry, exc, rows)
        out[label] = DataFrame.from_dict(out_data)
        out[label] = set_data_types_and_index(out[label], mapping.items)
    return out


def _time_series_columns(
    i: int, label: str, mapping: ResultMapping, rows: list[dict]
) -> dict[str, list[Any]]:
    missing = [row["key"] for row in rows if not row.get("timeSeries")]
    if missing:
        log.critical(
            "result[%s]: label: %s: %d rows have no time series and are ignored",
            i,
            label,
            len(missing),
        )
    if len(rows) > 1 and not mapping.has_aggregate_keys:
        raise ValueError(
            f"result[{i}]: label: {label}: more than 1 row in the result, so the "
            f"mapping needs at least one column not sourced from '{TIME_SERIES_PREFIX}'"
        )
    out_data: dict[str, list[Any]] = {column: [] for column, _ in mapping.items}
    series_names = [e.time_series_name for e in mapping.entries if e.is_time_series_key]
    for row in rows:
        if row["key"] in missing:
            continue
        absent = [name for name in series_names if name not in row["timeSeries"]]
        if absent:
            raise ValueError(
                f"result[{i}]: label: {label}: no time series for '{','.join(map(str, absent))}' "
                f"(available: '{','.join(row['timeSeries'])}')"
            )
        lengths = {len(row["timeSeries"][name]["flow"]) for name in series_names}
        if len(lengths) > 1:
            raise ValueError(
                f"result[{i}]: label: {label}: time series lengths differ ({lengths})"
            )
        length = max(lengths)
        for column, entry in mapping.items:
            if entry.is_time_series_key:
                assert entry.time_series_name is not None
                assert entry.time_series_field_idx is not None
                out_data[column].extend(
                    point[entry.time_series_field_idx]
                    for point in row["timeSeries"][entry.time_series_name]["flow"]
                )
            else:
                try:
                    out_data[column].extend([entry.source.format(**row)] * length)
                except KeyError as exc:
                    _log_missing(i, label, column, entry, exc, rows)
                    out_data[column].extend([None] * length)
    return out_data


def _log_missing(
    i: int,
    label: str,
    column: str,
    entry: MappingEntry,
    exc: KeyError,
    rows: list[dict],
) -> None:
    log.critical(
        "result[%d]: label: %s: mapping for column '%s' ('%s') needs fields '%s' "
        "that the data does not have (available fields: %s)",
        i,
        label,
        column,
        entry.source,
        ",".join(str(x) for x in exc.args),
        ",".join(rows[0].keys()) if rows else "",
    )
