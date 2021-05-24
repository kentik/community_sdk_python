from typing import Optional, List
from datetime import datetime

from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import ManualMitigation, Alarm, HistoricalAlert, AlertFilter
from kentik_api.requests_payload import manual_mitigations_payload
from kentik_api.requests_payload.conversions import convert, convert_or_none, enum_to_str


class AlertingAPI(BaseAPI):
    """Exposes Kentik API operations related to manual mitigation."""

    def create_manual_mitigation(self, manual_mitigation: ManualMitigation) -> bool:
        api_call = alerts.create_manual_mitigation()
        response = self.send(api_call, manual_mitigation)
        return manual_mitigations_payload.CreateResponse.from_json(response.text).status() == "OK"

    def get_active_alerts(
        self,
        start_time: datetime,
        end_time: datetime,
        filter_by: Optional[AlertFilter] = None,
        filter_val: Optional[str] = None,
        show_mitigations: bool = True,
        show_alarms: bool = True,
        show_matches: bool = False,
        learning_mode: bool = False,
    ) -> List[Alarm]:

        date_to_str = lambda date: date.strftime("%Y-%m-%dT%H:%M:%S")
        start_time_str = convert(start_time, date_to_str)
        end_time_str = convert(end_time, date_to_str)

        api_call = alerts.get_active_alerts(
            start_time=start_time_str,
            end_time=end_time_str,
            filter_by=convert_or_none(filter_by, enum_to_str),
            filter_val=filter_val,
            show_mitigations=1 if show_mitigations else 0,
            show_alarms=1 if show_alarms else 0,
            show_matches=1 if show_matches else 0,
            learning_mode=1 if learning_mode else 0,
        )
        response = self.send(api_call)
        return manual_mitigations_payload.GetActiveAlertsResponse.from_json(response.text).to_alarms()

    def get_alerts_history(
        self,
        start_time: datetime,
        end_time: datetime,
        filter_by: Optional[AlertFilter] = None,
        filter_val: Optional[str] = None,
        sort_order: Optional[str] = None,
        show_mitigations: bool = True,
        show_alarms: bool = True,
        show_matches: bool = False,
        learning_mode: bool = False,
    ) -> List[HistoricalAlert]:

        date_to_str = lambda date: date.strftime("%Y-%m-%dT%H:%M:%S")
        start_time_str = convert(start_time, date_to_str)
        end_time_str = convert(end_time, date_to_str)

        api_call = alerts.get_alerts_history(
            start_time=start_time_str,
            end_time=end_time_str,
            filter_by=convert_or_none(filter_by, enum_to_str),
            filter_val=filter_val,
            sort_order=sort_order,
            show_mitigations=1 if show_mitigations else 0,
            show_alarms=1 if show_alarms else 0,
            show_matches=1 if show_matches else 0,
            learning_mode=1 if learning_mode else 0,
        )
        response = self.send(api_call)
        return manual_mitigations_payload.GetHistoricalAlertsResponse.from_json(response.text).to_alerts()
