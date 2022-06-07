"""
Example of using the batch API
"""

import logging

from examples.utils import pretty_print
from kentik_api import BatchOperationPart, Criterion, Deletion, KentikAPI, Upsert
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### BATCH ON FLOW TAGS")
    criterion = Criterion(["192.168.0.77"], Criterion.Direction.SRC)
    upsert = Upsert("test_value", [criterion])
    deletion = Deletion("value_to_delete")
    batch = BatchOperationPart(False, True, [upsert], [deletion])
    status = client.batch.batch_operation_on_flow_tags(batch)
    pretty_print(status)
    print()

    print("### GET STATUS")
    got = client.batch.get_status(status.guid)
    pretty_print(got)
    print()


if __name__ == "__main__":
    run_crud()
