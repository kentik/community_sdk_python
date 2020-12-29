from dataclasses import dataclass
from typing import List, Optional


@dataclass()
class Criterion:

    direction: str
    addr: List[str]

    def __init__(self, addr: List[str], direction: Optional[str] = "either") -> None:
        assert direction in ["src", "dst", "either"]
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
