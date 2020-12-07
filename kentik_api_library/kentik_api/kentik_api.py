# Local application imports
from kentik_api.api_connection.api_connector import APIConnector
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.api_resources.device_labels_api import DeviceLabelsAPI


class KentikAPI:
    """ Root object for operating KentikAPI """

    API_VERSION = "v5"

    def __init__(self, connector: APIConnectorProtocol) -> None:
        self.device_labels = DeviceLabelsAPI(connector)
        # self.devices =
        # self.users =
        # self.tags =
        # ...



def for_com_domain(auth_email: str, auth_token: str) -> KentikAPI:
    """ Handy kentik api client constructor for COM domain """

    connector = new_connector(APIConnector.BASE_API_COM_URL, auth_email, auth_token)
    return KentikAPI(connector)


def for_eu_domain(auth_email: str, auth_token: str) -> KentikAPI:
    """ Handy kentik api client constructor for EU domain """

    connector = new_connector(APIConnector.BASE_API_EU_URL, auth_email, auth_token)
    return KentikAPI(connector)


def new_connector(api_url: str, auth_email: str, auth_token: str) -> APIConnector:
    versioned_api_url = api_url + "/" + KentikAPI.API_VERSION
    return APIConnector(versioned_api_url, auth_email, auth_token)
