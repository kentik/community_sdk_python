# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .v202505PolicyType import v202505PolicyType


class v202505Source(BaseModel):
    """
    v202505Source model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    policyType: v202505PolicyType = Field(validation_alias="policyType")

    id: str = Field(
        validation_alias="id",
        description="The ID of the policy, can be integer ID, UUID or any other format.",
    )
