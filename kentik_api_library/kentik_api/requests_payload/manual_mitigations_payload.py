from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from kentik_api.public.manual_mitigation import ManualMitigation, Alarm, HistoricalAlert
from kentik_api.public.errors import DataFormatError
from kentik_api.requests_payload.conversions import convert, from_dict, dict_from_json, list_from_json


CreateRequest = ManualMitigation


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
        dic = deepcopy(self.__dict__)
        try:  # when alarm end is not specified, the alarm_end is set to "0000-00-00 00:00:00" then converted to None
            dic["alarm_end"] = datetime.strptime(self.alarm_end, "%Y-%m-%d %H:%M:%S")
        except ValueError as err:
            if dic["alarm_end"] == "0000-00-00 00:00:00":
                dic["alarm_end"] = None
            else:
                raise DataFormatError(str(err))

        date_parse = lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")
        dic["alarm_start"] = convert(self.alarm_start, date_parse)
        dic["learning_mode"] = self.learning_mode != 0
        dic["debug_mode"] = self.debug_mode != 0

        return from_dict(data_class=Alarm, data=dic)


class GetActiveAlertsResponse(List[_Alarm]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        obj = cls()
        for i in items:
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
        dic["learning_mode"] = self.learning_mode != 0
        dic["debug_mode"] = self.debug_mode != 0

        date_parse = lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")
        dic["creation_time"] = convert(self.ctime, date_parse)

        date_parse = lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        dic["alarm_start_time"] = convert(self.alarm_start_time, date_parse)

        return from_dict(data_class=HistoricalAlert, data=dic)


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
