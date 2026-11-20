# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Populator import Populator


class CustomDimension(BaseModel):
    """
    CustomDimension model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the custom dimension.",
    )

    name: str = Field(
        validation_alias="name",
        description="The name of the custom dimension. Must start with 'c_'. Valid characters: alphanumeric dashes and underscores. Length: min=1, max=20.",
    )

    type: str = Field(
        validation_alias="type",
        description="should be an enum instead? but also YAGNI\n\nType of the custom dimension (valid values: 'string' or 'uint32')",
    )

    description: str = Field(
        validation_alias="description",
        description="The name to be displayed of the custom dimension. Valid characters: alphanumeric spaces, dashes and underscores. Length: min=2, max=30.",
    )

    populators: Optional[List[Optional[Populator]]] = Field(
        validation_alias="populators",
        default=None,
        description="Populators associated with this custom dimension.",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId",
        default=None,
        description="The system-assigned ID of the customer.",
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Date-time of populator creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Date-time of most-recent populator edit, in UTC.",
    )
