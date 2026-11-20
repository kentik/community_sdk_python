# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .NetworkScope import NetworkScope
from .SubjectPredicates import SubjectPredicates


class ScopedClause(BaseModel):
    """
    A scoped AND-group: one or more NetworkEntity contexts plus field predicates.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    networkScope: Optional[List[Optional[NetworkScope]]] = Field(
        validation_alias="networkScope",
        default=None,
        description="Which NetworkEntity context to evaluate predicates against.\n\nWhen empty, NETWORK_SCOPE_ANY is used. This evaluates the predicate against\neach supported subject scope (root, source, destination, and adjacent).\n\nWhen multiple values are set, the clause matches if any listed scope matches\n(OR across scopes, AND across predicate fields within the clause).",
    )

    predicates: Optional[SubjectPredicates] = Field(
        validation_alias="predicates", default=None
    )
