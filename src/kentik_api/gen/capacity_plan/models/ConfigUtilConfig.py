# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ConfigUtilConfig(BaseModel):
    """
    UtilConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    aggregate: Optional[str] = Field(
        validation_alias="aggregate",
        default=None,
        description="Aggregate for utilization",
    )

    warnPct: Optional[int] = Field(
        validation_alias="warnPct",
        default=None,
        description="Warning percentage for utilization",
    )

    critPct: Optional[int] = Field(
        validation_alias="critPct",
        default=None,
        description="Critical percentage for utilization",
    )
