from .api_connection.api_connector import APIConnector
from .api_resources.alerting_api import AlertingAPI
from .api_resources.batch_api import BatchAPI
from .api_resources.custom_applications_api import CustomApplicationsAPI
from .api_resources.custom_dimensions_api import CustomDimensionsAPI
from .api_resources.device_labels_api import DeviceLabelsAPI
from .api_resources.devices_api import DevicesAPI
from .api_resources.plans_api import PlansAPI
from .api_resources.query_api import QueryAPI
from .api_resources.saved_filters_api import SavedFiltersAPI
from .api_resources.sites_api import SitesAPI
from .api_resources.tags_api import TagsAPI
from .api_resources.tenants_api import MyKentikPortalAPI
from .api_resources.users_api import UsersAPI
from typing import Optional, Tuple, Union
from .api_connection.retryable_session import Retry

# pylint: disable=too-many-instance-attributes


class KentikAPI:
    """Root object for operating KentikAPI"""

    API_URL_EU = "https://api.kentik.eu/api/v5"
    API_URL_US = "https://api.kentik.com/api/v5"

    def __init__(
        self,
        auth_email: str,
        auth_token: str,
        api_url: str = API_URL_US,
        timeout: Union[float, Tuple[float, float]] = (10.0, 60.0),
        retry_strategy: Optional[Retry] = None,
    ) -> None:
        connector = new_connector(api_url, auth_email, auth_token, timeout, retry_strategy)

        self.device_labels = DeviceLabelsAPI(connector)
        self.sites = SitesAPI(connector)
        self.users = UsersAPI(connector)
        self.tags = TagsAPI(connector)
        self.saved_filters = SavedFiltersAPI(connector)
        self.custom_dimensions = CustomDimensionsAPI(connector)
        self.custom_applications = CustomApplicationsAPI(connector)
        self.query = QueryAPI(connector)
        self.plans = PlansAPI(connector)
        self.my_kentik_portal = MyKentikPortalAPI(connector)
        self.devices = DevicesAPI(connector)
        self.batch = BatchAPI(connector)
        self.alerting = AlertingAPI(connector)


# pylint: enable=too-many-instance-attributes


def new_connector(
    api_url: str,
    auth_email: str,
    auth_token: str,
    timeout: Union[float, Tuple[float, float]],
    retry_strategy: Optional[Retry],
) -> APIConnector:
    return APIConnector(api_url, auth_email, auth_token, timeout, retry_strategy)
