# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class BatchReplaceAll(BaseModel):
    """
    The result of replace_all.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    requested: Optional[bool] = Field(
        validation_alias="requested", default=None, description="replace_all was set."
    )

    deletes_performed: Optional[int] = Field(
        validation_alias="deletes_performed",
        default=None,
        description="Values deleted because the batch did not upsert them.",
    )

    successful: Optional[bool] = Field(
        validation_alias="successful",
        default=None,
        description="False when something stopped those deletes.",
    )
