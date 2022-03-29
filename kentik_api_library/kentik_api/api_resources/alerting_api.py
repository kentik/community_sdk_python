import logging
from datetime import datetime
from typing import List

from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import Alarm, AlertFilter, HistoricalAlert, ManualMitigation, SortOrder
from kentik_api.requests_payload import manual_mitigations_payload
from kentik_api.requests_payload.conversions import enum_to_str

logger = logging.getLogger(__name__)


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
        filter_by: AlertFilter = AlertFilter.NONE,
        filter_val: str = "",
        show_mitigations: bool = True,
        show_alarms: bool = True,
        show_matches: bool = False,
        learning_mode: bool = False,
    ) -> List[Alarm]:

        if filter_by == AlertFilter.NONE and filter_val != "":
            logger.warning("For filter_by == None, filter_val should be empty. Setting filter_val to empty")
            filter_val = ""

        api_call = alerts.get_active_alerts(
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            filter_by=enum_to_str(filter_by),
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
        filter_by: AlertFilter = AlertFilter.NONE,
        filter_val: str = "",
        sort_order: SortOrder = SortOrder.NONE,
        show_mitigations: bool = True,
        show_alarms: bool = True,
        show_matches: bool = False,
        learning_mode: bool = False,
    ) -> List[HistoricalAlert]:

        if filter_by == AlertFilter.NONE and filter_val != "":
            logger.warning("For filter_by == None, filter_val should be empty. Setting filter_val to empty")
            filter_val = ""

        api_call = alerts.get_alerts_history(
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            filter_by=enum_to_str(filter_by),
            filter_val=filter_val,
            sort_order=enum_to_str(sort_order),
            show_mitigations=1 if show_mitigations else 0,
            show_alarms=1 if show_alarms else 0,
            show_matches=1 if show_matches else 0,
            learning_mode=1 if learning_mode else 0,
        )
        response = self.send(api_call)
        return manual_mitigations_payload.GetHistoricalAlertsResponse.from_json(response.text).to_alerts()
