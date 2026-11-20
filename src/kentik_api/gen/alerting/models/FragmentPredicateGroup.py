# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FragmentPredicate import FragmentPredicate


class FragmentPredicateGroup(BaseModel):
    """
    FragmentPredicateGroup model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    and_: Optional[List[Optional[FragmentPredicate]]] = Field(
        validation_alias="and", serialization_alias="and", default=None
    )
