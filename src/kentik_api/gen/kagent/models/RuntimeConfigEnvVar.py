# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class RuntimeConfigEnvVar(BaseModel):
    """
    EnvVar
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="Name of the environment variable.",
    )

    value: Optional[str] = Field(
        validation_alias="value",
        default=None,
        description="Value of the environment variable.",
    )

    origin: Optional[str] = Field(
        validation_alias="origin",
        default=None,
        description="indicates the config layer that provided this variable\n\nConfig layer that provided this variable.",
    )
