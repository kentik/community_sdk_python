# Remediation Contract

## Purpose

Define the operational contract for closing validated audit findings one by one with verifiable outcomes.

## Inputs

- Validated ledger: [reports/pre-pr-audit-2026-10-10/validation.md](../../../reports/pre-pr-audit-2026-10-10/validation.md)
- Source report: [reports/pre-pr-audit-2026-10-10/report.md](../../../reports/pre-pr-audit-2026-10-10/report.md)

## Contract Rules

1. One-by-one batch rule

- A batch targets a bounded finding set with shared code paths.
- A batch must define verification commands before implementation.

1. Fix-or-defer rule

- Every validated finding must end in fixed or deferred state.
- Deferred findings require owner, rationale, mitigation, and revisit trigger.

1. Verification rule

- Each fixed finding needs at least one passing gate tied to its evidence class.
- Regression checks must be capable of failing when the defect is reintroduced.

1. Generated-output rule

- Do not hand-edit generated artifacts for durable fixes.
- Protected generated paths include `src/kentik_api/gen/`, `src/kentik_api/client_mixin.py`, `docs/sphinx/services/`, `docs/sphinx/sdk_runtime_architecture.md`, and `src/kentik_api/gen/README.md`.
- Implement durable fixes in hand-written runtime files, generator modules, or templates.
- When a fix touches generator behavior, run `make generate local` and keep only intentional generated diffs in the same batch.
- If a proposed change appears to require direct edits in protected generated paths, stop and defer the finding with rationale instead of patching generated output.

1. Release-readiness rule

- Blockers must be fixed or deferred before PR readiness.
- Deferred blockers must be listed in PR description.

## Outputs

- Updated code and tests for targeted finding batch.
- Verification evidence in command/test output.
- Updated finding states in remediation tracking notes.
