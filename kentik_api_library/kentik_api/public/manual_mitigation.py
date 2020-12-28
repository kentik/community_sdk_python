from typing import Optional
from dataclasses import dataclass


@dataclass()
class ManualMitigation:
    ipCidr: str
    platformID: str
    methodId: str
    minutesBeforeAutoStop: str
    comment: Optional[str]
