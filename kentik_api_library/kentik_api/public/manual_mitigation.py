from typing import Optional
from dataclasses import dataclass


@dataclass()
class ManualMitigation:
    ipCidr: str
    comment: Optional[str]
    platformID: str
    methodID: str
    minutesBeforeAutoStop: str
