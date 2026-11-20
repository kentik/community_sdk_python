# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Site import Site


class CreateSiteResponse(BaseModel):
    """
    CreateSiteResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    site: Optional[Site] = Field(validation_alias="site", default=None)
