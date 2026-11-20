# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ContextFilterConjunction import ContextFilterConjunction


class ContextFilter(BaseModel):
    """
    ContextFilter operates on materialized observation.subject attributes as
    recorded in context inputs.

    Used by Alert Manager alarm search and suppressions (context_filter on list and
    suppression config). Does not apply to ContextService List, which filters by
    input_types and producer_types on stored rows instead.

    Subject is the only filterable part of ContextInput for now. Producer-based
    filters (type, originating definition, API request metadata) are likely needed
    later.

    Disjunctive normal form:
    - conjunctions are ORed
    - clauses within a conjunction are ANDed
    - predicate fields within a clause are ANDed

    Each ScopedClause evaluates all set predicate fields against the same NetworkEntity
    context (see NetworkScope). For example, device_id and ip_address in a clause with
    NETWORK_SCOPE_DESTINATION both refer to subject.network.destination.*.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    conjunctions: Optional[List[Optional[ContextFilterConjunction]]] = Field(
        validation_alias="conjunctions",
        default=None,
        description='Example - (device_labels contains "prod" AND site_name = "NY") OR (device_id = "88903"):\n  conjunctions: [\n    { clauses: [{ predicates: { device_labels: { equals: "prod" }, site_name: { equals: "NY" } } }] },\n    { clauses: [{ predicates: { device_id: { equals: "88903" } } }] }\n  ]\n\nExample - root device AND destination IP in CIDR (different scopes, ANDed):\n  conjunctions: [{\n    clauses: [\n      { network_scope: [NETWORK_SCOPE_ROOT], predicates: { device_id: { equals: "88903" } } },\n      { network_scope: [NETWORK_SCOPE_DESTINATION], predicates: { ip_address: { within: "10.0.0.0/8" } } }\n    ]\n  }]',
    )
