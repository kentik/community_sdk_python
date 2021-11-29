from http import HTTPStatus
from typing import List

from kentik_api.api_calls import devices
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.device import AppliedLabels, Device, Interface
from kentik_api.public.types import ID
from kentik_api.requests_payload import devices_payload, interfaces_payload


class InterfacesAPI(BaseAPI):
    """Exposes Kentik API operations related to interfaces"""

    def get_all(self, device_id: ID) -> List[Interface]:
        api_call = devices.get_device_interfaces(device_id)
        response = self.send(api_call)
        return interfaces_payload.GetAllResponse.from_json(response.text).to_interfaces()

    def get(self, device_id: ID, interface_id: ID) -> Interface:
        api_call = devices.get_device_interface_info(device_id, interface_id)
        response = self.send(api_call)
        return interfaces_payload.GetResponse.from_json(response.text).to_interface()

    def create(self, interface: Interface) -> Interface:
        api_call = devices.create_interface(interface.device_id)
        payload = interfaces_payload.CreateRequest.from_interface(interface)
        response = self.send(api_call, payload)
        return interfaces_payload.CreateResponse.from_json(response.text).to_interface()

    def update(self, interface: Interface) -> Interface:
        api_call = devices.update_interface(interface.device_id, interface.id)
        payload = interfaces_payload.UpdateRequest.from_interface(interface)
        response = self.send(api_call, payload)
        return interfaces_payload.UpdateResponse.from_json(response.text).to_interface()

    def delete(self, device_id: ID, interface_id: ID) -> bool:
        api_call = devices.delete_interface(device_id, interface_id)
        response = self.send(api_call)
        return response.http_status_code == HTTPStatus.OK


class DevicesAPI(BaseAPI):
    """Exposes Kentik API operations related to devices"""

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        super(DevicesAPI, self).__init__(api_connector)
        self._interfaces = InterfacesAPI(api_connector)

    def get_all(self) -> List[Device]:
        api_call = devices.get_devices()
        response = self.send(api_call)
        return devices_payload.GetAllResponse.from_json(response.text).to_devices()

    def get(self, device_id: ID) -> Device:
        api_call = devices.get_device_info(device_id)
        response = self.send(api_call)
        return devices_payload.GetResponse.from_json(response.text).to_device()

    def create(self, device: Device) -> Device:
        api_call = devices.create_device()
        payload = devices_payload.CreateRequest.from_device(device)
        response = self.send(api_call, payload)
        return devices_payload.CreateResponse.from_json(response.text).to_device()

    def update(self, device: Device) -> Device:
        api_call = devices.update_device(device.id)
        payload = devices_payload.UpdateRequest.from_device(device)
        response = self.send(api_call, payload)
        return devices_payload.UpdateResponse.from_json(response.text).to_device()

    def delete(self, device_id: ID) -> bool:
        """
        Note: KentikAPI requires sending delete request twice to actually delete the device.
        This is a safety measure preventing deletion by mistake.
        """
        api_call = devices.delete_device(device_id)
        response = self.send(api_call)
        return response.http_status_code == HTTPStatus.NO_CONTENT

    def apply_labels(self, device_id: ID, label_ids: List[ID]) -> AppliedLabels:
        api_call = devices.apply_device_labels(device_id)
        payload = devices_payload.ApplyLabelsRequest.from_id_list(label_ids)
        response = self.send(api_call, payload)
        return devices_payload.ApplyLabelsResponse.from_json(response.text).to_applied_labels()

    @property
    def interfaces(self) -> InterfacesAPI:
        return self._interfaces
