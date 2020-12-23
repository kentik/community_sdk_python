from http import HTTPStatus

from kentik_api.api_calls import alerts
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.manual_mitigation import ManualMitigation
from kentik_api.requests_payload import manual_mitigations_payload
from kentik_api.requests_payload.as_dict import as_dict


class AlertingAPI(BaseAPI):
    """Exposes Kentik API operations related to manual mitigation. """

    def create_manual_mitigation(self, manual_mitigation: ManualMitigation) -> bool:
        api_call = alerts.create_manual_mitigation()
        payload = as_dict(manual_mitigations_payload.CreateRequest(
            ipCidr=manual_mitigation.ipCidr,
            Comment=manual_mitigation.comment,
            platformID=manual_mitigation.platformID,
            methodID=manual_mitigation.methodId,
            minutesBeforeAutoStop=manual_mitigation.minutesBeforeAutoStop,
        ))
        response = self._send(api_call, payload)
        return manual_mitigations_payload.CreateResponse.from_json(response.text).status() == "OK"
