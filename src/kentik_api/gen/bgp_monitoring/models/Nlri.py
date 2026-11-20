# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Afi import Afi
from .Safi import Safi


class Nlri(BaseModel):
    """
    Nlri
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    afi: Afi = Field(validation_alias="afi")

    safi: Safi = Field(validation_alias="safi")

    prefix: Optional[str] = Field(
        validation_alias="prefix",
        default=None,
        description="Actual prefix data (format depends on AFI)",
    )
