import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Type, TypeVar, Union

import yaml
from pandas import DataFrame, to_datetime

from kentik_api import KentikAPI
from kentik_api.public import QueryDataResult, QueryObject, QuerySQL, QuerySQLResult

MappedQueryFn = Callable[..., DataFrame]


TIME_SERIES_PREFIX = "@TS"
TIME_SERIES_FIELDS = ("timestamp", "value", "period")
TIME_SERIES_REGEX = re.compile(
    "{prefix}[.]([^.]+)[.]({fields})".format(prefix=TIME_SERIES_PREFIX, fields="|".join(TIME_SERIES_FIELDS))
)


class MappingEntry:
    """
    Class describing single mapping entry for construction of a DataFrame from KDE API 'sql' or 'topXdata' result.
    Attributes:
        'source': string containing 'str.format' formatting string for extracting specific result data field. Special
                  directives, prefixed with @TS allow to extract data from 'topXdata' result 'timeSeries' blocks
        'data_type': optional string containing desired data type for column values. Any numpy.dtype and Python
                  type name is accepted. In addition to that, following special type strings are provided:
                  'time': converts string to pandas.datetime object
                  'unix_timestamp': converts integer Unix epoch timestamp to pandas.datetime object
                  'unix_timestamp_millis': converts integer Unix epoch millisecond timestamp to pandas.datetime object
                  '@fixup<python lambda>': allows to apply <python lambda> to every value in the columns. Example:
                         '@fixup: lambda x: x.split(".")[0]' results in calling
                          DataFrame.transform(lambda x: x.split(".")[0] for all values in the column

        'is_index': boolean indicating whether columns should be used as index for resulting DataFrame
    """

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
                        "Overriding 'data_type: %s' for time_series timestamp (source: %s)",
                        self.data_type,
                        self.source,
                    )
                self.data_type = "unix_timestamp_millis"

    @property
    def is_time_series_key(self) -> bool:
        return self.time_series_field is not None


def set_data_types_and_index(df: DataFrame, mapping: Generator[Tuple[str, MappingEntry], None, None]) -> None:
    """
    Apply data types and indexing of DataFrame according to mapping
    :param df: DataFrame to operate on
    :param mapping: mapping dictionary
    :return: None (modified input DataFrame in place)
    """
    index_columns = list()
    for k, m in mapping:
        if k not in df:
            logging.debug(
                "mapping column %s not in DataFrames (columns: %s)",
                k,
                ",".join(df.columns),
            )
            continue
        if m.data_type is not None:
            if m.data_type == "time":
                df[k] = to_datetime(df[k])
            elif m.data_type == "unix_timestamp":
                df[k] = to_datetime(df[k], unit="s", utc=True)
            elif m.data_type == "unix_timestamp_millis":
                df[k] = to_datetime(df[k] / 1000, unit="s", utc=True)
            elif m.data_type.startswith("@fixup:"):
                try:
                    fn = eval(m.data_type.split("@fixup:")[1])
                except SyntaxError:
                    raise RuntimeError(f"Syntax error in '@fixup:' directive ({m.data_type}) for column {k}")
                df[k] = df[k].transform(fn)
            else:
                df[k] = df[k].astype(m.data_type)
        if m.is_index:
            index_columns.append(k)
    if index_columns:
        df.set_index(index_columns, inplace=True)
        df.sort_index(inplace=True)


ResultMappingType = TypeVar("ResultMappingType", bound="ResultMapping")


class ResultMapping:
    """
    Collection of data mapping entries used for construction of DataFrames based on KDE API 'sql' or 'topXdata' query
    results.

    ResultMapping instance is basically dictionary on MappingEntries keyed by DataFrame column names.
    """

    @classmethod
    def from_dict(cls: Type[ResultMappingType], data: Optional[Dict] = None) -> ResultMappingType:
        mapping: Dict[str, MappingEntry] = dict()
        if data is None:
            return cls()
        for c, d in data.items():
            if c in mapping:
                raise RuntimeError(f"Duplicate mapping for column '{c}' in query definition ({data})")
            if type(d) != dict or "source" not in d.keys():
                raise RuntimeError(f"'source' is missing in query definition entry for column {c} ({data})")
            mapping[c] = MappingEntry(
                source=d["source"],
                data_type=d.get("type"),
                is_index=d.get("index", False),
            )
        return cls(entries=mapping)

    def __init__(self, entries: Optional[Dict[str, MappingEntry]] = None) -> None:
        self._entries: Dict[str, MappingEntry] = dict()
        if entries:
            self._entries.update(entries)

    def __getitem__(self, column):
        return self._entries.get(column)

    def has(self, column) -> bool:
        return column in self._entries

    @property
    def has_aggregate_keys(self):
        return any(e for e in self._entries.values() if not e.is_time_series_key)

    @property
    def has_time_series_keys(self):
        return any(e for e in self._entries.values() if e.is_time_series_key)

    @property
    def items(self) -> Generator[Tuple[str, MappingEntry], None, None]:
        for k, v in self._entries.items():
            yield k, v

    @property
    def entries(self):
        for e in self._entries.values():
            yield e

    @property
    def is_empty(self) -> bool:
        return len(self._entries) == 0


@dataclass
class SQLQueryDefinition:
    """
    Class describing KDE API 'sql' query template and associated mapping allowing to transform result to
    pandas DataFrame.

    Query template is a string containing KDE SQL query with optional 'str.format'
    style directives allowing to interpolate query attributes based on a dictionary of attributes provided at runtime.
    """

    query: str
    mapping: ResultMapping

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
        return cls(query=qd["query"], mapping=ResultMapping.from_dict(qd.get("mapping")))

    def to_sql(self, **kwargs) -> QuerySQL:
        """
        Produce SQL query object from template by expanding embedded str.format directives using data in kwargs
        """
        try:
            q = self.query.format(**kwargs)
        except KeyError as ex:
            _s = ",".join(ex.args)
            _p = ",".join(kwargs.keys())
            raise RuntimeError(
                f"No values provided for query template parameters '{_s}' (template: {self.query}, "
                f"provided parameters: '{_p}'"
            )
        return QuerySQL(q)

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


def sql_result_to_df(mapping: ResultMapping, sql_data: QuerySQLResult) -> Optional[DataFrame]:
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
                try:
                    data[k].append(m.source.format(**row))
                except KeyError as ex:
                    logging.critical(
                        "mapping for column '%s' ('%s') cannot be satisfied, fields '%s' not present in data "
                        "(available fields: %s)",
                        k,
                        m.source,
                        ",".join([str(x) for x in ex.args]),
                        ",".join(row.keys()),
                    )
    df = DataFrame.from_dict(data)
    set_data_types_and_index(df, mapping.items)
    logging.debug("df shape: (%d, %d)", df.shape[0], df.shape[1])
    return df


class DataQueryDefinition:
    """
    Class describing KDE API 'topXdata' data query template and associated set of mappings allowing to transform results
    into pandas DataFrames.

    Query template can be provided either as a JSON string of equivalent dictionary. It may contain 'str.format'
    style directives allowing to interpolate query attributes based on a dictionary of attributes provided at runtime.

    Set of mappings keyed by query/result 'bucket' attribute value allow to define construction of values for colums
    of resulting DataFrame based on data in response.
    """

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
        if "mappings" not in qd:
            raise RuntimeError(f"No 'mapping' query definition: {qd}")
        mappings = {k: ResultMapping.from_dict(d) for k, d in qd["mappings"].items()}
        if len(mappings) < 1:
            raise RuntimeError(f"No valid 'mapping' query definition: {qd}")
        return cls(query=qd["query"], mappings=mappings)

    def __init__(self, query: Union[str, Dict], mappings: Dict[str, ResultMapping]) -> None:
        if type(query) == str:
            self.query = json.loads(query)
        else:
            self.query = query
        self.mappings = mappings

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
                try:
                    r = data.format(**kwargs)
                except KeyError as ex:
                    _s = ",".join(ex.args)
                    _p = ",".join(kwargs.keys())
                    raise RuntimeError(
                        f"No values provided for query template parameters '{_s}' (template: {self.query}, "
                        f"provided parameters: '{_p}'"
                    )
                return r
            else:
                return data

        return _expand(self.query, parent="")

    def query_object(self, **kwargs) -> QueryObject:
        """
        Produce data query object from template by expanding embedded str.format directives using data in kwargs
        """
        return QueryObject.from_dict(self.expand_query(**kwargs))

    def get_data(self, api: KentikAPI, **kwargs) -> Dict[str, DataFrame]:
        result = api.query.data(self.query_object(**kwargs))
        return data_result_to_df(self.mappings, result)

    def make_query_fn(self, api: KentikAPI, result_bucket: str) -> MappedQueryFn:
        """
        Create a function returning DataFrame based on the query definition. It allows to extract only 1 DataFrame
        from all responses.
        The main purpose is to pass the function to the DFCache.fetch method
        """

        def data_mapped_query(**kwargs) -> DataFrame:
            return self.get_data(api, **kwargs).get(result_bucket)

        return data_mapped_query


def data_result_to_df(mappings: Dict[str, ResultMapping], data: QueryDataResult) -> Dict[str, DataFrame]:
    """
    Map KDE API 'topXdata' query result to Pandas DataFrames based on result mappings.

    Mapping sets (ResultMapping objects) are matched to result entries based on value of 'bucket' attribute. If no match
    for is found in the 'mappings' dictionary, an entry with key 'all' is used, if present, otherwise error is logged
    and result entry is ignored.

    If ResultMapping for an result entry contains columns sourced from 'timeSeries' data (i.e. source specification
    starting with '@TS'), number of rows in the resulting DataFrame is equal to number of result data entries times
    lengths of 'timeSeries' data. Non 'timeSeries' data are replicated for each timestamp in the time series.

    If no @TS sourced columns are present in the mapping, number of rows in the resulting DataFrame is equal to number
    of result 'data' entries.

    :param mappings: Dictionary keyed by result 'bucket' containing ResultMapping objects
    :param data: QueryDataResult containing response data
    :return: Dictionary keyed by result 'bucket' containing DataFrame for each results entry
    """
    if len(data.results) < 1:
        logging.debug("No data in query result")
        return dict()
    out: Dict[str, DataFrame] = dict()
    for i, r in enumerate(data.results):
        mapping = mappings.get(r["bucket"], mappings.get("all"))
        if mapping is None or mapping.is_empty:
            logging.critical(
                "No applicable mapping for result[%d] bucket: %s. Result ignored",
                i,
                r["bucket"],
            )
            continue
        result_label = r["bucket"]
        if result_label in out:
            n = 0
            while result_label in out:
                n += 1
                result_label = f"{result_label}_{n}"
            logging.warning("Duplicate bucket name: %s (using: '%s')", r["bucket"], result_label)
        out_data: Dict[str, List[Any]] = dict()
        if mapping.has_time_series_keys:
            # check that all data entries in the result have `timeSeries` key
            missing = [e["key"] for e in r["data"] if "timeSeries" not in e or not e["timeSeries"]]
            if missing:
                logging.critical(
                    "result[%s]: label: %s: %d data entries do not contain time series and will be ignored",
                    i,
                    result_label,
                    len(missing),
                )
            if len(r["data"]) > 1 and not mapping.has_aggregate_keys:
                # if there is more than one `data` entry, time_series mapping must contain at least one non-time series
                # column to make rows unique
                raise RuntimeError(
                    f"result[{i}]: label: {result_label}: More than 1 data item in result,"
                    f"'time_series' mapping must contain at least one non-'{TIME_SERIES_PREFIX}' 'source'"
                )
            out_data = {k: list() for k, _ in mapping.items}
            for e in r["data"]:
                if e["key"] in missing:
                    logging.debug("no time series in entry: %s", e)
                    continue
                # check that all time_series names are present
                missing_ts = [
                    n
                    for n in [m.time_series_name for m in mapping.entries if m.is_time_series_key]
                    if n not in e["timeSeries"]
                ]
                if missing_ts:
                    raise RuntimeError(
                        "result[{i}]: label: {label}: Entry has no time series for variables '{mts}' "
                        "(available time series: '{ts_keys}')".format(
                            i=i,
                            label=result_label,
                            mts=",".join([str(x) for x in missing_ts]),
                            ts_keys=",".join(e["timeSeries"].keys()),
                        )
                    )
                ts_len = set(
                    len(e["timeSeries"][m.time_series_name]["flow"]) for m in mapping.entries if m.is_time_series_key
                )
                if len(ts_len) > 1:
                    _s = " ".join([str(x) for x in ts_len])
                    raise RuntimeWarning(f"result[{i}]: bucket: {r['bucket']}: lengths of 'timeSeries' differ ({_s})")
                for k, m in mapping.items:
                    if m.is_time_series_key:
                        out_data[k].extend(
                            row[m.time_series_field_idx] for row in e["timeSeries"][m.time_series_name]["flow"]
                        )
                    else:
                        try:
                            val = m.source.format(**e)
                            out_data[k].extend([val] * max(ts_len))
                        except KeyError as ex:
                            logging.critical(
                                "result[%d]: label: %s: mapping for column '%s' ('%s') cannot be satisfied, "
                                "fields '%s' not present in data "
                                "(available fields: %s)",
                                i,
                                result_label,
                                k,
                                m.source,
                                ",".join([str(x) for x in ex.args]),
                                ",".join(r["data"][0].keys()),
                            )
                            out_data[k].extend([None] * max(ts_len))
        else:
            for c, m in mapping.items:
                try:
                    out_data[c] = [m.source.format(**e) for e in r["data"]]
                except KeyError as ex:
                    logging.critical(
                        "result[%d]: label: %s: mapping for column '%s' ('%s') cannot be satisfied, "
                        "fields '%s' not present in data "
                        "(available fields: %s)",
                        i,
                        result_label,
                        c,
                        m.source,
                        ",".join([str(x) for x in ex.args]),
                        ",".join(r["data"][0].keys()),
                    )
        out[result_label] = DataFrame.from_dict(out_data)
        set_data_types_and_index(out[result_label], mapping.items)
        logging.debug(
            "result[%d]: label: %s df shape: (%d, %d)",
            i,
            result_label,
            *out[result_label].shape,
        )
    return out
