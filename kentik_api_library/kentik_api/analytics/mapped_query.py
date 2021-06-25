import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, Generator, Optional, Tuple, Type, TypeVar

import yaml
from pandas import DataFrame, to_datetime  # type: ignore

from kentik_api import KentikAPI  # type: ignore
from kentik_api.public import QuerySQL, QuerySQLResult  # type: ignore

MappedQueryFn = Callable[..., DataFrame]


@dataclass
class MappingEntry:
    format: str
    data_type: Optional[str]
    is_index: bool = False


T = TypeVar("T", bound="SQLResultMapping")


class SQLResultMapping:
    @classmethod
    def from_dict(cls: Type[T], data: Optional[Dict] = None) -> T:
        mapping = cls()
        if data is None:
            return mapping
        for c, d in data.items():
            if mapping.has(c):
                raise RuntimeError(f"Duplicate mapping for column '{c}' in query definition ({data})")
            if type(d) != dict or "source" not in d.keys():
                raise RuntimeError(f"'source' is missing in query definition entry for column {c} ({data})")
            mapping[c] = MappingEntry(format=d["source"], data_type=d.get("type"), is_index=d.get("index", False))
        return mapping

    def __init__(self, entries: Optional[Dict[str, MappingEntry]] = None) -> None:
        self._entries: Dict[str, MappingEntry] = dict()
        if entries:
            self._entries.update(entries)

    def __getitem__(self, column):
        return self._entries.get(column)

    def __setitem__(self, key: str, value: MappingEntry) -> None:
        self._entries[key] = value

    def has(self, column) -> bool:
        return column in self._entries

    def items(self) -> Generator[Tuple[str, MappingEntry], None, None]:
        for k, v in self._entries.items():
            yield k, v

    @property
    def is_empty(self) -> bool:
        return len(self._entries) == 0


@dataclass
class SQLQueryDefinition:
    query: str
    mapping: SQLResultMapping

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            qd = yaml.load(f, yaml.SafeLoader)
        logging.debug("Loading query definition: %s from %s", qd, filename)
        return cls.from_dict(qd)

    @classmethod
    def from_dict(cls, qd: dict):
        if "query" not in qd:
            raise RuntimeError(f"No query template in query definition: {qd}")
        return cls(query=qd["query"], mapping=SQLResultMapping.from_dict(qd.get("mapping")))

    def to_sql(self, **kwargs) -> QuerySQL:
        """
        Produce SQL query object from template by expanding embedded str.format directives using data in kwargs
        """
        return QuerySQL(self.query.format(**kwargs))

    def get_data(self, api: KentikAPI, **kwargs) -> DataFrame:
        result = api.query.sql(self.to_sql(**kwargs))
        return sql_result_to_df(self.mapping, result)

    def make_query_fn(self, api: KentikAPI) -> MappedQueryFn:
        """
        Create a function returning DataFrame based on the query definition
        The main purpose is to pass the function to the DFCache.fetch method
        """

        def sql_mapped_query(**kwargs) -> DataFrame:
            return self.get_data(api, **kwargs)

        return sql_mapped_query


def sql_result_to_df(mapping: SQLResultMapping, sql_data: QuerySQLResult) -> Optional[DataFrame]:
    """
    Map KDE SQL query result to Pandas DataFrame
    If no mapping is provided in query definition, every column in response row is included as DataFrame columns
    otherwise data are mapped to DataFrame based on mapping entries
    """
    if len(sql_data.rows) < 1:
        logging.debug("No data in SQL result")
        return None
    data = defaultdict(list)
    for row in sql_data.rows:
        if mapping.is_empty:
            for k, v in row:
                data[k].append(v)
        else:
            for k, m in mapping.items():
                data[k].append(m.format.format(**row))
    df = DataFrame.from_dict(data)
    for k, m in mapping.items():
        if m.data_type is None:
            continue
        if m.data_type == "time":
            df[k] = to_datetime(df[k])
        else:
            df[k] = df[k].astype(m.data_type)
        if m.is_index:
            df.set_index(k, inplace=True)
            df.sort_index(inplace=True)
    logging.debug("df shape: (%d, %d)", df.shape[0], df.shape[1])
    return df
