from typing import List
from http import HTTPStatus
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.api_calls import devices
from kentik_api.public.device import Device, AppliedLabels
from kentik_api.requests_payload import devices_payload


class DevicesAPI(BaseAPI):
    """ Exposes Kentik API operations related to devices """

    def get_all(self) -> List[Device]:
        api_call = devices.get_devices()
        response = self._send(api_call)
        return devices_payload.GetAllResponse.from_json(response.text).to_devices()

    def get(self, device_id: int) -> Device:
        api_call = devices.get_device_info(device_id)
        response = self._send(api_call)
        return devices_payload.GetResponse.from_json(response.text).to_device()

    def create(self, device: Device) -> Device:
        api_call = devices.create_device()
        payload = devices_payload.CreateRequest.from_device(device)
        response = self._send(api_call, payload)
        return devices_payload.CreateResponse.from_json(response.text).to_device()

    def update(self, device: Device) -> Device:
        api_call = devices.update_device(device.id)
        payload = devices_payload.UpdateRequest.from_device(device)
        response = self._send(api_call, payload)
        return devices_payload.UpdateResponse.from_json(response.text).to_device()

    def delete(self, device_id: int) -> bool:
        """
        Note: KentikAPI requires sending delete request twice to actually delete the device.
        This is a safety measure preventing deletion by mistake.
        """
        api_call = devices.delete_device(device_id)
        response = self._send(api_call)
        return response.http_status_code == HTTPStatus.NO_CONTENT

    def apply_labels(self, device_id: int, label_ids: List[int]) -> AppliedLabels:
        api_call = devices.apply_device_labels(device_id)
        payload = devices_payload.ApplyLabelsRequest.from_id_list(label_ids)
        response = self._send(api_call, payload)
        return devices_payload.ApplyLabelsResponse.from_json(response.text).to_applied_labels()
