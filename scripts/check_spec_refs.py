"""Validate cross-artifact identifier references inside `specs/`.

Renumbering a sequential ID rewrites the key every sibling artifact points at,
so a stale reference survives as a *real but wrong* pointer that no Markdown
tool notices. Three renumbering passes on feature 003 left twelve of them.

The orphan check below is the one that catches that class. A dangling-reference
check cannot, because the references still resolve. But a renumber shifts a
whole block at once, which always strands the requirements at the block's edge
with no citation left, and that is detectable.

Known limit: a single hand-typo'd citation that lands on another requirement
which some other task still cites will pass. A keyword-overlap heuristic was
tried and rejected: it flagged 7 correct citations and did not distinguish a
seeded defect, so it added noise without signal. Cascades are the recurring
failure and are covered; isolated typos still need a human reading the diff.

Run via `uv run poe check-specs`. Exits non-zero and names every offending file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"

FR_DEF = re.compile(r"^- \*\*(FR-\d{3}[a-z]?)\*\*:", re.MULTILINE)
SC_DEF = re.compile(r"^- \*\*(SC-\d{3}[a-z]?)\*\*:", re.MULTILINE)
TASK_DEF = re.compile(r"^- \[[ xX]\] (T\d{3}[a-z]?)", re.MULTILINE)
ANY_REF = re.compile(r"\b(?:FR|SC)-\d{3}[a-z]?\b|\bT\d{3}[a-z]?\b")
OUT_OF_SCOPE = re.compile(r"^\*\*Out of scope\*\*", re.MULTILINE)
DIGITS = re.compile(r"\d+")


def _base_number(item_id: str) -> int:
    match = DIGITS.search(item_id)
    if match is None:
        raise ValueError(f"{item_id!r} has no number")
    return int(match.group())


def _contiguous(ids: list[str], label: str) -> list[str]:
    """IDs must run 1..N with no gap, or a reference becomes ambiguous.

    A letter-suffixed ID (`FR-022a`, `T012a`) is an insertion that deliberately
    avoids renumbering its successors, so it shares a base number with the item
    it follows without being a duplicate of it.
    """
    bases = [_base_number(i) for i in ids]
    distinct = sorted(set(bases))
    expected = list(range(1, len(distinct) + 1))
    if distinct == expected and len(set(ids)) == len(ids):
        return []

    problems = []
    if missing := sorted(set(expected) - set(distinct)):
        problems.append(f"{label} gaps at {missing}")
    if dupes := sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"{label} duplicates: {dupes}")
    return problems


def check_feature(feature_dir: Path) -> tuple[list[str], bool]:
    """Return the problems found, and whether the feature is already shipped."""
    spec = feature_dir / "spec.md"
    tasks = feature_dir / "tasks.md"
    if not spec.exists() or not tasks.exists():
        return [], False

    spec_text = spec.read_text()
    tasks_text = tasks.read_text()
    frs = FR_DEF.findall(spec_text)
    if not frs:
        return [], False

    problems: list[str] = []
    scs = SC_DEF.findall(spec_text)
    task_ids = TASK_DEF.findall(tasks_text)
    shipped = bool(task_ids) and "- [ ] T" not in tasks_text

    problems += _contiguous(frs, "FR")
    problems += _contiguous(scs, "SC")
    problems += _contiguous(task_ids, "T")

    cutoff = OUT_OF_SCOPE.search(spec_text)
    exempt = set()
    if cutoff:
        exempt = set(FR_DEF.findall(spec_text[cutoff.start() :]))

    known = set(frs) | set(scs) | set(task_ids)
    for artifact in sorted(feature_dir.rglob("*.md")):
        referenced = set(ANY_REF.findall(artifact.read_text()))
        for dangling in sorted(referenced - known):
            rel = artifact.relative_to(PROJECT_ROOT)
            problems.append(f"{rel} references undefined {dangling}")

    cited = set(ANY_REF.findall(tasks_text))
    for orphan in sorted(set(frs) - exempt - cited):
        summary = re.search(rf"\*\*{re.escape(orphan)}\*\*: (.{{0,70}})", spec_text)
        detail = summary.group(1).strip() if summary else ""
        problems.append(f"{orphan} is cited by no task ({detail}...)")
    for orphan in sorted(set(scs) - cited):
        problems.append(f"{orphan} is cited nowhere in tasks.md")

    return problems, shipped


def main() -> int:
    if not SPECS_DIR.exists():
        print("no specs/ directory, nothing to check")
        return 0

    failed = False
    for feature_dir in sorted(p for p in SPECS_DIR.iterdir() if p.is_dir()):
        problems, shipped = check_feature(feature_dir)
        if not problems:
            continue
        label = "warnings, feature already complete" if shipped else "errors"
        failed = failed or not shipped
        print(f"\n{feature_dir.relative_to(PROJECT_ROOT)} ({label}):")
        for problem in problems:
            print(f"  {problem}")

    if failed:
        print("\nspec reference check FAILED")
        return 1
    print("\nspec reference check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
