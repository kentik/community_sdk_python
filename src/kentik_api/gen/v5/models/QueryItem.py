# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Query import Query


class QueryItem(BaseModel):
    """
    One query and its series options. Keeps every field it gets, so JSON copied from Data Explorer reaches the API unchanged.
    """

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "extra": "allow",
    }

    query: Query = Field(validation_alias="query")

    bucket: Optional[str] = Field(
        validation_alias="bucket",
        default=None,
        description="The series name. The response groups rows by it.",
    )

    bucketIndex: Optional[int] = Field(
        validation_alias="bucketIndex",
        default=None,
        description="The index of the query in its bucket, 0 or more.",
    )

    isOverlay: Optional[bool] = Field(
        validation_alias="isOverlay",
        default=None,
        description="Treats the query as an overlay. Chart and URL only.",
    )
