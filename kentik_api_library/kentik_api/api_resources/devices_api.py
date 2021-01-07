from typing import List
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.api_calls import devices
from kentik_api.public.device import Device
from kentik_api.requests_payload import devices_payload


class DevicesAPI(BaseAPI):
    """ Exposes Kentik API operations related to devices """

    def get(self, device_id: int) -> Device:
        apicall = devices.get_device_info(device_id)
        response = self._send(apicall)
        return devices_payload.GetResponse.from_json(response.text).to_device()
