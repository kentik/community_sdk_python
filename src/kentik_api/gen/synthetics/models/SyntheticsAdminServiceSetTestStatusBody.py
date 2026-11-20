# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .TestStatus import TestStatus


class SyntheticsAdminServiceSetTestStatusBody(BaseModel):
    """
    SetTestStatusRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: TestStatus = Field(validation_alias="status")
