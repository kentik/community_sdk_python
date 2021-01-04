from kentik_api.public.manual_mitigation import ManualMitigation
import json
from dataclasses import dataclass
from typing import Optional


@dataclass()
class CreateRequest:
    ipCidr: str
    comment: Optional[str]
    platformID: str
    methodID: str
    minutesBeforeAutoStop: str


class CreateResponse:
    def __init__(self, result: str) -> None:
        self.result = result

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(dic["response"]["result"])

    def status(self) -> str:
        return self.result
