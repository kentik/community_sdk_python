from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List

from kentik_api.public.plan import Plan, PlanDevice, PlanDeviceType
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, convert_or_none, dict_from_json, from_dict


@dataclass()
class GetResponse:
    plan: Dict[str, Any]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(cls, {"plan": dic})

    def to_plan(self) -> Plan:
        plan_dict = deepcopy(self.plan)
        plan_dict["device_types"] = [from_dict(PlanDeviceType, i) for i in plan_dict["deviceTypes"]]
        plan_dict.pop("deviceTypes")
        plan_dict["devices"] = [
            PlanDevice(
                device_name=i["device_name"],
                device_type=i["device_type"],
                id=convert(i["id"], ID),
            )
            for i in plan_dict["devices"]
        ]
        plan_dict["id"] = convert(plan_dict["id"], ID)
        plan_dict["company_id"] = convert_or_none(plan_dict["company_id"], ID)
        plan_dict["created_date"] = plan_dict["cdate"]
        plan_dict.pop("cdate")
        plan_dict["updated_date"] = plan_dict.get("edate")
        if "edate" in plan_dict:
            plan_dict.pop("edate")

        return from_dict(Plan, plan_dict)


@dataclass()
class GetAllResponse:
    plans: List[Dict[str, Any]]

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)

    def to_plans(self) -> List[Plan]:
        return [GetResponse.from_dict(d).to_plan() for d in self.plans]
