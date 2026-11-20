# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PackageServiceUpdatePackageBody(BaseModel):
    """
    UpdatePackageRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    package: Optional[Dict[str, Any]] = Field(
        validation_alias="package", default=None, description="Package"
    )
