# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class NmsContextAlarmTarget(BaseModel):
    """
    NmsContextAlarmTarget model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    fields: Optional[Dict[str, Any]] = Field(validation_alias="fields", default=None)

    tags: Optional[Dict[str, Any]] = Field(validation_alias="tags", default=None)
