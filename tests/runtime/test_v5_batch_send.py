# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""send_batch() sends parts in order and never resends one (spec 005, FR-014)."""

from __future__ import annotations

import pytest

from kentik_api.errors import HTTPException
from kentik_api.gen.v5.models import BatchPart, BatchResponse, BatchUpsert
from kentik_api.v5_tools import BatchSendError, send_batch


def _parts(count: int) -> list[BatchPart]:
    return [
        BatchPart(
            replace_all=False,
            complete=n == count - 1,
            upserts=[BatchUpsert(value=f"tag-{n}")],
        )
        for n in range(count)
    ]


class _Recorder:
    def __init__(self, fail_on: int | None = None):
        self.sent: list[BatchPart] = []
        self.fail_on = fail_on

    def __call__(self, *, data: BatchPart) -> BatchResponse:
        self.sent.append(data)
        if len(self.sent) == self.fail_on:
            raise HTTPException(500, "batch store failed")
        return BatchResponse(message="queued", guid="g-1")


def test_the_first_guid_goes_into_every_later_part():
    send = _Recorder()

    guid = send_batch(send, _parts(3))

    assert guid == "g-1"
    assert [part.guid for part in send.sent] == [None, "g-1", "g-1"]
    later = send.sent[1].model_dump(by_alias=True, exclude_unset=True)
    assert later["guid"] == "g-1"


def test_a_failed_part_stops_the_batch_and_nothing_is_resent():
    send = _Recorder(fail_on=2)

    with pytest.raises(BatchSendError) as exc:
        send_batch(send, _parts(3))

    assert exc.value.sent == 1
    assert exc.value.guid == "g-1"
    assert isinstance(exc.value.__cause__, HTTPException)
    assert len(send.sent) == 2


def test_the_callers_parts_are_not_changed():
    parts = _parts(2)

    send_batch(_Recorder(), parts)

    assert parts[1].guid is None


def test_no_parts_is_refused():
    with pytest.raises(ValueError, match="no parts"):
        send_batch(_Recorder(), [])
