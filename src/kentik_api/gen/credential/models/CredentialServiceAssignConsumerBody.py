# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .Consumer import Consumer


class CredentialServiceAssignConsumerBody(BaseModel):
    """
    AssignConsumerRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    consumer: Consumer = Field(validation_alias="consumer")
