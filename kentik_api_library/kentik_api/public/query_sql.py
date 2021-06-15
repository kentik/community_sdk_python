import json
import logging
from pandas import DataFrame, to_datetime
import yaml
from collections import  defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class MappingEntry:
    format: str
    data_type: str
    is_index: bool = False


@dataclass
class QueryDefinition:
    query: str
    mapping: Optional[Dict[str, MappingEntry]] = None

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
        m: Optional[dict] = None
        if "mapping" in qd:
            m = dict()
            for c, d in qd['mapping'].items():
                if c in m:
                    raise RuntimeError(f"Duplicate mapping for column '{c}' in query definition {qd}")
                if type(d) != dict or "source" not in d.keys():
                    raise RuntimeError(f"'source' is missing in query definition entry for column {c} ({qd})")
                m[c] = MappingEntry(format=d["source"], data_type=d.get("type"), is_index=d.get("index", False))
        return cls(query=qd["query"], mapping=m)

    def expand_query(self, **kwargs) -> str:
        """
        Produce query string from template by expanding embedded str.format directives using data in kwargs
        """
        return self.query.format(**kwargs)


@dataclass
class QuerySQL:
    query: str

    @classmethod
    def from_file(cls, filename: str):
        """
        Load SQL query from a neatly formatted file
        """
        with open(filename) as f:
            qs = ' '.join([line.strip() for line in f.readlines()])
        return cls(qs)

    @classmethod
    def from_query_definition(cls, qd: QueryDefinition, **kwargs):
        return cls(qd.expand_query(**kwargs))


@dataclass
class QuerySQLResult:
    rows: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)

    def to_dataframe(self, qd: QueryDefinition) -> Optional[DataFrame]:
        """
        Retrieve data from KDE via SQL query and map them to Pandas DataFrame
        If no mapping is provided in query definition, every column in response row is included as DataFrame columns
        otherwise data are mapped to DataFrame based on mapping entries
        """
        if len(self.rows) < 1:
            logging.debug('No data in SQL result')
            return None
        data = defaultdict(list)
        for row in self.rows:
            if qd.mapping is not None:
                for k, mapping in qd.mapping.items():
                    data[k].append(mapping.format.format(**row))
            else:
                for k, v in row:
                    data[k].append(v)
        df = DataFrame.from_dict(data)
        if qd.mapping is not None:
            for k, m in qd.mapping.items():
                if m.data_type is None:
                    continue
                if m.data_type == 'time':
                    df[k] = to_datetime(df[k])
                else:
                    df[k] = df[k].astype(m.data_type)
                if m.is_index:
                    df.set_index(k, inplace=True)
                    df.sort_index(inplace=True)
        logging.debug('df shape: (%d, %d)', df.shape[0], df.shape[1])
        return df
