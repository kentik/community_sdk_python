# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Label(BaseModel):
    """
    Label
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique system assigned identifier of the label",
    )

    name: str = Field(
        validation_alias="name",
        description="Label text visible in listing of configuration of objects to which it has been applied",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Optional description of the label, visible only in API responses",
    )

    color: Optional[str] = Field(
        validation_alias="color",
        default=None,
        description="[Hexadecimal code of the color](https://www.color-hex.com/) of the label text background in the portal",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )
