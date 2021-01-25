from copy import deepcopy
import json
from dataclasses import dataclass
from typing import Optional, List
from dacite import from_dict
from datetime import datetime

from kentik_api.public.manual_mitigation import ManualMitigation, Alarm, HistoricalAlert


CreateRequest = ManualMitigation


class CreateResponse:
    def __init__(self, result: str) -> None:
        self.result = result

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(dic["response"]["result"])

    def status(self) -> str:
        return self.result


@dataclass
class _Alarm:
    alarm_id: int
    row_type: str
    alarm_state: str
    alert_id: int
    mitigation_id: Optional[int]
    threshold_id: int
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: float
    alert_value3rd: float
    alert_match_count: int
    alert_baseline: int
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
    policy_id: int
    policy_name: str
    alert_key_lookup: str

    def to_alarm(self) -> Alarm:
        dic = self.__dict__
        try:
            dic["alarm_end"] = datetime.strptime(self.alarm_end, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dic["alarm_end"] = None
        dic["alarm_start"] = datetime.strptime(self.alarm_start, "%Y-%m-%dT%H:%M:%S.000Z")
        return Alarm(**dic)


class GetActiveAlertsResponse(List[_Alarm]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        obj = cls()
        for i in dic:
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
    threshold_id: int
    alarm_id: int
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: int
    alert_value3rd: int
    alert_baseline: int
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
        dic = deepcopy(self.__dict__)
        dic.pop("ctime")
        dic["creation_time"] = datetime.strptime(self.ctime, "%Y-%m-%dT%H:%M:%S.000Z")
        dic["alarm_start_time"] = datetime.strptime(self.alarm_start_time, "%Y-%m-%d %H:%M:%S")
        return HistoricalAlert(**dic)


class GetHistoricalAlertsResponse(List[_HistoricalAlert]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        obj = cls()
        for i in dic:
            obj.append(from_dict(data_class=_HistoricalAlert, data=i))
        return obj

    def to_alerts(self) -> List[HistoricalAlert]:
        alarms = [i.to_alert() for i in self]
        return alarms
