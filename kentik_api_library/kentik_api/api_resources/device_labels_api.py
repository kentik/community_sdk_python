from typing import List

from kentik_api.api_calls import labels
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.public.device_label import DeviceLabel
from kentik_api.requests_payload import labels_payload, as_dict


class DeviceLabelsAPI:
    """ Exposes Kentik API operations related to device labels """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def _send(self, api_call, payload=None):
        if payload is not None:
            payload = as_dict.as_dict(payload)
        return self._api_connector.send(api_call, payload)

    def get_all(self) -> List[DeviceLabel]:
        apicall = labels.get_labels()
        response = self._send(apicall)
        return labels_payload.GetAllResponse.from_json(response.text).to_device_labels()

    def get(self, label_id: int) -> DeviceLabel:
        apicall = labels.get_label_info(label_id)
        response = self._send(apicall)
        return labels_payload.GetResponse.from_json(response.text).to_device_label()

    def create(self, device_label: DeviceLabel) -> DeviceLabel:
        apicall = labels.create_label()
        payload = labels_payload.CreateRequest(device_label.name, device_label.color).__dict__
        response = self._send(apicall, payload)
        return labels_payload.CreateResponse.from_json(response.text).to_device_label()

    def update(self, device_label: DeviceLabel) -> DeviceLabel:
        apicall = labels.update_label(device_label.id)
        payload = labels_payload.UpdateRequest(device_label.name, device_label.color).__dict__
        response = self._send(apicall, payload)
        return labels_payload.UpdateResponse.from_json(response.text).to_device_label()

    def delete(self, label_id: int) -> bool:
        apicall = labels.delete_label(label_id)
        response = self._send(apicall)
        return labels_payload.DeleteResponse.from_json(response.text).success
