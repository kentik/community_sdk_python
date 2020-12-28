from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# pylint: disable=too-many-instance-attributes


@dataclass()
class PlanDeviceType:
    device_type: str


@dataclass()
class PlanDevice:
    device_name: str
    device_type: str
    id: int


@dataclass()
class Plan:
    id: int
    company_id: int
    name: str
    description: str
    active: bool
    max_devices: int
    max_fps: int
    bgp_enabled: bool
    fast_retention: int
    full_retention: int
    cdate: str
    edate: Optional[str]
    max_bigdata_fps: int
    deviceTypes: List[PlanDeviceType]
    devices: List[PlanDevice]
    metadata: Dict[str, Any]
