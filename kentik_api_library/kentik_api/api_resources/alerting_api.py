from typing import Optional, List

from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import ManualMitigation, Alarm, HiscoricalAlert
from kentik_api.requests_payload import manual_mitigations_payload


class AlertingAPI(BaseAPI):
    """Exposes Kentik API operations related to manual mitigation. """

    def create_manual_mitigation(self, manual_mitigation: ManualMitigation) -> bool:
        api_call = alerts.create_manual_mitigation()
        response = self._send(api_call, manual_mitigation)
        return manual_mitigations_payload.CreateResponse.from_json(response.text).status() == "OK"

    def get_active_alerts(
        self,
        startTime: str,
        endTime: str,
        filterBy: Optional[str] = None,
        filterVal: Optional[str] = None,
        showMitigations: int = 1,
        showAlarms: int = 1,
        showMatches: int = 0,
        learningMode: int = 0,
    ) -> List[Alarm]:
        api_call = alerts.get_active_alerts(
            startTime=startTime,
            endTime=endTime,
            filterBy=filterBy,
            filterVal=filterVal,
            showMitigations=showMitigations,
            showAlarms=showAlarms,
            showMatches=showMatches,
            learningMode=learningMode,
        )
        response = self._send(api_call)
        return manual_mitigations_payload.GetActiveAlertsResponse.from_json(response.text).to_alarms()

    def get_alerts_history(
        self,
        startTime: str,
        endTime: str,
        filterBy: Optional[str] = None,
        filterVal: Optional[str] = None,
        sortOrder: Optional[str] = None,
        showMitigations: int = 1,
        showAlarms: int = 1,
        showMatches: int = 0,
        learningMode: int = 0,
    ) -> List[HiscoricalAlert]:
        api_call = alerts.get_alerts_history(
            startTime=startTime,
            endTime=endTime,
            filterBy=filterBy,
            filterVal=filterVal,
            sortOrder=sortOrder,
            showMitigations=showMitigations,
            showAlarms=showAlarms,
            showMatches=showMatches,
            learningMode=learningMode,
        )
        response = self._send(api_call)
        return manual_mitigations_payload.GetHistoricalAlertsResponse.from_json(response.text).to_alerts()
