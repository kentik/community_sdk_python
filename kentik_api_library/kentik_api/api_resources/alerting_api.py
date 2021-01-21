from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import ManualMitigation
from kentik_api.requests_payload import manual_mitigations_payload


class AlertingAPI(BaseAPI):
    """Exposes Kentik API operations related to manual mitigation. """

    def create_manual_mitigation(self, manual_mitigation: ManualMitigation) -> bool:
        api_call = alerts.create_manual_mitigation()
        response = self.send(api_call, manual_mitigation)
        return manual_mitigations_payload.CreateResponse.from_json(response.text).status() == "OK"
