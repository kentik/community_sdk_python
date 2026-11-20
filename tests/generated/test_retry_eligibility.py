# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Which operations a future retry policy may replay (FR-032a, FR-033).

No post-response retry exists yet. This records the rule a later feature must
implement against, derived from each operation's HTTP verb rather than a
hand-kept list, so it stays correct as the schema grows. RFC 9110 section
9.2.2 defines GET, PUT, and DELETE as idempotent; POST and PATCH are not, so
replaying one can create or change something twice.
"""

from __future__ import annotations

import importlib
import json
from collections import Counter
from pathlib import Path

from _discovery import discover_cases, parse_rest_call_metadata

_ROOT = Path(__file__).resolve().parents[2]
RETRY_ELIGIBLE_VERBS = frozenset({"GET", "PUT", "DELETE"})
NEVER_RETRIED_VERBS = frozenset({"POST", "PATCH"})


def _verbs_by_operation() -> dict[str, str]:
    verbs = {}
    for case in discover_cases():
        module = importlib.import_module(case.module_path)
        rest_module = getattr(module, case.rest_module_alias)
        metadata = parse_rest_call_metadata(rest_module, case.rest_function_name)
        assert metadata is not None, case
        verbs[f"{case.wrapper_class}.{case.method_name}"] = metadata.method.upper()
    return verbs


def test_every_operation_verb_falls_on_one_side_of_the_rule():
    unclassified = {
        op: verb
        for op, verb in _verbs_by_operation().items()
        if verb not in RETRY_ELIGIBLE_VERBS | NEVER_RETRIED_VERBS
    }

    assert unclassified == {}


def test_eligibility_split_matches_the_recorded_surface():
    counts = Counter(
        "eligible" if verb in RETRY_ELIGIBLE_VERBS else "never"
        for verb in _verbs_by_operation().values()
    )

    surface = json.loads((_ROOT / "api_surface.json").read_text(encoding="utf-8"))
    recorded = Counter(
        "eligible" if key.split()[0] in RETRY_ELIGIBLE_VERBS else "never"
        for service in surface["services"].values()
        if service["mounted"]
        for key in service["operations"]
    )

    assert counts == recorded
