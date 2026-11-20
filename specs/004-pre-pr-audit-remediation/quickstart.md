# Quickstart Validation Guide: Pre-PR Audit Remediation

This guide validates remediation batches end-to-end without changing the execution model of the repository.

## Prerequisites

- Repo dependencies installed via uv.
- Local schema checkout available when running generation checks.
- No direct edits under generated output paths.

## Execution workflow notes

1. Start each batch by updating tracking ledgers before code changes.
2. Set the batch status in [reports/pre-pr-audit-2026-10-10/report.md](../../reports/pre-pr-audit-2026-10-10/report.md).
3. Keep finding IDs stable in [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md), and append only state updates and evidence links.
4. Use the manual spot-check runner for C1-C5 replays and include remediation-state metadata when the replay supports closure decisions.
5. If a finding is deferred, add one entry in [reports/pre-pr-audit-2026-10-10/deferred-risks.md](../../reports/pre-pr-audit-2026-10-10/deferred-risks.md) in the same batch.

## 1. Baseline checks

Run before starting a new remediation batch:

- uv sync --locked
- make test
- uv run ruff check .
- uv run ruff format --check .
- make typecheck
- make check-specs
- uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html

Expected outcome: clean baseline or known failures already tracked in current batch scope.

## 2. Batch execution pattern

For each remediation batch:

1. Identify target finding IDs.
2. Implement only scoped fixes for that batch.
3. Run targeted evidence or regression checks for those IDs.
4. Run project-level gates.
5. Record fixed or deferred status for each target finding in the validation ledger.
6. Update deferred risk records when a target finding remains deferred.

## 3. Evidence-driven verification

Use the evidence scripts linked in [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md) as reproducibility references.

Expected outcome: original defect signal is removed for fixed findings, or explicitly documented for deferred findings.

## 4. Regeneration and surface checks

When batch scope includes generator changes:

- make generate local
- make release-notes
- make check-changelog SINCE=BASELINE_REF

Expected outcome: generated diff is intentional and tracked, surface/report tooling reflects actual changes.

## 5. Batch verification command catalog

Use this catalog to pick the minimum gate set for each batch type.

| Batch type | Commands | Pass rule |
| --- | --- | --- |
| Setup and foundational tracking | `uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py list` | Check catalog is available and check IDs are stable. |
| Manual replay with finding-state update | `uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py run --check C2 --remediation-state in_progress --verification-gate "C2 replay"` | Check record is appended to markdown log and JSON artifact with remediation-state metadata. |
| Runtime-focused blocker batch | `uv run pytest tests/runtime/test_rest_runtime.py` and `uv run pytest tests/runtime/test_grpc_runtime.py` | Targeted runtime regressions pass for changed paths. |
| Generator/release batch | `make generate local`, `make release-notes`, `make check-changelog SINCE=BASELINE_REF` | Generation succeeds, surface report is intentional, changelog check passes. |
| Full branch gate | `make test`, `uv run ruff check .`, `uv run ruff format --check .`, `make typecheck`, `make check-specs`, `uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html` | Full verification stack passes or only contains already tracked known failures. |

## 6. Final readiness check

Before PR draft or ready-for-review transition:

- Re-run all baseline checks.
- Ensure blocker findings are fixed or deferred with mitigation.
- Ensure deferred blockers are listed in PR description.

Expected outcome: branch is ready for reviewer verification and CI parity.

## 7. Closure notes (2026-10-12)

- Tasks T001 to T064 are complete. Some descriptions carry a "deferred" note where the work moved to the ledger.
- Evidence: [validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md) holds one state table per phase and the final gate results.
- Open risks: 57 entries in [deferred-risks.md](../../reports/pre-pr-audit-2026-10-10/deferred-risks.md). The PR summary block is at the end of [report.md](../../reports/pre-pr-audit-2026-10-10/report.md).
- Not run: C4 and C5 live spot checks, and any live e2e suite. They need explicit opt-in.
