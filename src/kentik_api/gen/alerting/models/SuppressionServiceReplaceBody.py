# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict

from pydantic import BaseModel, Field


class SuppressionServiceReplaceBody(BaseModel):
    """
    SuppressionServiceReplaceBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    suppression: Dict[str, Any] = Field(
        validation_alias="suppression",
        description="Different matching constraints are ANDed. Values within sources\nand severities are alternatives. At least one non-empty matching constraint is\nrequired; a display name, comment, or strictness flag alone is insufficient.",
    )
