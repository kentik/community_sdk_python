# Phase 0 Research: Pre-PR Audit Remediation

## Decision 1: Use evidence-led remediation order

Decision: Process findings in strict risk order, not by file ownership.

Rationale:

- Blockers affect immediate release safety.
- Generator/release defects can hide breakage behind green CI.
- Packaging/docs fixes are important but lower immediate production risk.

Alternatives considered:

- Ownership-first batching: rejected because it delays blocker closure.
- Single large patch: rejected because verification becomes ambiguous.

## Decision 2: One-by-one remediation batches with explicit verification

Decision: Each batch must have a target finding set, fix scope, and pass/fail verification commands.

Rationale:

- Matches user request to fix issues one by one.
- Makes regression attribution clear.
- Supports safe defer decisions for unresolved items.

Alternatives considered:

- Bulk fixes by section only: rejected due high blast radius.

## Decision 3: Treat partial findings as gated work items

Decision: For findings validated as partial, keep them in scope but require a prerequisite step before code change.

Rationale:

- Partial items are still credible and often source-validated.
- Prerequisites (fixtures, scratch repos, environment setup) avoid blind edits.

Alternatives considered:

- Drop partial findings from this cycle: rejected because they are user-visible risk.

## Decision 4: Keep generated-file rule strict

Decision: No direct edits under generated output paths; fix generator/runtime sources only.

Rationale:

- Direct generated edits are non-durable.
- Constitution and repo guidance require source-of-generation fixes.

Alternatives considered:

- Temporary generated hotfixes: rejected due guaranteed drift on regeneration.

## Decision 5: Validation baseline for this plan

Decision: Use [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md) as baseline.

Rationale:

- It records run/static/partial status per finding ID.
- It links findings to reproducible evidence scripts and code references.

Alternatives considered:

- Re-deriving status during implementation: rejected to avoid moving baseline.

## Open prerequisites

- Some evidence scripts need local scratch arguments or fixture files.
- A small subset of claims are static/traced and need environment-specific confirmation before final sign-off.
- Live API confirmations remain opt-in and are not mandatory for initial remediation batches.
