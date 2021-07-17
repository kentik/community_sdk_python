import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, TypeVar, Union

import yaml
import json
from pandas import DataFrame, to_datetime

from kentik_api import KentikAPI
from kentik_api.public import QuerySQL, QuerySQLResult, QueryObject, QueryDataResult

MappedQueryFn = Callable[..., Union[DataFrame, Dict[str, DataFrame]]]


@dataclass
class MappingEntry:
    format: str
    data_type: Optional[str]
    is_index: bool = False


SQLResultMappingType = TypeVar("SQLResultMappingType", bound="SQLResultMapping")


class SQLResultMapping:
    @classmethod
    def from_dict(cls: Type[SQLResultMappingType], data: Optional[Dict] = None) -> SQLResultMappingType:
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
        elif m.data_type == "unix_timestamp":
            df[k] = to_datetime(df[k], unit="s", utc=True)
        else:
            df[k] = df[k].astype(m.data_type)
        if m.is_index:
            df.set_index(k, inplace=True)
            df.sort_index(inplace=True)
    logging.debug("df shape: (%d, %d)", df.shape[0], df.shape[1])
    return df


DataResultMappingType = TypeVar("DataResultMappingType", bound="DataResultMapping")


class DataResultMapping:
    @classmethod
    def from_dict(cls: Type[DataResultMappingType], data: Optional[Dict] = None) -> DataResultMappingType:
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


class DataQueryDefinition:
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
        return cls(query=qd["query"], mapping=DataResultMapping.from_dict(qd.get("mapping")))

    def __init__(self, query: Union[str, Dict], mapping: DataResultMapping) -> None:
        if type(query) == str:
            self.query = json.loads(query)
        else:
            self.query = query
        self.mapping = mapping

    def expand_query(self, **kwargs) -> Dict:
        def _expand_dict(data: Dict, parent: str, **kwargs) -> Dict:
            return {k: _expand(v, parent=f"{parent}.{k}", **kwargs) for k, v in data.items()}

        def _expand_list(data: List, parent: str , **kwargs) -> List:
            return [_expand(v, parent=f"{parent}[{i}]", **kwargs) for i, v in enumerate(data)]

        def _expand(data: Any, parent: str, **kwargs) -> Any:
            if type(data) == dict:
                return _expand_dict(data, parent, **kwargs)
            elif type(data) == list:
                return _expand_list(data, parent, **kwargs)
            elif type(data) == str:
                logging.debug("key: %s expanding: '%s'", f"{parent}", data)
                r = data.format(**kwargs)
                logging.debug("got: '%s'", r)
                return r
            else:
                return data
        return _expand(self.query, parent="", **kwargs)

    def query_object(self, **kwargs) -> QueryObject:
        """
        Produce SQL query object from template by expanding embedded str.format directives using data in kwargs
        """
        return QueryObject.from_dict(self.expand_query(**kwargs))

    def get_data(self, api: KentikAPI, **kwargs) -> Dict[str, DataFrame]:
        result = api.query.data(self.query_object(**kwargs))
        return data_result_to_df(self.mapping, result)

    def make_query_fn(self, api: KentikAPI) -> MappedQueryFn:
        """
        Create a function returning DataFrame based on the query definition
        The main purpose is to pass the function to the DFCache.fetch method
        """

        def data_mapped_query(**kwargs) -> Dict[str, DataFrame]:
            return self.get_data(api, **kwargs)

        return data_mapped_query


def data_result_to_df(mapping: DataResultMapping, data: QueryDataResult) -> Dict[str, DataFrame]:
    """
    Map KDE SQL query result to Pandas DataFrame
    If no mapping is provided in query definition, every column in response row is included as DataFrame columns
    otherwise data are mapped to DataFrame based on mapping entries
    """
    if len(data.results) < 1:
        logging.debug("No data in query result")
        return None
    if mapping.is_empty:
        logging.error("Empty mapping")
        raise RuntimeError("Mapping is required to transform data query results to DataFrames")
    out = dict()
    for r in data.results:
        raise RuntimeError("Code is not finished")

    # INSERT DATA MAPPING

        columns = defaultdict(list)
        df = DataFrame.from_dict(data)
        apply_data_types(df, mapping)
        logging.debug("df shape: (%d, %d)", df.shape[0], df.shape[1])
        out[r.bucket] = df
    return out

