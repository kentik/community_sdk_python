from http import HTTPStatus
from typing import List

from kentik_api.api_calls import custom_applications
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.custom_application import CustomApplication
from kentik_api.public.types import ID
from kentik_api.requests_payload import custom_applications_payload


class CustomApplicationsAPI(BaseAPI):
    """Exposes Kentik API operations related to custom applications"""

    def get_all(self) -> List[CustomApplication]:
        apicall = custom_applications.get_custom_applications()
        response = self.send(apicall)
        return custom_applications_payload.GetAllResponse.from_json(response.text).to_custom_applications()

    def create(self, custom_application: CustomApplication) -> CustomApplication:
        apicall = custom_applications.create_custom_application()
        payload = custom_applications_payload.CreateRequest.from_custom_application(custom_application)
        response = self.send(apicall, payload)
        return custom_applications_payload.CreateResponse.from_json(response.text).to_custom_application()

    def update(self, custom_application: CustomApplication) -> CustomApplication:
        apicall = custom_applications.update_custom_application(custom_application.id)
        payload = custom_applications_payload.UpdateRequest.from_custom_application(custom_application)
        response = self.send(apicall, payload)
        return custom_applications_payload.UpdateResponse.from_json(response.text).to_custom_application()

    def delete(self, custom_application_id: ID) -> bool:
        apicall = custom_applications.delete_custom_application(custom_application_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT
