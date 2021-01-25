from typing import Optional, List
from datetime import datetime

from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import ManualMitigation, Alarm, HistoricalAlert
from kentik_api.requests_payload import manual_mitigations_payload


class AlertingAPI(BaseAPI):
    """Exposes Kentik API operations related to manual mitigation. """

    def create_manual_mitigation(self, manual_mitigation: ManualMitigation) -> bool:
        api_call = alerts.create_manual_mitigation()
        response = self.send(api_call, manual_mitigation)
        return manual_mitigations_payload.CreateResponse.from_json(response.text).status() == "OK"

    def get_active_alerts(
        self,
        start_time: datetime,
        end_time: datetime,
        filter_by: Optional[str] = None,
        filter_val: Optional[str] = None,
        show_mitigations: int = 1,
        show_alarms: int = 1,
        show_matches: int = 0,
        learning_mode: int = 0,
    ) -> List[Alarm]:
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        api_call = alerts.get_active_alerts(
            start_time=start_time_str,
            end_time=end_time_str,
            filter_by=filter_by,
            filter_val=filter_val,
            show_mitigations=show_mitigations,
            show_alarms=show_alarms,
            show_matches=show_matches,
            learning_mode=learning_mode,
        )
        response = self.send(api_call)
        return manual_mitigations_payload.GetActiveAlertsResponse.from_json(response.text).to_alarms()

    def get_alerts_history(
        self,
        start_time: datetime,
        end_time: datetime,
        filter_by: Optional[str] = None,
        filter_val: Optional[str] = None,
        sort_order: Optional[str] = None,
        show_mitigations: int = 1,
        show_alarms: int = 1,
        show_matches: int = 0,
        learning_mode: int = 0,
    ) -> List[HistoricalAlert]:
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        api_call = alerts.get_alerts_history(
            start_time=start_time_str,
            end_time=end_time_str,
            filter_by=filter_by,
            filter_val=filter_val,
            sort_order=sort_order,
            show_mitigations=show_mitigations,
            show_alarms=show_alarms,
            show_matches=show_matches,
            learning_mode=learning_mode,
        )
        response = self.send(api_call)
        return manual_mitigations_payload.GetHistoricalAlertsResponse.from_json(response.text).to_alerts()
