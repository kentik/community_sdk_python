"""
Examples of using the Synthetics API
"""

import logging
from typing import Any

from kentik_api import KentikAPI
from kentik_api.utils import get_credentials
from kentik_api.generated.kentik.synthetics.v202101beta1.synthetics_pb2 import ListTestsRequest, ListTestsResponse, Test


logging.basicConfig(level=logging.INFO)


def pretty_print(v: Any, level: int) -> None:
    INDENT = " " * level * 2

    for field_name, field in v.__dict__.items():
        if callable(field):
            continue
        if not hasattr(field, "__dict__"):
            print(f"{INDENT}{field_name}: {field}")
        else:
            print(f"{INDENT}{field_name}")
            pretty_print(field, level + 1)


def run_list_tests() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    items = client.synthetics.tests
    for test in items:
        print(test.id)
        pretty_print(test, 1)
        print()


def run_list_agents() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    agents = client.synthetics.agents
    for agent in agents:
        print(agent.id)
        pretty_print(agent, 1)
        print()


if __name__ == "__main__":
    run_list_tests()
    # run_list_agents()
