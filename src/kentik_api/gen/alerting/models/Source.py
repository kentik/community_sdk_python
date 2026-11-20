# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .PolicyType import PolicyType


class Source(BaseModel):
    """
    Source model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    policyType: PolicyType = Field(validation_alias="policyType")

    id: str = Field(
        validation_alias="id",
        description="The ID of the policy, can be integer ID, UUID or any other format.",
    )
