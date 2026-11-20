# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CloudType import CloudType


class CloudSubnet(BaseModel):
    """
    CloudSubnet model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[CloudType] = Field(validation_alias="type", default=None)

    subnets: Optional[List[str]] = Field(
        validation_alias="subnets", default=None, description="Subnet masks"
    )
