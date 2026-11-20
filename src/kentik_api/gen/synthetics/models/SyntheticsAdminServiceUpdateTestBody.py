# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class SyntheticsAdminServiceUpdateTestBody(BaseModel):
    """
    UpdateTestRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    test: Optional[Dict[str, Any]] = Field(
        validation_alias="test", default=None, description="Test"
    )
