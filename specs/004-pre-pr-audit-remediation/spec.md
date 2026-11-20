# Feature Specification: Pre-PR Audit Remediation

**Feature Branch**: FA-2-Update-the-python-SDK-from-V5-to-V6

**Created**: 2026-10-10

**Status**: Draft

**Input**: User description: Validate the full pre-PR audit report against the evidence corpus, then create a Spec Kit plan to fix validated issues one by one.

## Context

The [audit report][audit] lists blockers and lower-severity defects.
It covers the runtime, generator, tests, release tools, packaging, and documentation.

[audit]: ../../reports/pre-pr-audit-2026-10-10/report.md

Validation in this session executed the evidence corpus and produced a finding ledger at [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md).

This feature turns that validated ledger into an ordered remediation program, with explicit verification gates and one-by-one delivery.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Release-critical blockers are resolved first (Priority: P1)

As a maintainer preparing the PR, I need all validated blocker findings to be fixed first, or explicitly deferred with documented risk, so the PR can ship safely.

**Why this priority**: Blockers directly impact correctness, safety, or release viability.

**Independent Test**: Run blocker repro scripts and confirm each no longer reproduces after its fix, or appears in a deferred-risk list with owner and rationale.

**Acceptance Scenarios**:

1. **Given** a validated blocker finding, **When** its remediation is merged, **Then** its paired evidence repro no longer shows the defect.
2. **Given** a blocker not fixed in this cycle, **When** the PR is prepared, **Then** that blocker is listed in an explicit deferred-risk section with mitigation.

---

### User Story 2 - Generator and release gates prevent silent regressions (Priority: P1)

As a maintainer, I need generator and release-tooling defects fixed so schema syncs and release notes reliably detect real breakage.

**Why this priority**: Current gaps can produce green CI with broken generated behavior.

**Independent Test**: Run the generator and release repro scripts for validated P/L findings; verify they fail before fix and pass after fix.

**Acceptance Scenarios**:

1. **Given** a protoc failure or routing loss, **When** generation runs, **Then** generation exits non-zero and reports the failure.
2. **Given** a true public-surface break, **When** changelog checks run, **Then** the check fails unless a matching changelog entry exists.

---

### User Story 3 - Runtime behavior is transport-consistent and safe (Priority: P1)

As an SDK caller, I need REST and gRPC runtime behavior to be safe, predictable, and free of known crash/leak paths.

**Why this priority**: Runtime defects affect production callers immediately.

**Independent Test**: Execute validated runtime evidence scripts for B and R findings and confirm fixed behavior.

**Acceptance Scenarios**:

1. **Given** malformed credentials or transport faults, **When** calls fail, **Then** errors do not leak secrets and match SDK error contracts.
2. **Given** a closed gRPC transport, **When** a call is attempted, **Then** the SDK raises a catchable SDK exception and does not crash the interpreter.

---

### User Story 4 - Test suite catches the defects it is expected to guard (Priority: P2)

As a maintainer, I need test-gap findings closed so CI catches the same defect classes that the audit found.

**Why this priority**: Without test hardening, fixes can regress silently.

**Independent Test**: Add or adjust tests for validated T findings, then run make test and targeted generator/runtime suites.

**Acceptance Scenarios**:

1. **Given** a seeded regression from a validated gap class, **When** tests run, **Then** at least one relevant test fails.
2. **Given** fixed behavior, **When** the full test suite runs, **Then** it passes with the new assertions.

---

### User Story 5 - Packaging and docs are release-ready and accurate (Priority: P2)

As a maintainer, I need packaging and documentation findings resolved so published artifacts and instructions are correct.

**Why this priority**: Incorrect packaging/docs cause user-facing breakage and support cost.

**Independent Test**: Run build/docs/release commands and static checks associated with validated K and D findings.

**Acceptance Scenarios**:

1. **Given** packaging metadata and workflow settings, **When** release gates run, **Then** they enforce lock correctness, safe publish flow, and clean artifacts.
2. **Given** docs pages and generated docs snippets, **When** docs checks run, **Then** content is accurate and Sphinx build is warning-clean.

### Edge Cases

- A remediation changes generated output unexpectedly outside intended scope.
- Fixing one blocker exposes additional defects in the same area.
- Evidence scripts need scratch fixtures not present by default.
- A fix is correct but cannot be safely completed before the PR deadline.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The remediation program MUST use [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md) as the source of truth for validated findings.
- **FR-002**: Every validated blocker (B1-B13) MUST be either fixed or explicitly deferred with risk, owner, and mitigation.
- **FR-003**: Blocker fixes MUST be implemented one by one in a deterministic order that minimizes release risk.
- **FR-004**: Each completed fix MUST include a reproducible verification step tied to at least one evidence script or direct test.
- **FR-005**: Runtime/security fixes MUST never leak credential values in exception messages or logs.
- **FR-006**: gRPC close-path behavior MUST be catchable and MUST NOT terminate the interpreter process.
- **FR-007**: REST and gRPC override semantics MUST be consistent, or explicit mismatch behavior MUST be surfaced as a configuration error.
- **FR-008**: Enum handling for path/query and response parsing MUST be robust to valid SDK usage and schema evolution.
- **FR-009**: Generator pipeline fixes for P1-P7 MUST include regression tests or validation checks where feasible.
- **FR-010**: Surface/changelog tooling MUST detect the validated break classes documented in P6.
- **FR-011**: Latent hazards L1-L13 MUST be triaged into fix-now vs scheduled follow-up, with explicit rationale per item.
- **FR-012**: Test-gap items T1-T10 MUST be addressed so seeded regressions from each class are detectable.
- **FR-013**: Runtime defects R1-R16 MUST be triaged and remediated or explicitly deferred with user impact.
- **FR-014**: Packaging/release findings K1-K12 MUST be resolved or deferred before first 2.0.0 publish.
- **FR-015**: Documentation findings D1-D12 MUST be corrected in the owning source (generator templates or hand-written docs).
- **FR-016**: Remediation MUST avoid hand-editing generated output directly; generator/template changes MUST drive generated diffs.
- **FR-017**: The final branch state MUST pass the same CI-equivalent gates used for PR readiness.
- **FR-018**: Any remaining deferred findings MUST be listed in PR description and tracked for follow-up.

### Key Entities *(include if feature involves data)*

- **ValidatedFinding**: A finding ID with status, scope, evidence links, and remediation state.
- **RemediationBatch**: A one-by-one delivery unit with target findings, code paths, and verification steps.
- **VerificationGate**: A repeatable command or test proving defect resolution.
- **DeferredRiskEntry**: A documented unresolved finding with owner, impact, mitigation, and due follow-up.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of validated blocker findings are either fixed with passing verification or explicitly deferred with documented risk.
- **SC-002**: All required CI-equivalent commands pass from a clean workspace state before PR creation.
- **SC-003**: At least one regression-detection check exists for each validated test-gap category addressed in this cycle.
- **SC-004**: No evidence script used for blocker verification reproduces its original defect after the corresponding fix, except intentionally deferred items.
- **SC-005**: Documentation and packaging checks for targeted findings are warning-clean and internally consistent.

## Assumptions

- The evidence corpus is authoritative for reproducing and validating finding classes.
- Some scripts require scratch fixtures or local setup; those are acceptable as validation prerequisites.
- No direct edits to generated files are accepted as durable fixes.
- Real Kentik API calls remain opt-in for this remediation cycle unless explicitly required for a specific claim.
