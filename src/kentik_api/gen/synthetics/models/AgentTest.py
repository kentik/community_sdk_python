# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AgentTest(BaseModel):
    """
    AgentTest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target", default=None, description="ID of the target agent"
    )

    useLocalIp: Optional[bool] = Field(
        validation_alias="useLocalIp",
        default=None,
        description="Boolean value indicating whether to use local (private) IP address of the target agent",
    )

    reciprocal: Optional[bool] = Field(
        validation_alias="reciprocal",
        default=None,
        description="Boolean value indicating whether to make the test bidirectional",
    )
