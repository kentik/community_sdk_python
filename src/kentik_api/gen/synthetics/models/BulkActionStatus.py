# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BulkActionItemStatus import BulkActionItemStatus
from .BulkActionState import BulkActionState


class BulkActionStatus(BaseModel):
    """
    BulkActionStatus

    absent when nothing was dispatched, so no workflow exists to poll
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    workflowId: Optional[str] = Field(
        validation_alias="workflowId",
        default=None,
        description="ID to use when requesting the status of the bulk action. Empty when nothing was started, for example because every item was rejected; there is then nothing to poll.",
    )

    state: Optional[BulkActionState] = Field(validation_alias="state", default=None)

    startTime: Optional[str] = Field(
        validation_alias="startTime",
        default=None,
        description="When the bulk action started running (UTC). Not included in the reply to the request that started it.",
    )

    endTime: Optional[str] = Field(
        validation_alias="endTime",
        default=None,
        description="When the bulk action finished (UTC). Set only after it has finished, so its presence means no further changes will occur.",
    )

    totalCount: Optional[int] = Field(
        validation_alias="totalCount",
        default=None,
        description="Number of distinct items in the request. Counts and `items` may be omitted after the bulk action has finished and per-item results are no longer available; an omitted count means unknown, while 0 means none.",
    )

    succeededCount: Optional[int] = Field(
        validation_alias="succeededCount",
        default=None,
        description="Number of items processed successfully.",
    )

    failedCount: Optional[int] = Field(
        validation_alias="failedCount",
        default=None,
        description="Number of items that failed validation or processing.",
    )

    pendingCount: Optional[int] = Field(
        validation_alias="pendingCount",
        default=None,
        description="Number of items not yet processed.",
    )

    items: Optional[List[Optional[BulkActionItemStatus]]] = Field(
        validation_alias="items",
        default=None,
        description="Items that failed, with the reason for each. Items that succeeded or are still pending are not listed. An item may appear more than once if several of its fields failed validation.",
    )

    skippedCount: Optional[int] = Field(
        validation_alias="skippedCount",
        default=None,
        description="Number of items in `skipped`. Reported only in the reply to the request that started the bulk action.",
    )

    skipped: Optional[List[Optional[BulkActionItemStatus]]] = Field(
        validation_alias="skipped",
        default=None,
        description="Items that were not processed, with the reason for each: for example, IDs that do not exist or that no requested change applies to, or valid items held back because the request was rejected. Reported only in the reply to the request that started the bulk action.",
    )
