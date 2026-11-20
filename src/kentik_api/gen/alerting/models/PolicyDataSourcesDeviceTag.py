# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class PolicyDataSourcesDeviceTag(BaseModel):
    """
    PolicyDataSourcesDeviceTag model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the device tag to include in the policy.",
    )

    values: Optional[List[str]] = Field(
        validation_alias="values",
        default=None,
        description="The values of the device tag to include in the policy. Has to contain at least one value.",
    )
