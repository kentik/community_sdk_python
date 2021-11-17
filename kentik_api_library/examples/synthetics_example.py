"""
Examples of using the Synthetics API
"""

import logging
import os
import sys
from typing import List, Tuple, Any

from kentik_api import KentikAPI
from kentik_api.grpc.kentik.synthetics.v202101beta1.synthetics_pb2 import ListTestsRequest, ListTestsResponse, Test


logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def print_indented(v: Any, level: int) -> None:
    INDENT = " " * level * 2

    for field_name, field in v.__dict__.items():
        if callable(field):
            continue
        if not hasattr(field, "__dict__"):
            print(INDENT, field_name, ":", field)
        else:
            print(INDENT, field_name)
            print_indented(field, level + 1)


def run_list_tests() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    items = client.synthetics.tests
    for i, test in enumerate(items):
        print(f"{i}.")
        print_indented(test, 0)
        print()


def run_list_agents() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    agents = client.synthetics.agents
    for i, item in enumerate(agents):
        print(f"{i}.")
        print_indented(item, 0)
        print()


if __name__ == "__main__":
    run_list_tests()
    # run_list_agents()
