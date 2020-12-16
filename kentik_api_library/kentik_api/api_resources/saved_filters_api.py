from http import HTTPStatus
from typing import List

from kentik_api.api_calls import saved_filters
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.public.saved_filter import SavedFilter
from kentik_api.requests_payload import saved_filters_payload
from kentik_api.requests_payload.as_dict import as_dict


class SavedFiltersAPI:
    """Exposes Kentik API operations related to saved filters. """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def get_all(self) -> List[SavedFilter]:
        api_call = saved_filters.get_saved_filters()
        response = self._api_connector.send(api_call)
        return saved_filters_payload.GetAllResponse.from_json(response.text).to_saved_filters()

    def get(self, saved_filter_id: int) -> SavedFilter:
        api_call = saved_filters.get_saved_filter_info(saved_filter_id)
        response = self._api_connector.send(api_call)
        return saved_filters_payload.GetResponse.from_json(response.text).to_saved_filter()

    def create(self, savedFilter: SavedFilter) -> SavedFilter:
        # Checking if required data is provided
        assert savedFilter.filter_name is not None, "Filter must have name"
        assert savedFilter.filters.connector is not None
        # assert savedFilter.filters.filterGroups.connector is not None
        assert all(i.connector is not None for i in savedFilter.filters.filterGroups)
        # assert savedFilter.filters.filterGroups.not_ is not None
        assert all(i.not_ is not None for i in savedFilter.filters.filterGroups)

        api_call = saved_filters.create_saved_filter()
        payload = as_dict(saved_filters_payload.CreateRequest(savedFilter))
        print(payload)
        response = self._api_connector.send(api_call, payload)
        return saved_filters_payload.CreateResponse.from_json(response.text).to_saved_filter()
    #
    # def update(self, user: User) -> User:
    #     assert user.id is not None, "User ID has to be provided"
    #
    #     api_call = users.update_user(user.id)
    #     payload = as_dict(
    #         users_payload.UpdateRequest(
    #             user_name=user.username,
    #             user_full_name=user.full_name,
    #             user_email=user.email,
    #             role=user.role,
    #             email_service=user.email_service,
    #             email_product=user.email_product,
    #         )
    #     )
    #     response = self._api_connector.send(api_call, payload)
    #     return users_payload.UpdateResponse.from_json(response.text).to_user()
    #
    def delete(self, saved_filter_id: int) -> bool:
        api_call = saved_filters.delete_saved_filter(saved_filter_id)
        response = self._api_connector.send(api_call)
        return response.http_status_code == HTTPStatus.NO_CONTENT
