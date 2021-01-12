import json
from typing import Optional, List
from dataclasses import dataclass
from dacite import from_dict


@dataclass()
class BatchRequest:
    @dataclass()
    class Upsert:
        @dataclass()
        class Criterion:

            direction: str
            addr: List[str]

        value: str
        criteria: List[Criterion]

    @dataclass()
    class Delete:

        value: str

    replace_all: bool
    complete: bool
    upserts: List[Upsert]
    deletes: List[Delete]
    guid: Optional[str] = None


@dataclass()
class BatchResponse:

    message: str
    guid: str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)


@dataclass()
class BatchStatusResponse:
    @dataclass()
    class CustomDimension:

        id: int
        name: str

    @dataclass()
    class User:

        id: int
        email: str

    @dataclass()
    class Upserts:

        total: int
        applied: int
        invalid: int
        unchanged: int
        over_limit: int

    @dataclass()
    class Deletes:

        total: int
        applied: int
        unchanged: int
        invalid: int

    @dataclass()
    class ReplaceAll:

        requested: bool
        deletes_performed: int
        successful: bool

    custom_dimension: Optional[CustomDimension]
    guid: str
    is_multipart: bool
    is_complete: bool
    number_of_parts: int
    user: User
    upserts: Upserts
    deletes: Deletes
    replace_all: ReplaceAll
    batch_date: str
    is_pending: Optional[bool] = None

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return from_dict(data_class=cls, data=dic)
