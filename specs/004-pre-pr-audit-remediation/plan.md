# Implementation Plan: Pre-PR Audit Remediation

**Branch**: FA-2-Update-the-python-SDK-from-V5-to-V6 | **Date**: 2026-10-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from [specs/004-pre-pr-audit-remediation/spec.md](spec.md)

## Summary

Resolve validated findings from the pre-PR audit in risk order, with one-by-one
remediation batches and explicit verification gates. Prioritize blocker closure,
then generator/release correctness, then runtime/test/documentation hardening.
Use the validation ledger as the execution source of truth.

## Technical Context

**Language/Version**: Python >=3.12

**Primary Dependencies**: httpx, grpcio, protobuf, pydantic, python-dotenv, pytest, ruff, ty, sphinx

**Storage**: N/A

**Testing**: pytest suites under tests/generated, tests/runtime, tests/smoke, tests/generator, plus opt-in tests/e2e

**Target Platform**: Python SDK consumers on macOS/Linux/Windows

**Project Type**: Generated client SDK with hand-written shared runtime and generator pipeline

**Performance Goals**: Preserve deterministic generation and avoid runtime regressions while closing defects

**Constraints**:

- Never hand-edit generated output directly
- Keep fixes scoped by remediation batch
- CI-equivalent verification required after each batch
- Preserve security constraints around credentials and logs

**Scale/Scope**: Validated findings across B/P/L/T/R/K/D categories as documented in [reports/pre-pr-audit-2026-10-10/validation.md](../../reports/pre-pr-audit-2026-10-10/validation.md)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Principle I (generated code): PASS. Plan routes fixes through generator/runtime sources.
- Principle II (shared runtime): PASS. Runtime defects are fixed in shared runtime modules.
- Principle III (phase modules): PASS. Generator fixes stay in scripts/generation with tests.
- Principle IV (coverage): PASS with action. Test-gap closure is an explicit phase.
- Principle V (e2e opt-in): PASS. No default CI expansion into live e2e.
- Principle VI (credentials): PASS with action. Token-leak and credential-handling blockers prioritized.
- Principle VII (scope discipline): PASS. One-by-one batches and deferred-risk ledger required.

## Project Structure

### Documentation (this feature)

```text
specs/004-pre-pr-audit-remediation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── remediation-contract.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
src/kentik_api/
├── core/
├── transports/
├── auth/
└── errors/

scripts/
├── generate_sdk.py
└── generation/

tests/
├── generated/
├── runtime/
├── smoke/
└── generator/

.github/workflows/

docs/
```

**Structure Decision**: Keep current project structure. Apply targeted fixes in existing runtime/generator/test/doc files, grouped by remediation batch.

## Phases

### Phase 0: Validation-led research finalization

Outputs: [research.md](research.md)

- Confirm execution strategy per finding group (blocker, generator/release, runtime/tests, packaging/docs).
- Record unresolved prerequisites for partial findings.
- Freeze remediation order and verification strategy.

### Phase 1: Design and contract

Outputs: [data-model.md](data-model.md), [contracts/remediation-contract.md](contracts/remediation-contract.md), [quickstart.md](quickstart.md)

- Define tracking entities and batch workflow.
- Define remediation contract: one finding class at a time, mandatory verification, defer rules.
- Define operator quickstart for execution and acceptance.

### Phase 2: Implementation sequencing (for tasks generation)

- Batch A: Release-critical quick fixes (B8, K1, K4-K7, B13 fixture semantics)
- Batch B: Runtime blockers (B5, B6, B7, B9, B10, R1-R3)
- Batch C: Generator blockers and parity safety (B2, B3, B4, P1, P4, B1)
- Batch D: Public API stability and error hierarchy (B11, B12, P6)
- Batch E: Test-gap closure (T1-T10 plus remaining B13 assertions)
- Batch F: CI sync automation and pinning (P2, P3)
- Batch G: Packaging/docs closure (K2-K12, D1-D12, remaining R/L follow-ups)

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| None | N/A | N/A |
