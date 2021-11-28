from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.types import ID

# pylint: disable=too-many-instance-attributes


@dataclass()
class PlanDeviceType:
    device_type: str


@dataclass()
class PlanDevice:
    device_name: str
    device_type: str
    id: ID


@dataclass()
class Plan:
    id: ID
    company_id: Optional[ID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    max_devices: Optional[int] = None
    max_fps: Optional[int] = None
    bgp_enabled: Optional[bool] = None
    fast_retention: Optional[int] = None
    full_retention: Optional[int] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    max_bigdata_fps: Optional[int] = None
    device_types: Optional[List[PlanDeviceType]] = None
    devices: Optional[List[PlanDevice]] = None
    metadata: Optional[Dict[str, Any]] = None
