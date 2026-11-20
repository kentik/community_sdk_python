# Data Model: Pre-PR Audit Remediation

## Entity: ValidatedFinding

Purpose: Represents one audit finding and its current remediation state.

Fields:

- id: String (example: B4, P6, R3)
- section: Enum (blocker, generation, latent, tests, runtime, packaging, docs)
- validation_status: Enum (confirmed_run, confirmed_static, confirmed_run_static, confirmed_run_partial, confirmed_static_partial, partial)
- validation_status_frozen_at: DateTime (baseline lock timestamp)
- severity: Enum (blocker, high, medium, low)
- evidence_links: List of paths
- remediation_state: Enum (open, in_progress, fixed, deferred)
- remediation_state_updated_at: DateTime
- remediation_state_owner: String
- verification_gate_id: String (required when remediation_state is fixed)
- defer_reason: String (required when remediation_state is deferred)
- defer_mitigation: String (required when remediation_state is deferred)
- defer_revisit_trigger: String (required when remediation_state is deferred)
- verification_gate: String command or test reference
- notes: String

Validation rules:

- id must be unique.
- id is immutable after baseline freeze.
- validation_status is immutable after baseline freeze unless a dated re-validation note is appended.
- allowed state transitions: open -> in_progress -> fixed or deferred; deferred -> in_progress; fixed -> in_progress only with explicit reopen note.
- deferred findings must include defer_reason, defer_mitigation, defer_revisit_trigger, and remediation_state_owner.
- fixed findings must include verification_gate_id and at least one passing VerificationGateResult.

## Entity: RemediationBatch

Purpose: One-by-one execution unit for a coherent subset of findings.

Fields:

- batch_id: String (A, B, C...)
- title: String
- target_finding_ids: List of finding ids
- scope_paths: List of repository paths
- preconditions: List of prerequisites
- verification_commands: List of commands
- completion_criteria: List of measurable checks
- status: Enum (planned, active, complete, blocked)
- closed_at: DateTime

Validation rules:

- Every target_finding_id must exist in ValidatedFinding.
- Batch cannot be complete unless all completion criteria pass.
- Batch cannot be complete while any target finding is still open.

## Entity: VerificationGateResult

Purpose: Captures result of a verification command for audit traceability.

Fields:

- finding_id: String
- batch_id: String
- command_or_test: String
- executed_at: DateTime
- outcome: Enum (pass, fail, skipped)
- output_summary: String
- artifact_path: String

Validation rules:

- Fixed findings require at least one pass result.
- Each result must map to an existing finding_id and batch_id.

## Entity: DeferredRiskEntry

Purpose: Records explicitly deferred findings and why deferment is acceptable.

Fields:

- finding_id: String
- reason: String
- user_impact: String
- mitigation: String
- owner: String
- revisit_trigger: String
- created_at: DateTime
- last_reviewed_at: DateTime
- status: Enum (open, accepted, resolved)

Validation rules:

- Deferred blockers require mitigation and explicit owner.
- finding_id must exist in ValidatedFinding with remediation_state set to deferred.
