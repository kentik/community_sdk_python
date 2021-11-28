# pylint: disable=redefined-outer-name
"""
Example of using the users API
"""

import logging

from kentik_api import KentikAPI, User
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
    user = User.new(
        username="testuser",
        full_name="Test User",
        user_email="test@user.example",
        role="Member",
        user_password="test_password",
        email_service=True,
        email_product=True,
    )
    created = client.users.create(user)
    print(created.__dict__)
    print()

    print("### GET_ALL")
    all_users = client.users.get_all()
    for i in all_users:
        print(i.__dict__)
    print()

    print("### UPDATE")
    created.full_name = "User Testing"
    got = client.users.update(created)
    print(got.__dict__)
    print()

    print("### GET")
    got = client.users.get(created.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.users.delete(created.id)
    print(deleted)


if __name__ == "__main__":
    run_crud()
