# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BatchDeleteCounts import BatchDeleteCounts
from .BatchReplaceAll import BatchReplaceAll
from .BatchStatusCustomDimension import BatchStatusCustomDimension
from .BatchStatusUser import BatchStatusUser
from .BatchUpsertCounts import BatchUpsertCounts


class BatchStatus(BaseModel):
    """
    The progress of a batch.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    guid: Optional[str] = Field(
        validation_alias="guid", default=None, description="The batch ID."
    )

    custom_dimension: Optional[BatchStatusCustomDimension] = Field(
        validation_alias="custom_dimension", default=None
    )

    is_multipart: Optional[bool] = Field(
        validation_alias="is_multipart",
        default=None,
        description="The batch has more than one part.",
    )

    is_pending: Optional[bool] = Field(
        validation_alias="is_pending",
        default=None,
        description="The batch waits to be processed.",
    )

    is_complete: Optional[bool] = Field(
        validation_alias="is_complete",
        default=None,
        description="Every part arrived and was processed.",
    )

    number_of_parts: Optional[int] = Field(
        validation_alias="number_of_parts",
        default=None,
        description="The parts received so far.",
    )

    user: Optional[BatchStatusUser] = Field(validation_alias="user", default=None)

    upserts: Optional[BatchUpsertCounts] = Field(
        validation_alias="upserts", default=None
    )

    deletes: Optional[BatchDeleteCounts] = Field(
        validation_alias="deletes", default=None
    )

    replace_all: Optional[BatchReplaceAll] = Field(
        validation_alias="replace_all", default=None
    )

    batch_date: Optional[str] = Field(
        validation_alias="batch_date",
        default=None,
        description="When the first part arrived.",
    )
