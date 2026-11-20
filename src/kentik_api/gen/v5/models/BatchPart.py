# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BatchDelete import BatchDelete
from .BatchUpsert import BatchUpsert


class BatchPart(BaseModel):
    """
    One part of a batch of flow tags or populators.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    replace_all: bool = Field(
        validation_alias="replace_all",
        description="If true, the API deletes every tag or populator that the batch does not upsert. Send the same value in every part.",
    )

    complete: bool = Field(
        validation_alias="complete", description="True on the last part only."
    )

    upserts: Optional[List[Optional[BatchUpsert]]] = Field(
        validation_alias="upserts",
        default=None,
        description="The values to create or update.",
    )

    deletes: Optional[List[Optional[BatchDelete]]] = Field(
        validation_alias="deletes", default=None, description="The values to delete."
    )

    guid: Optional[str] = Field(
        validation_alias="guid",
        default=None,
        description="Empty on the first part. The guid from the first response on every later part.",
    )
