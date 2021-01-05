from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


@dataclass()
class Criterion:
    class Direction(Enum):
        SRC = "src"
        DST = "dst"
        EITHER = "either"

    direction: Direction
    addr: List[str]

    def __init__(self, addr: List[str], direction: Direction = Direction.EITHER) -> None:
        assert len(addr) > 0

        self.direction = direction
        self.addr = addr


@dataclass()
class Upsert:

    value: str
    criteria: List[Criterion]


@dataclass()
class Deletion:

    value: str


@dataclass()
class BatchOperationPart:

    replace_all: bool
    complete: bool
    upserts: List[Upsert]
    deletes: List[Deletion]
    guid: Optional[str] = None