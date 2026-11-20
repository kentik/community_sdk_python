# Manual spot-check record

Date:
Runner:
Branch:
Python:

## Checklist

- [x] C1 - B13 e2e targets wrong host and false-pass rule
- [x] C2 - B5 malformed credential leaks token in error text
- [x] C3 - B6 gRPC use-after-close crashes process
- [x] C4 - B7 gRPC override ignores credential and host override (live candidate)
- [x] C5 - B1 unknown enum value can escape KentikError path (live candidate)

## How to run

1. Start from repo root.
2. Use the project interpreter at .venv/bin/python.
3. Record command, output, pass or fail, and notes for each check.

## Automation helper (one check per invocation)

Use the helper script to run exactly one check and append a structured run record.

```bash
uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py list
uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py run --check C4
uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py run --check C5 --notes "Staging token rotation test"
```

## Run output archive

- Summary log (auto-appended): [manual-spot-check-output.md](manual-spot-check-output.md)
- Structured artifacts (auto-written): [manual-spot-check-artifacts](manual-spot-check-artifacts)

## Spot-check replay policy

- Replay C1-C5 before the first blocker fix batch starts.
- Replay the affected checks after each blocker batch that changes the related code path.
- Replay all checks once more before PR readiness.
- Run one check per command invocation so each artifact has one finding context.
- When replay output supports a closure decision, include remediation-state metadata in the command.

Example fixed-state replay:

```bash
uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py run \
  --check C2 \\
  --remediation-state fixed \\
  --verification-gate "C2 replay after B5 fix"
```

Example deferred-state replay:

```bash
uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py run \
  --check C4 \\
  --remediation-state deferred \\
  --state-owner "sdk-runtime" \\
  --defer-reason "Needs upstream grpcio runtime fix" \\
  --mitigation "Keep REST fallback and track grpcio release notes" \\
  --revisit-trigger "Re-run after grpcio upgrade"
```

## Artifact retention policy

- Keep all JSON artifacts and markdown log entries for the full lifetime of this remediation feature.
- Treat [manual-spot-check-output.md](manual-spot-check-output.md) as append-only.
- Do not overwrite old artifacts. New runs must create new timestamped artifact files.
- Keep at least one reproduce artifact and one verify-after-fix artifact for each check ID.
- Link each closure decision in [validation.md](validation.md) to its supporting artifact file.

## Check log

| Check ID | Finding | Local script | Live API candidate | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | B13 e2e targets wrong host and false-pass rule | reports/pre-pr-audit-2026-10-10/evidence/tests/e2e_target_probe.py and e2e_logic_probe.py | No | Run (smoke) | See manual-spot-check-output.md entry at 2026-10-10T17:12:15Z |
| C2 | B5 malformed credential leaks token in error text | reports/pre-pr-audit-2026-10-10/evidence/rest/token_leak.py | No | Run | Reproduced. See manual-spot-check-output.md entry at 2026-10-10T17:19:54Z |
| C3 | B6 gRPC use-after-close crashes process | reports/pre-pr-audit-2026-10-10/evidence/rest/grpc_use_after_close.py | No | Run | Reproduced (exit_code -11). See manual-spot-check-output.md entry at 2026-10-10T17:20:57Z |
| C4 | B7 gRPC override ignores credential and host override | reports/pre-pr-audit-2026-10-10/evidence/rest/override_grpc.py | Yes | Run (live smoke) | See manual-spot-check-output.md entry at 2026-10-10T17:12:43Z |
| C5 | B1 unknown enum value can escape KentikError path | reports/pre-pr-audit-2026-10-10/evidence/me/enum_resp2.py | Yes, account-dependent | Run (live smoke) | See manual-spot-check-output.md entry at 2026-10-10T17:12:52Z |

## Detailed run worksheet

### C1

Command:
Output summary:
Observed result:
Expected result:
Assessment:

### C2

Command:
Output summary:
Observed result:
Expected result:
Assessment:

### C3

Command:
Output summary:
Observed result:
Expected result:
Assessment:

### C4

Command:
Output summary:
Observed result:
Expected result:
Assessment:

### C5

Command:
Output summary:
Observed result:
Expected result:
Assessment:
