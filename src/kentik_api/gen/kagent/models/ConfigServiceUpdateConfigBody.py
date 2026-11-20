# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict

from pydantic import BaseModel, Field


class ConfigServiceUpdateConfigBody(BaseModel):
    """
    UpdateConfigRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    config: Dict[str, Any] = Field(validation_alias="config", description="Config")

    mask: str = Field(
        validation_alias="mask",
        description="Attributes of the config to be updated. Attributes not listed keep their current value.",
    )
