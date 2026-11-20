# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ProducerPredicates import ProducerPredicates
from .ScopedClause import ScopedClause


class ContextFilterConjunction(BaseModel):
    """
    ContextFilterConjunction model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    clauses: Optional[List[Optional[ScopedClause]]] = Field(
        validation_alias="clauses", default=None
    )

    producerPredicates: Optional[ProducerPredicates] = Field(
        validation_alias="producerPredicates", default=None
    )
