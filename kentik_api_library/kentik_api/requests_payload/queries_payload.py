import json
from typing import List, Dict
from dataclasses import dataclass

from kentik_api.public.query_object import QueryResult


@dataclass()
class GetDataResponse:
    results: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        params = json.loads(json_string)
        return cls(**params)

    def to_query_result(self) -> QueryResult:
        return QueryResult(results=self.results)
