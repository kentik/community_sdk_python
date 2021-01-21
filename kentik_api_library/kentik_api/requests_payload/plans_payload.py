from dataclasses import dataclass
import json
from typing import Dict, List, Any

from kentik_api.requests_payload.conversions import convert, convert_or_none
from kentik_api.public.types import ID
from kentik_api.public.plan import Plan, PlanDeviceType, PlanDevice


@dataclass()
class GetResponse:
    plan: Dict[str, Any]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(plan=dic)

    def to_plan(self) -> Plan:
        plan_dict = self.plan
        device_types = [PlanDeviceType(**i) for i in plan_dict["deviceTypes"]]
        devices = [
            PlanDevice(
                device_name=i["device_name"],
                device_type=i["device_type"],
                id=convert(i["id"], ID),
            )
            for i in plan_dict["devices"]
        ]

        return Plan(
            id=convert(plan_dict["id"], ID),
            company_id=convert_or_none(plan_dict["company_id"], ID),
            name=plan_dict["name"],
            description=plan_dict["description"],
            active=plan_dict["active"],
            max_devices=plan_dict["max_devices"],
            max_fps=plan_dict["max_fps"],
            bgp_enabled=plan_dict["bgp_enabled"],
            fast_retention=plan_dict["fast_retention"],
            full_retention=plan_dict["full_retention"],
            created_date=plan_dict["cdate"],
            updated_date=plan_dict.get("edate"),
            max_bigdata_fps=plan_dict["max_bigdata_fps"],
            device_types=device_types,
            devices=devices,
            metadata=plan_dict["metadata"],
        )


@dataclass()
class GetAllResponse:
    plans: List[Dict[str, Any]]

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_plans(self) -> List[Plan]:
        return [GetResponse.from_dict(d).to_plan() for d in self.plans]
