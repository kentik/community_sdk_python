# pylint: disable=redefined-outer-name
"""
Example of using the users API
"""

import logging

from examples.utils import pretty_print
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
        email_service=True,
        email_product=True,
    )
    created = client.users.create(user)
    pretty_print(created)
    print()

    print("### GET_ALL")
    all_users = client.users.get_all()
    pretty_print(all_users)
    print()

    print("### UPDATE")
    created.full_name = "User Testing"
    got = client.users.update(created)
    pretty_print(got)
    print()

    print("### GET")
    got = client.users.get(created.id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.users.delete(created.id)
    print(deleted)
    print()


if __name__ == "__main__":
    run_crud()
