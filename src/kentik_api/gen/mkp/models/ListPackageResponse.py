# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Package import Package


class ListPackageResponse(BaseModel):
    """
    ListPackageResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    packages: Optional[List[Optional[Package]]] = Field(
        validation_alias="packages", default=None
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="The number of invalid packages, for troubleshooting. Should be zero.",
    )
