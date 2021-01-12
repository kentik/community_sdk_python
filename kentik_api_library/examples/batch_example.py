"""
Example of using the batch API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, Criterion, Upsert, Deletion, BatchOperationPart

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
    Runs example API calls and prints responses
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### BATCH ON FLOW TAGS")
    criterion = Criterion(["192.168.0.77"], Criterion.Direction.SRC)
    upsert = Upsert("test_value", [criterion])
    deletion = Deletion("value_to_delete")
    batch = BatchOperationPart(False, True, [upsert], [deletion])
    status = client.batch.batch_operation_on_flow_tags(batch)
    print(status.__dict__)
    print()

    print("### GET STATUS")
    got = client.batch.get_status(status.guid)
    print(got.__dict__)
    print()


if __name__ == "__main__":
    run_crud()
