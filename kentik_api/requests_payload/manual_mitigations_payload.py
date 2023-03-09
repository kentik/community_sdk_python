from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from kentik_api.public.errors import DataFormatError
from kentik_api.public.manual_mitigation import Alarm, HistoricalAlert
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, convert_or_none, dict_from_json, from_dict, list_from_json


class CreateResponse:
    def __init__(self, result: str) -> None:
        self.result = result

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string, "response")
        return cls(dic["result"])

    def status(self) -> str:
        return self.result


@dataclass
class _Alarm:
    alarm_id: int
    row_type: str
    alarm_state: str
    alert_id: int
    mitigation_id: Optional[int]
    threshold_id: Optional[int]
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: float
    alert_value3rd: float
    alert_match_count: int
    alert_baseline: float
    alert_severity: str
    baseline_used: int
    learning_mode: int
    debug_mode: int
    alarm_start: str
    alarm_end: str
    alarm_last_comment: Optional[str]
    mit_alert_id: int
    mit_alert_ip: str
    mit_threshold_id: int
    args: str
    id: int
    policy_id: Optional[int]
    policy_name: str
    alert_key_lookup: str

    def to_alarm(self) -> Alarm:
        d = deepcopy(self.__dict__)
        # when alarm end is not specified, the alarm_end is set to "0000-00-00 00:00:00" then converted to None
        if d["alarm_end"] == "0000-00-00 00:00:00":
            d["alarm_end"] = None
        else:
            try:
                d["alarm_end"] = datetime.fromisoformat(self.alarm_end.replace("Z", "+00:00"))
            except ValueError as err:
                raise DataFormatError(str(err))

        d["alarm_start"] = datetime.fromisoformat(self.alarm_start.replace("Z", "+00:00"))
        d["learning_mode"] = self.learning_mode != 0
        d["debug_mode"] = self.debug_mode != 0

        d["alarm_id"] = convert(d["alarm_id"], ID)
        d["alert_id"] = convert(d["alert_id"], ID)
        d["mitigation_id"] = convert_or_none(d["mitigation_id"], ID)
        d["threshold_id"] = convert_or_none(d["threshold_id"], ID)
        d["mit_alert_id"] = convert(d["mit_alert_id"], ID)
        d["mit_threshold_id"] = convert(d["mit_threshold_id"], ID)
        d["id"] = convert(d["id"], ID)
        d["policy_id"] = convert_or_none(d["policy_id"], ID)

        return from_dict(data_class=Alarm, data=d)


class GetActiveAlertsResponse(List[_Alarm]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        obj = cls()
        for i in items:
            # Workaround for manual mitigation entries which do not comply with general schema
            if "type" in i and i["type"] == "manual":
                if i["args"] is None:
                    i["args"] = ""
                if i["alert_metric"] == "":
                    i["alert_metric"] = []
                if i["alarm_end"] is None:
                    i["alarm_end"] = "0000-00-00 00:00:00"
                if i["mit_alert_id"] is None:
                    i["mit_alert_id"] = 0
                if i["mit_threshold_id"] is None:
                    i["mit_threshold_id"] = 0
            obj.append(from_dict(data_class=_Alarm, data=i))
        return obj

    def to_alarms(self) -> List[Alarm]:
        alarms = [i.to_alarm() for i in self]
        return alarms


@dataclass
class _HistoricalAlert:
    row_type: str
    old_alarm_state: str
    new_alarm_state: str
    alert_match_count: str
    alert_severity: str
    alert_id: int
    threshold_id: Optional[int]
    alarm_id: int
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: float
    alert_value3rd: float
    alert_baseline: float
    baseline_used: int
    learning_mode: int
    debug_mode: int
    ctime: str
    alarm_start_time: str
    comment: Optional[str]
    mitigation_id: Optional[int]
    mit_method_id: int
    args: str
    id: int
    policy_id: int
    policy_name: str
    alert_key_lookup: str

    def to_alert(self) -> HistoricalAlert:
        d = deepcopy(self.__dict__)
        d.pop("ctime")
        d["learning_mode"] = self.learning_mode != 0
        d["debug_mode"] = self.debug_mode != 0

        d["creation_time"] = datetime.fromisoformat(self.ctime.replace("Z", "+00:00"))
        d["alarm_start_time"] = datetime.fromisoformat(self.alarm_start_time + "+00:00")

        d["alert_id"] = convert(d["alert_id"], ID)
        d["threshold_id"] = convert_or_none(d["threshold_id"], ID)
        d["alarm_id"] = convert(d["alarm_id"], ID)
        d["mitigation_id"] = convert_or_none(d["mitigation_id"], ID)
        d["mit_method_id"] = convert(d["mit_method_id"], ID)
        d["id"] = convert(d["id"], ID)
        d["policy_id"] = convert(d["policy_id"], ID)

        return from_dict(data_class=HistoricalAlert, data=d)


class GetHistoricalAlertsResponse(List[_HistoricalAlert]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        obj = cls()
        for i in items:
            obj.append(from_dict(data_class=_HistoricalAlert, data=i))
        return obj

    def to_alerts(self) -> List[HistoricalAlert]:
        alarms = [i.to_alert() for i in self]
        return alarms
