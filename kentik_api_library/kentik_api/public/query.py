import json
from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass
class SQLQuery:
    query: str


@dataclass
class SQLQueryResult:
    rows: Sequence[Mapping]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)
