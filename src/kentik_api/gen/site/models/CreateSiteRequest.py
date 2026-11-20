# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .Site import Site


class CreateSiteRequest(BaseModel):
    """
    CreateSiteRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    site: Site = Field(validation_alias="site")
