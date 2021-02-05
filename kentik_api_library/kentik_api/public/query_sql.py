import json
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class QuerySQL:
    query: str


@dataclass
class QuerySQLResult:
    rows: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)
