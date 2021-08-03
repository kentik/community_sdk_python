import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, TypeVar, Union

import re
import yaml
import json
from pandas import DataFrame, to_datetime

from kentik_api import KentikAPI
from kentik_api.public import QuerySQL, QuerySQLResult, QueryObject, QueryDataResult

MappedQueryFn = Callable[..., DataFrame]


TIME_SERIES_FIELDS = ("timestamp", "value", "period")
TIME_SERIES_REGEX = re.compile("__TS[.]([^.]+)[.]({})".format("|".join(TIME_SERIES_FIELDS)))


class MappingEntry:
    def __init__(self, source: str, data_type: Optional[str] = None, is_index: bool = False):
        self.source = source
        self.data_type = data_type
        self.is_index = is_index
        m = TIME_SERIES_REGEX.match(self.source)
        if m is None:
            self.time_series_name = None
            self.time_series_field = None
            self.time_series_field_idx = None
        else:
            self.time_series_name = m.group(1)
            self.time_series_field = m.group(2)
            self.time_series_field_idx = TIME_SERIES_FIELDS.index(self.time_series_field)
            if self.time_series_field_idx == 0:
                #  automatically set data_type for time series timestamps
                if self.data_type is not None:
                    logging.warning(
                        "Overriding 'data_type: %s' for time_series timestamp (source: %s)", self.data_type, self.source
                    )
                self.data_type = "unix_timestamp_millis"

    @property
    def is_time_series_key(self) -> bool:
        return self.time_series_field is not None


def apply_data_types(df: DataFrame, mapping: Generator[Tuple[str, MappingEntry], None, None]) -> None:
    """
    Apply data types specified in the mapping to the DataFrame
    :param df: DataFrame to operate on
    :param mapping: mapping dictionary
    :return: None (modified input DataFrame in place)
    """
    for k, m in mapping:
        if m.data_type is not None:
            if m.data_type == "time":
                df[k] = to_datetime(df[k])
            elif m.data_type == "unix_timestamp":
                df[k] = to_datetime(df[k], unit="s", utc=True)
            elif m.data_type == "unix_timestamp_millis":
                df[k] = to_datetime(df[k] / 1000, unit="s", utc=True)
            else:
                df[k] = df[k].astype(m.data_type)
        if m.is_index:
            df.set_index(k, inplace=True)
            df.sort_index(inplace=True)


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
            mapping[c] = MappingEntry(source=d["source"], data_type=d.get("type"), is_index=d.get("index", False))
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

    @property
    def items(self) -> Generator[Tuple[str, MappingEntry], None, None]:
        for k, v in self._entries.items():
            yield k, v

    @property
    def entries(self):
        return self._entries

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
            for k, m in mapping.items:
                data[k].append(m.source.format(**row))
    df = DataFrame.from_dict(data)
    apply_data_types(df, mapping.items)
    logging.debug("df shape: (%d, %d)", df.shape[0], df.shape[1])
    return df


DataResultMappingType = TypeVar("DataResultMappingType", bound="DataResultMapping")


class DataResultMapping:
    @classmethod
    def from_dict(cls: Type[DataResultMappingType], data: Optional[Dict] = None) -> DataResultMappingType:
        if data is None:
            raise RuntimeError("No data passed to DataResultMapping.from_dict")
        mappings: Dict[str, Dict[str, MappingEntry]] = dict()
        for m in ("aggregates", "time_series"):
            mappings[m] = dict()
            if m not in data:
                logging.debug("No %s in mapping data %s", m, data)
                continue
            for c, d in data[m].items():
                if c in mappings[m]:
                    raise RuntimeError(f"Duplicate mapping for column '{c}' in '{m}' mapping data ({data})")
                if type(d) != dict or "source" not in d.keys():
                    raise RuntimeError(f"'source' is missing in '{m}' mapping entry for column '{c}' ({data})")
                mappings[m][c] = MappingEntry(
                    source=d["source"], data_type=d.get("type"), is_index=d.get("index", False)
                )
        return cls(**mappings)

    def __init__(
        self,
        aggregates: Optional[Dict[str, MappingEntry]] = None,
        time_series: Optional[Dict[str, MappingEntry]] = None,
    ) -> None:
        self._aggregates: Dict[str, MappingEntry] = dict()
        self._time_series: Dict[str, MappingEntry] = dict()
        if aggregates:
            self._aggregates.update(aggregates)
        if time_series:
            self._time_series.update(time_series)
            # sanity check that the mapping uses any fields from `timeSeries`
            for _, m in self.time_series:
                if m.is_time_series_key:
                    break
            else:
                raise RuntimeError("'time_series' mapping must contain at least one '__TS' 'source'")

    def set_aggregates(self, key: str, value: MappingEntry) -> None:
        self._aggregates[key] = value

    def set_time_series(self, key: str, value: MappingEntry) -> None:
        self._time_series[key] = value

    def has_aggregates_column(self, column) -> bool:
        return column in self._aggregates

    def has_time_series_column(self, column) -> bool:
        return column in self._time_series

    @property
    def aggregates(self) -> Generator[Tuple[str, MappingEntry], None, None]:
        for k, v in self._aggregates.items():
            yield k, v

    @property
    def time_series(self) -> Generator[Tuple[str, MappingEntry], None, None]:
        for k, v in self._time_series.items():
            yield k, v

    @property
    def has_aggregates(self):
        return len(self._aggregates) > 0

    @property
    def has_time_series(self):
        return len(self._time_series) > 0

    @property
    def is_empty(self) -> bool:
        return not self.has_aggregates and not self.has_time_series


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
        def _expand_dict(data: Dict, parent: str) -> Dict:
            return {k: _expand(v, parent=f"{parent}.{k}") for k, v in data.items()}

        def _expand_list(data: List, parent: str) -> List:
            return [_expand(v, parent=f"{parent}[{i}]") for i, v in enumerate(data)]

        def _expand(data: Any, parent: str) -> Any:
            if type(data) == dict:
                return _expand_dict(data, parent)
            elif type(data) == list:
                return _expand_list(data, parent)
            elif type(data) == str:
                logging.debug("key: %s expanding: '%s'", f"{parent}", data)
                r = data.format(**kwargs)
                logging.debug("got: '%s'", r)
                return r
            else:
                return data

        return _expand(self.query, parent="")

    def query_object(self, **kwargs) -> QueryObject:
        """
        Produce SQL query object from template by expanding embedded str.format directives using data in kwargs
        """
        return QueryObject.from_dict(self.expand_query(**kwargs))

    def get_data(self, api: KentikAPI, **kwargs) -> List[Tuple[Optional[DataFrame], Optional[DataFrame]]]:
        result = api.query.data(self.query_object(**kwargs))
        return data_result_to_df(self.mapping, result)


def data_result_to_df(
    mapping: DataResultMapping, data: QueryDataResult
) -> List[Tuple[Optional[DataFrame], Optional[DataFrame]]]:
    """
    Map KDE API data query result to Pandas DataFrames. A Tuple of two DataFrames is created for each result returned.
    In each tuple the first entry contains DataFrame for aggregates mapping, if present in mapping data, otherwise None.
    The second entry contains DataFrame for time_series mapping, if present in the mapping data, otherwise None.
    """
    if len(data.results) < 1:
        logging.debug("No data in query result")
        return [(None, None)]
    if mapping.is_empty:
        logging.error("Empty mapping")
        raise RuntimeError("Mapping is required to transform data query results to DataFrames")
    out = list()
    for i, r in enumerate(data.results):
        aggregates = None
        time_series = None
        if mapping.has_aggregates:
            out_data = dict()
            for c, m in mapping.aggregates:
                out_data[c] = [m.source.format(bucket=r["bucket"], **e) for e in r["data"]]
            aggregates = DataFrame.from_dict(out_data)
            apply_data_types(aggregates, mapping.aggregates)
        if mapping.has_time_series:
            # check that all data entries in the result have `timeSeries` key
            missing = [e["key"] for e in r["data"] if "timeSeries" not in e or not e["timeSeries"]]
            if missing:
                logging.warning("%d data entries do not contain time series and will be ignored", len(missing))
            if len(r["data"]) > 1:
                # if there is more than one `data` entry, time_series mapping must contain at least one non-time series
                # column to make rows unique
                for _, m in mapping.time_series:
                    if not m.is_time_series_key:
                        break
                else:
                    raise RuntimeError(
                        "More than 1 data item in result,"
                        "'time_series' mapping must contain at least one non '__TS' 'source'"
                    )
            out_data = {k: list() for k, _ in mapping.time_series}
            for e in r["data"]:
                if e["key"] in missing:
                    logging.debug("no time series in entry: %s", e)
                    continue
                # check that all time_series names are present
                missing_ts = [
                    n
                    for n in [m.time_series_name for _, m in mapping.time_series if m.is_time_series_key]
                    if n not in e["timeSeries"]
                ]
                if missing_ts:
                    raise RuntimeError(
                        "No 'timeSeries' for variables(s) '{mts}' in entry '{e}'".format(
                            mts=",".join([str(x) for x in missing_ts]), e=e
                        )
                    )
                ts_len = max(
                    [
                        len(e["timeSeries"][m.time_series_name]["flow"])
                        for _, m in mapping.time_series
                        if m.is_time_series_key
                    ]
                )
                for k, m in mapping.time_series:
                    if m.is_time_series_key:
                        out_data[k].extend(
                            row[m.time_series_field_idx] for row in e["timeSeries"][m.time_series_name]["flow"]
                        )
                    else:
                        val = m.source.format(bucket=r["bucket"], **e)
                        out_data[k].extend([val] * ts_len)
            time_series = DataFrame.from_dict(out_data)
            apply_data_types(time_series, mapping.time_series)
            #  FINISH MAPPING OF TIME SERIES DATA
        if aggregates is not None:
            logging.debug("result[%d]: aggregates shape: (%d, %d)", i, aggregates.shape[0], aggregates.shape[1])
        else:
            logging.debug("result[%d]: no aggregates", i)
        if time_series is not None:
            logging.debug("result[%d]: time_series shape: (%d, %d)", i, time_series.shape[0], time_series.shape[1])
        else:
            logging.debug("result[%d]: no time_series", i)
        out.append((aggregates, time_series))
    return out
