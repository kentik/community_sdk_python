# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ConfigRunoutConfig import ConfigRunoutConfig
from .ConfigUtilConfig import ConfigUtilConfig


class Config(BaseModel):
    """
    Config
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    runout: Optional[ConfigRunoutConfig] = Field(
        validation_alias="runout", default=None
    )

    utilization: Optional[ConfigUtilConfig] = Field(
        validation_alias="utilization", default=None
    )
