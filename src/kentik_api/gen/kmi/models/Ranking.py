# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Ranking(BaseModel):
    """
    Ranking
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="Autonomous System Number (ASN)",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="Name of the Autonomous System",
    )

    rank: Optional[int] = Field(
        validation_alias="rank",
        default=None,
        description="Rank of the Autonomous System",
    )

    rankChange: Optional[int] = Field(
        validation_alias="rankChange",
        default=None,
        description="Rank Change of the Autonomous System",
    )

    score: Optional[int] = Field(
        validation_alias="score",
        default=None,
        description="Score of the Autonomous System",
    )

    scoreChange: Optional[int] = Field(
        validation_alias="scoreChange",
        default=None,
        description="Score Change of the Autonomous System",
    )
