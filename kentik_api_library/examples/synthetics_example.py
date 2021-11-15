"""
Examples of using the Synthetics API
"""

import logging
import os
import sys
from typing import Tuple

from kentik_api import KentikAPI


logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_list_tests() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    tests = client.synthetics.tests
    for item in tests:
        print(item.__dict__)
        print()


def run_list_agents() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    agents = client.synthetics.agents
    for item in agents:
        print(item)
        print()


if __name__ == "__main__":
    run_list_tests()
    run_list_agents()
