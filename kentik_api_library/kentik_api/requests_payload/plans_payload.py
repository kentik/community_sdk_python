from dataclasses import dataclass
import json
from typing import Dict, List

from kentik_api.public.plan import Plan, PlanDeviceType, PlanDevice


@dataclass()
class GetAllResponse:
    plans: List[Dict]

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_plans(self) -> List[Plan]:
        plans = self.plans
        for plan in plans:
            plan["deviceTypes"] = [PlanDeviceType(**i) for i in plan["deviceTypes"]]
            plan["devices"] = [
                PlanDevice(
                    device_name=i["device_name"],
                    device_type=i["device_type"],
                    id=int(i["id"]),
                )
                for i in plan["devices"]
            ]
        return [Plan(**i) for i in plans]
