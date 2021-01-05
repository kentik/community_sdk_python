# pylint: disable=redefined-outer-name
"""
Examples of using the alerting API
"""

import os
import sys
import logging
from kentik_api import KentikAPI, ManualMitigation
from typing import Tuple

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud():
    """Runs example CRUD API calls and prints responses"""

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    # below ManualMitigation values are invalid and will cause error 404
    new_manual_mitigation = ManualMitigation("192.168.0.0/24", "1234", "12345", "20", "This is comment")
    try:
        created = client.alerting.create_manual_mitigation(new_manual_mitigation)
    except KeyError:
        exit()
    print(created)
    print()


if __name__ == "__main__":
    run_crud()
