# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class NmsStateSet(BaseModel):
    """
    NmsStateSet model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    states: Optional[List[str]] = Field(validation_alias="states", default=None)
