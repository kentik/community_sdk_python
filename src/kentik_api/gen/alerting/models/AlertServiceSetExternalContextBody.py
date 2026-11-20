# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .ExternalContext import ExternalContext


class AlertServiceSetExternalContextBody(BaseModel):
    """
    AlertServiceSetExternalContextBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    context: ExternalContext = Field(validation_alias="context")
