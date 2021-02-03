"""Examples of handling errors raised in kentik_api library. Only a subset of possible errors is presented."""

import os
import sys
import logging

from typing import Tuple

from kentik_api import KentikAPI, AuthError, NotFoundError, IncompleteObjectError, Device, RateLimitExceededError

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def handle_errors() -> None:
    bad_email = "not_an_email"
    bad_token = "dummy_token"

    client = KentikAPI(bad_email, bad_token)

    try:
        users = client.users.get_all()

    except AuthError:
        email, token = get_auth_email_token()
        client = KentikAPI(email, token)

    users = client.users.get_all()

    try:
        fake_id = -1
        user = client.users.get(fake_id)  # there is no user with -1 ID

    except NotFoundError:
        print("User with ID: {} not exist".format(fake_id))

    new_device = Device(plan_id=10)  # device without required fields to create it
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
