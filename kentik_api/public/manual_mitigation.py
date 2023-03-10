from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from kentik_api.public.types import ID


@dataclass()
class ManualMitigation:
    ipCidr: str
    comment: Optional[str]
    platformID: ID
    methodID: ID
    minutesBeforeAutoStop: str


@dataclass
class Alarm:
    alarm_id: ID
    row_type: str
    alarm_state: str
    alert_id: ID
    mitigation_id: Optional[ID]
    threshold_id: Optional[ID]
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
    learning_mode: bool
    debug_mode: bool
    alarm_start: datetime
    alarm_end: Optional[datetime]
    alarm_last_comment: Optional[str]
    mit_alert_id: ID
    mit_alert_ip: str
    mit_threshold_id: ID
    args: str
    id: ID
    policy_id: Optional[ID]
    policy_name: str
    alert_key_lookup: str


@dataclass
class HistoricalAlert:
    row_type: str
    old_alarm_state: str
    new_alarm_state: str
    alert_match_count: str
    alert_severity: str
    alert_id: ID
    threshold_id: Optional[ID]
    alarm_id: ID
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: float
    alert_value3rd: float
    alert_baseline: float
    baseline_used: float
    learning_mode: bool
    debug_mode: bool
    creation_time: datetime
    alarm_start_time: datetime
    comment: Optional[str]
    mitigation_id: Optional[ID]
    mit_method_id: ID
    args: str
    id: ID
    policy_id: ID
    policy_name: str
    alert_key_lookup: str


class AlertFilter(Enum):
    NONE = "None"
    OLD_STATE = "old_state"
    NEW_STATE = "new_state"
    ANY_STATE = "any_state"
    ALERT_KEY_PARTIAL = "alert_key_partial"
    DIMENSION_KEY = "dimension_key"
    MITIGATION_ID = "mitigation_id"
    ALERT_ID = "alert_id"
    ALERT_KEY = "alert_key"
    ALARM_ID = "alarm_id"


class SortOrder(Enum):
    NONE = "None"
    ALERT_KEY = "alert_key"
    SEVERITY = "severity"
    MITIGATION_ID = "mitigation_id"
    ALARM_ID = "alarm_id"
    ALERT_ID = "alert_id"
    ALERT_VALUE = "alert_value"
    ALARM_STATE = "alarm_state"
