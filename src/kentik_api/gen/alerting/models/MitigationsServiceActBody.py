# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field


class MitigationsServiceActBody(BaseModel):
    """
    MitigationsServiceActBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ids: List[str] = Field(
        validation_alias="ids", description="The IDs of the mitigations to act on."
    )
