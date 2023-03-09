from typing import List

from kentik_api.api_calls import device_labels
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.device_label import DeviceLabel
from kentik_api.public.types import ID
from kentik_api.requests_payload import labels_payload


class DeviceLabelsAPI(BaseAPI):
    """Exposes Kentik API operations related to device labels"""

    def get_all(self) -> List[DeviceLabel]:
        apicall = device_labels.get_device_labels()
        response = self.send(apicall)
        return labels_payload.GetAllResponse.from_json(response.text).to_device_labels()

    def get(self, label_id: ID) -> DeviceLabel:
        apicall = device_labels.get_device_label_info(label_id)
        response = self.send(apicall)
        return labels_payload.GetResponse.from_json(response.text).to_device_label()

    def create(self, device_label: DeviceLabel) -> DeviceLabel:
        apicall = device_labels.create_device_label()
        payload = labels_payload.CreateRequest(device_label.name, device_label.color)
        response = self.send(apicall, payload)
        return labels_payload.CreateResponse.from_json(response.text).to_device_label()

    def update(self, device_label: DeviceLabel) -> DeviceLabel:
        apicall = device_labels.update_device_label(device_label.id)
        payload = labels_payload.UpdateRequest(device_label.name, device_label.color)
        response = self.send(apicall, payload)
        return labels_payload.UpdateResponse.from_json(response.text).to_device_label()

    def delete(self, label_id: ID) -> bool:
        apicall = device_labels.delete_device_label(label_id)
        response = self.send(apicall)
        return labels_payload.DeleteResponse.from_json(response.text).success
