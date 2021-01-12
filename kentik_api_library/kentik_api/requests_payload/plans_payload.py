from dataclasses import dataclass
import json
from typing import Dict, List, Any

from kentik_api.public.plan import Plan, PlanDeviceType, PlanDevice


@dataclass()
class GetResponse:
    plan: Dict[str, Any]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(plan=dic)

    def to_plan(self) -> Plan:
        plan_dict = dict(self.plan)  # deep copy for safety
        plan_dict["deviceTypes"] = [PlanDeviceType(**i) for i in plan_dict["deviceTypes"]]
        plan_dict["devices"] = [
            PlanDevice(
                device_name=i["device_name"],
                device_type=i["device_type"],
                id=int(i["id"]),
            )
            for i in plan_dict["devices"]
        ]
        return Plan(**plan_dict)


@dataclass()
class GetAllResponse:
    plans: List[Dict[str, Any]]

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_plans(self) -> List[Plan]:
        return [GetResponse.from_dict(d).to_plan() for d in self.plans]
