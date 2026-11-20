# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Helpers for the V5-backed `client.v5` calls.

They call the generated operations and never send HTTP themselves, so every
request still goes through the shared runtime.
"""

from __future__ import annotations

import base64
import binascii
import json
import math
import re
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from kentik_api.core.api_config import _is_timeout_failure
from kentik_api.errors import HTTPException, KentikError, TransportError
from kentik_api.gen.v5.models import (
    BatchDelete,
    BatchPart,
    BatchResponse,
    BatchStatus,
    BatchUpsert,
    ChartResponse,
)

if TYPE_CHECKING:
    from kentik_api.client import KentikAPI

BATCH_PART_LIMIT = 4_000_000

_DATA_URI = re.compile(
    r"data:(?P<mime>[^;,]+)(?:;[^;,]+)*;base64,(?P<data>.*)", re.DOTALL
)


@dataclass(frozen=True)
class ChartImage:
    image_type: str
    """The MIME type, for example `image/png` or `image/svg+xml`."""
    data: bytes


def decode_chart(response: ChartResponse) -> ChartImage:
    """Decodes the data URI of a `client.v5.top_x_chart` response."""
    if not response.dataUri:
        raise _unusable("no data URI")
    match = _DATA_URI.fullmatch(response.dataUri)
    if match is None:
        raise _unusable("not a base64 data URI")
    try:
        data = base64.b64decode(match["data"], validate=True)
    except binascii.Error:
        raise _unusable("not valid base64") from None
    return ChartImage(match["mime"], data)


def _unusable(problem: str) -> HTTPException:
    return HTTPException(
        502,
        f"TopXChart returned an unusable chart: {problem}.",
        details={"problem": problem},
    )


class BatchSendError(KentikError):
    """A batch part failed. The parts before it were sent, and none is resent."""

    def __init__(self, guid: str | None, sent: int, cause: object):
        self.guid = guid
        self.sent = sent
        super().__init__(
            f"Batch part {sent + 1} failed after {sent} part(s) were sent "
            f"(guid {guid}): {cause}"
        )


class BatchWaitTimeout(KentikError):
    """The batch did not complete within the time limit."""

    def __init__(self, guid: str, last_status: BatchStatus | None):
        self.guid = guid
        self.last_status = last_status
        super().__init__(f"Batch {guid} did not complete within the time limit.")


def _wire_size(item: Any) -> int:
    # json.dumps's default separators are wider than httpx's, so this never undercounts.
    return len(json.dumps(item.model_dump(by_alias=True, exclude_unset=True)).encode())


def split_batch(
    upserts: Sequence[BatchUpsert],
    deletes: Sequence[BatchDelete] = (),
    *,
    replace_all: bool = False,
    max_bytes: int = BATCH_PART_LIMIT,
) -> list[BatchPart]:
    """Packs upserts, then deletes, into parts of at most `max_bytes` each.

    Only the last part is `complete`. The API applies deletes after the last
    part arrives, so their position does not change the result.
    """
    # The largest empty part: a guid goes into every part after the first.
    overhead = _wire_size(
        BatchPart(
            replace_all=replace_all,
            complete=False,
            upserts=[],
            deletes=[],
            guid="x" * 64,
        )
    )
    budget = max_bytes - overhead
    parts: list[BatchPart] = []
    current: dict[str, list[Any]] = {"upserts": [], "deletes": []}
    used = 0
    for kind, items in (("upserts", upserts), ("deletes", deletes)):
        for item in items:
            size = _wire_size(item) + 2  # the separator before it
            if size > budget:
                raise ValueError(
                    f"A {kind[:-1]} of {size} bytes is larger than max_bytes allows."
                )
            if used + size > budget:
                parts.append(_part(current, replace_all, complete=False))
                current, used = {"upserts": [], "deletes": []}, 0
            current[kind].append(item)
            used += size
    parts.append(_part(current, replace_all, complete=True))
    return parts


def _part(items: dict[str, list[Any]], replace_all: bool, complete: bool) -> BatchPart:
    part = BatchPart(replace_all=replace_all, complete=complete)
    if items["upserts"]:
        part.upserts = items["upserts"]
    if items["deletes"]:
        part.deletes = items["deletes"]
    return part


def send_batch(send: Callable[..., BatchResponse], parts: Sequence[BatchPart]) -> str:
    """Sends the parts in order with `send(data=part)` and returns the batch guid.

    `send` is `client.v5.batch_tags`, or `batch_populators` with the dimension
    bound, for example `functools.partial(client.v5.batch_populators,
    dimensionName="c_x")`. A failed part raises `BatchSendError`; nothing is resent.
    """
    if not parts:
        raise ValueError("send_batch got no parts.")
    guid: str | None = None
    for sent, part in enumerate(parts):
        if guid is not None:
            part = part.model_copy()
            part.guid = guid  # an assignment, so model_dump(exclude_unset) sends it
        try:
            response = send(data=part)
        except KentikError as exc:
            raise BatchSendError(guid, sent, exc) from exc
        if guid is None:
            if not response.guid:
                raise BatchSendError(None, sent + 1, "the response has no guid")
            guid = response.guid
    assert guid is not None
    return guid


def wait_for_batch(
    client: KentikAPI, guid: str, *, timeout: float = 600.0, interval: float = 5.0
) -> BatchStatus:
    """Polls `client.v5.batch_status` until the batch is complete.

    Deadlines are cooperative. A request timeout observed at or after expiry
    raises `BatchWaitTimeout` with its original cause and latest status.
    Other errors propagate unchanged. The batch is never resent.
    """
    for field, value in (("timeout", timeout), ("interval", interval)):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{field} must be finite and positive, got {value!r}")
    deadline = time.monotonic() + timeout
    api_config = client.v5_api_config._with_rest_deadline(deadline)
    status: BatchStatus | None = None
    while True:
        if time.monotonic() >= deadline:
            raise BatchWaitTimeout(guid, status)
        try:
            status = client.v5.batch_status(guid=guid, api_config_override=api_config)
        except TransportError as exc:
            if _is_timeout_failure(exc) and time.monotonic() >= deadline:
                raise BatchWaitTimeout(guid, status) from exc
            raise
        if time.monotonic() >= deadline:
            raise BatchWaitTimeout(guid, status)
        if status.is_complete:
            return status
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise BatchWaitTimeout(guid, status)
        time.sleep(min(interval, remaining))
