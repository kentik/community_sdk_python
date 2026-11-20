# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Package import Package


class UpdatePackageResponse(BaseModel):
    """
    UpdatePackageResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    package: Optional[Package] = Field(validation_alias="package", default=None)
