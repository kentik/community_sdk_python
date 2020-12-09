from http import HTTPStatus
from typing import List

from kentik_api.api_calls import users
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.public.user import User
from kentik_api.requests_payload import users_payload
from kentik_api.requests_payload.as_dict import as_dict


class UsersAPI:
    """Exposes Kentik API operations related to users. """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def get_all(self) -> List[User]:
        api_call = users.get_users()
        response = self._api_connector.send(api_call)
        return users_payload.GetAllResponse.from_json(response.text).to_users()

    def get(self, user_id: int) -> User:
        api_call = users.get_user_info(user_id)
        response = self._api_connector.send(api_call)
        return users_payload.GetResponse.from_json(response.text).to_user()

    def create(self, user: User) -> User:
        api_call = users.create_user()
        payload = {
            'user': as_dict(users_payload.CreateRequest(
                user_name=user.username,
                user_full_name=user.full_name,
                user_email=user.email,
                user_password=user.password,
                role=user.role,
                email_service=user.email_service,
                email_product=user.email_product,
                )),
        }
        response = self._api_connector.send(api_call, payload)
        return users_payload.CreateResponse.from_json(response.text).to_user()

    def update(self, user: User) -> User:
        api_call = users.update_user(user.id)
        payload = {
            'user': as_dict(users_payload.UpdateRequest(
                user_name=user.username,
                user_full_name=user.full_name,
                user_email=user.email,
                role=user.role,
                email_service=user.email_service,
                email_product=user.email_product,
                id=user.id,
                last_login=user.last_login,
                created_date=user.created_date,
                updated_date=user.updated_date,
                company_id=user.company_id,
                user_api_token=user.api_token,
                filters=user.filters,
                saved_filters=user.saved_filters,
            )),
        }
        response = self._api_connector.send(api_call, payload)
        return users_payload.UpdateResponse.from_json(response.text).to_user()

    def delete(self, user_id: int) -> bool:
        api_call = users.delete_user(user_id)
        response = self._api_connector.send(api_call)
        return response.http_status_code == HTTPStatus.NO_CONTENT
