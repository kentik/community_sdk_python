# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .IdentityPredicate import IdentityPredicate
from .LabelPredicate import LabelPredicate
from .StringPredicate import StringPredicate


class ProducerPredicates(BaseModel):
    """
    ProducerPredicates model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    originId: Optional[IdentityPredicate] = Field(
        validation_alias="originId", default=None
    )

    originName: Optional[StringPredicate] = Field(
        validation_alias="originName", default=None
    )

    originLabels: Optional[LabelPredicate] = Field(
        validation_alias="originLabels", default=None
    )
