from http import HTTPStatus
from typing import List

from kentik_api.api_calls import users
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.types import ID
from kentik_api.public.user import User
from kentik_api.requests_payload import users_payload


class UsersAPI(BaseAPI):
    """Exposes Kentik API operations related to users."""

    def get_all(self) -> List[User]:
        api_call = users.get_users()
        response = self.send(api_call)
        return users_payload.GetAllResponse.from_json(response.text).to_users()

    def get(self, user_id: ID) -> User:
        api_call = users.get_user_info(user_id)
        response = self.send(api_call)
        return users_payload.GetResponse.from_json(response.text).to_user()

    def create(self, user: User) -> User:
        api_call = users.create_user()
        payload = users_payload.CreateRequest(
            user_name=user.username,
            user_full_name=user.full_name,
            user_email=user.email,
            role=user.role,
            email_service=user.email_service,
            email_product=user.email_product,
        )
        response = self.send(api_call, payload)
        return users_payload.CreateResponse.from_json(response.text).to_user()

    def update(self, user: User) -> User:
        api_call = users.update_user(user.id)
        payload = users_payload.UpdateRequest(
            user_name=user.username,
            user_full_name=user.full_name,
            user_email=user.email,
            role=user.role,
            email_service=user.email_service,
            email_product=user.email_product,
        )
        response = self.send(api_call, payload)
        return users_payload.UpdateResponse.from_json(response.text).to_user()

    def delete(self, user_id: ID) -> bool:
        api_call = users.delete_user(user_id)
        response = self.send(api_call)
        return response.http_status_code == HTTPStatus.NO_CONTENT
