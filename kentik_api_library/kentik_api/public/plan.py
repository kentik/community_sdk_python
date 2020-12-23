from typing import Any, Dict, List, Optional

# pylint: disable=too-many-instance-attributes


class PlanDeviceType:
    def __init__(self, device_type: str) -> None:
        self.device_type = device_type


class PlanDevice:
    def __init__(self, device_name: str, device_type: str, id: int) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.id = int(id)


class Plan:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        id: int,
        company_id: int,
        name: str,
        description: str,
        active: bool,
        max_devices: int,
        max_fps: int,
        bgp_enabled: bool,
        fast_retention: int,
        full_retention: int,
        cdate: str,
        edate: Optional[str],
        max_bigdata_fps: int,
        deviceTypes: List[PlanDeviceType],
        devices: List[PlanDevice],
        metadata: Dict[str, Any],
    ) -> None:
        self.id = id
        self.company_id = company_id
        self.name = name
        self.description = description
        self.active = active
        self.max_devices = max_devices
        self.max_fps = max_fps
        self.bgp_enabled = bgp_enabled
        self.fast_retention = fast_retention
        self.full_retention = full_retention
        self.cdate = cdate
        self.edate = edate
        self.max_bigdata_fps = max_bigdata_fps
        self.deviceTypes = deviceTypes
        self.devices = devices
        self.metadata = metadata
