# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ConfigRunoutConfig(BaseModel):
    """
    RunoutConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    strategy: Optional[str] = Field(
        validation_alias="strategy", default=None, description="Strategy for runout"
    )

    warnQty: Optional[int] = Field(
        validation_alias="warnQty",
        default=None,
        description="Warning quantity for runout",
    )

    critQty: Optional[int] = Field(
        validation_alias="critQty",
        default=None,
        description="Critical quantity for runout",
    )
