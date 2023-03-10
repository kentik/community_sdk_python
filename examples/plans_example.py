# pylint: disable=redefined-outer-name
"""
Example of using the plans API
"""

import logging

from examples.utils import pretty_print
from kentik_api import KentikAPI
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_plans = client.plans.get_all()
    pretty_print(all_plans)
    print()


if __name__ == "__main__":
    run_list()
