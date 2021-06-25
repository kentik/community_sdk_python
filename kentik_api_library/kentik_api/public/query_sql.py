import json
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class QuerySQL:
    query: str

    @classmethod
    def from_file(cls, filename: str):
        """
        Load SQL query from a neatly formatted file
        """
        with open(filename) as f:
            qs = " ".join([line.strip() for line in f.readlines()])
        return cls(qs)


@dataclass
class QuerySQLResult:
    rows: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)
