"""Examples of handling errors raised in kentik_api library. Only a subset of possible errors is presented."""

import logging

from kentik_api import AuthError, Device, IncompleteObjectError, KentikAPI, NotFoundError, RateLimitExceededError
from kentik_api.public.types import ID
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def handle_errors() -> None:
    bad_email = "not_an_email"
    bad_token = "dummy_token"

    client = KentikAPI(bad_email, bad_token)

    try:
        users = client.users.get_all()

    except AuthError:
        email, token = get_credentials()
        client = KentikAPI(email, token)

    users = client.users.get_all()

    try:
        fake_id = ID("-1")
        client.users.get(fake_id)  # there is no user with -1 ID

    except NotFoundError:
        print("User with ID: {} not exist".format(fake_id))

    new_device = Device(plan_id=ID("10"))  # device without required fields to create it
    try:
        client.devices.create(new_device)
    except IncompleteObjectError:
        print("Cannot create device")

    for _ in range(100):
        try:
            client.users.get(users[0].id)
        except RateLimitExceededError:
            print("Requests rate limit exceeded")


if __name__ == "__main__":
    handle_errors()
