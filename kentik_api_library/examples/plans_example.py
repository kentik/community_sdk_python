# pylint: disable=redefined-outer-name
"""
Example of using the plans API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, Plan

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_plans = client.plans.get_all()
    for i in all_plans:
        print(i.__dict__)
    print()


if __name__ == "__main__":
    run_crud()
