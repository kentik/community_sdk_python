# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Bulk-sync flow tags with the V5 batch API (port of 1.x batch_example.py).

This writes to your account, so it only prints the parts unless you pass
`--send`. replace_all stays False: tags that the batch does not name are kept.

    uv run python -m examples.v5.batch          # dry run
    uv run python -m examples.v5.batch --send   # sends, then waits
"""

import sys

from kentik_api.client import KentikAPI
from kentik_api.gen.v5.models import BatchCriterion, BatchDelete, BatchUpsert
from kentik_api.v5_tools import send_batch, split_batch, wait_for_batch


def main(argv: list[str] | None = None) -> None:
    """Preview a flow tag batch or send it when requested.

    Args:
        argv: Command arguments, or None to read the command line.
    """
    send = "--send" in (sys.argv[1:] if argv is None else argv)
    upserts = [
        BatchUpsert(
            value="example_tag",
            criteria=[BatchCriterion(direction="src", addr=["192.0.2.77/32"])],
        )
    ]
    deletes = [BatchDelete(value="example_tag_to_delete")]
    parts = split_batch(upserts, deletes, replace_all=False)
    print(
        f"{len(parts)} part(s), {len(upserts)} upsert(s), "
        f"{len(deletes)} delete(s)."
    )
    if not send:
        print("Dry run. Pass --send to send the batch.")
        return

    client = KentikAPI()
    guid = send_batch(client.v5.batch_tags, parts)
    status = wait_for_batch(client, guid, timeout=300, interval=5)
    print(f"Batch {guid}: complete={status.is_complete}")
    if status.upserts is not None:
        print(f"  upserts applied: {status.upserts.applied}")
    if status.deletes is not None:
        print(f"  deletes applied: {status.deletes.applied}")


if __name__ == "__main__":
    main()
