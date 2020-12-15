from .api_connection.api_connector import APIConnector
from .api_resources.device_labels_api import DeviceLabelsAPI
from .api_resources.sites_api import SitesAPI
from .api_resources.users_api import UsersAPI
from .api_resources.tags_api import TagsAPI
from .api_resources.custom_applications_api import CustomApplicationsAPI
from .api_resources.custom_dimensions_api import CustomDimensionsAPI

API_REGION_US = "us"
API_REGION_EU = "eu"


class KentikAPI(object):
    """ Root object for operating KentikAPI """

    API_VERSION = "v5"

    def __init__(self, auth_email: str, auth_token: str, region: str = API_REGION_US) -> None:
        if region.lower() == API_REGION_EU:
            url = APIConnector.BASE_API_EU_URL
        else:
            url = APIConnector.BASE_API_US_URL
        connector = new_connector(url, auth_email, auth_token)

        self.device_labels = DeviceLabelsAPI(connector)
        self.sites = SitesAPI(connector)
        self.users = UsersAPI(connector)
        self.tags = TagsAPI(connector)
        self.custom_dimensions = CustomDimensionsAPI(connector)
        self.custom_applications = CustomApplicationsAPI(connector)
        # self.devices =
        # ...


def new_connector(api_url: str, auth_email: str, auth_token: str) -> APIConnector:
    versioned_api_url = api_url + "/" + KentikAPI.API_VERSION
    return APIConnector(versioned_api_url, auth_email, auth_token)
