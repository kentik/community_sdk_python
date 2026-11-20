# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BulkActionItemState import BulkActionItemState


class BulkActionItemStatus(BaseModel):
    """
    BulkActionItemStatus
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="ID of the item, such as a test ID.",
    )

    state: Optional[BulkActionItemState] = Field(validation_alias="state", default=None)

    error: Optional[str] = Field(
        validation_alias="error",
        default=None,
        description="Why the item failed or was not processed. Empty unless `state` is FAILED.",
    )

    errorType: Optional[str] = Field(
        validation_alias="errorType",
        default=None,
        description="Category of the error, when the item failed during processing. Empty for items rejected by request validation.",
    )

    field: Optional[str] = Field(
        validation_alias="field",
        default=None,
        description="The field that failed validation, when the item was rejected by request validation. Empty for items that failed during processing.",
    )
