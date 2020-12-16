from typing import List

from kentik_api.api_calls import custom_applications
from kentik_api.public.custom_application import CustomApplication
from kentik_api.requests_payload import custom_applications_payload, as_dict
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol


class CustomApplicationsAPI:
    """ Exposes Kentik API operations related to custom applications """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def _send(self, api_call, payload=None):
        if payload is not None:
            payload = as_dict.as_dict(payload)
        return self._api_connector.send(api_call, payload)

    def get_all(self) -> List[CustomApplication]:
        apicall = custom_applications.get_custom_applications()
        response = self._send(apicall)
        return custom_applications_payload.GetAllResponse.from_json(response.text).to_custom_applications()

    def create(self, custom_application: CustomApplication) -> CustomApplication:
        assert custom_application.name is not None
        apicall = custom_applications.create_custom_application()
        payload = custom_applications_payload.CreateRequest(
            name=custom_application.name,
            description=custom_application.description,
            ip_range=custom_application.ip_range,
            protocol=custom_application.protocol,
            port=custom_application.port,
            asn=custom_application.asn,
        )
        response = self._send(apicall, payload)
        return custom_applications_payload.CreateResponse.from_json(response.text).to_custom_application()

    def update(self, custom_application: CustomApplication) -> CustomApplication:
        apicall = custom_applications.update_custom_application(custom_application.id)
        payload = custom_applications_payload.UpdateRequest(
            name=custom_application.name,
            description=custom_application.description,
            ip_range=custom_application.ip_range,
            protocol=custom_application.protocol,
            port=custom_application.port,
            asn=custom_application.asn,
        )
        response = self._send(apicall, payload)
        return custom_applications_payload.UpdateResponse.from_json(response.text).to_custom_application()

    def delete(self, custom_application_id: int) -> bool:
        apicall = custom_applications.delete_custom_application(custom_application_id)
        response = self._send(apicall)
        return response.http_status_code == 204
