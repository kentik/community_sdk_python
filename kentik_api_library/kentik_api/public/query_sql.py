import json
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class SQLQuery:
    query: str


@dataclass
class SQLQueryResult:
    rows: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)
