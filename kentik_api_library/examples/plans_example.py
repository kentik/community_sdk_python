# pylint: disable=redefined-outer-name
"""
Example of using the plans API
"""

import logging

from kentik_api import KentikAPI
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_plans = client.plans.get_all()
    for i in all_plans:
        print(i.__dict__)
    print()


if __name__ == "__main__":
    run_crud()
