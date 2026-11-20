# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PolicyFiltersSavedFilter(BaseModel):
    """
    PolicyFiltersSavedFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the saved filter. Saved filters are pre-defined filters that can be used in the policy.",
    )

    not_: Optional[bool] = Field(
        validation_alias="not",
        serialization_alias="not",
        default=None,
        description="If true, the saved filter will be negated.",
    )
