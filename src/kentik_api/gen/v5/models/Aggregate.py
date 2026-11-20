# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Aggregate(BaseModel):
    """
    One aggregate column.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="The column name, for example avg_bits_per_sec.",
    )

    column: Optional[str] = Field(
        validation_alias="column",
        default=None,
        description="The KDE column to aggregate, for example f_sum_both_bytes.",
    )

    fn: Optional[str] = Field(
        validation_alias="fn",
        default=None,
        description="The function: sum, average, percentile, max, composite, exponent, modulus, greaterThan, greaterThanEquals, lessThan, lessThanEquals, equals, or notEquals.",
    )

    rank: Optional[int] = Field(
        validation_alias="rank",
        default=None,
        description="The percentile, 5 to 99, when fn is percentile.",
    )

    sample_rate: Optional[float] = Field(
        validation_alias="sample_rate",
        default=None,
        description="A factor applied to every value.",
    )

    raw: Optional[bool] = Field(
        validation_alias="raw", default=None, description="Returns the raw values."
    )
