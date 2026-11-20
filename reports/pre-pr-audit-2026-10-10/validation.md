# Validation matrix for pre-PR audit report

Date: 2026-10-10
Target report: [reports/pre-pr-audit-2026-10-10/report.md](report.md)

## Validation method

> Only the written record is tracked in git. The `evidence/` scripts, spot-check
> output, and artifacts stay local because they hold machine-specific paths and
> about 6 MB of scratch copies. Links to them work only in the author's tree.

- Executed all evidence Python scripts under [reports/pre-pr-audit-2026-10-10/evidence](evidence) with a 25s timeout per script.
- Corpus size: 168 scripts.
- Execution result: 136 exit 0, 32 non-zero, 0 timeout.
- Non-zero scripts were mostly expected crash repros (exit -11) or scripts that require scratch args/fixtures.
- Added static source checks for claims that are design-time or config-time, not runtime repros.
- Replayed C1-C5 manual spot checks via
  [reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py](run_manual_spot_check.py).
- Operator-visible replay output is archived in
  [reports/pre-pr-audit-2026-10-10/manual-spot-check-output.md](manual-spot-check-output.md).
- Structured replay records are in
  [reports/pre-pr-audit-2026-10-10/manual-spot-check-artifacts](manual-spot-check-artifacts).

Status legend:

- Confirmed (run): reproduced by direct script execution in this session.
- Confirmed (static): verified from source/config in this session.
- Partial: some sub-claims verified, at least one part needs extra fixture or a dedicated external environment.

## Remediation execution header

- Execution start: 2026-10-10.
- Execution scope: Phase 1 and Phase 2 scaffolding tasks.
- Source-of-truth rule: this file is authoritative for finding IDs, baseline validation status, and closure-state updates.
- ID freeze rule: do not rename, renumber, or delete finding IDs recorded in this file.
- Update rule: append remediation-state evidence and notes, and do not overwrite baseline validation facts.
- Related ledgers: [reports/pre-pr-audit-2026-10-10/report.md](report.md) and [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md).

## Blocker remediation order

1. B5
2. B6
3. B7
4. B1
5. B10
6. B13
7. B2
8. B3
9. B4
10. B8
11. B9
12. B11
13. B12

## Frozen source-of-truth snapshot (2026-10-10)

- Blockers: Confirmed (run)=B1,B2,B3,B4,B5,B6,B7,B9,B10,B11,B12; Confirmed (static)=B8; Partial=B13.
- Generation: Confirmed (run)=P1,P4,P5,P6; Confirmed (static)=P2,P3,P7.
- Latent hazards: Confirmed (run)=L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13.
- Test gaps: Confirmed (run)=T1,T3,T4,T9; Confirmed (static)=T5,T8,T10; Confirmed (run/static)=T6; Partial=T2,T7.
- Runtime defects: Confirmed (run)=R1,R2,R3,R4,R5,R6,R7,R8,R9,R11,R14,R16; Confirmed (run/partial)=R12; Partial=R10,R13,R15.
- Release and packaging: Confirmed (static)=K1,K2,K3,K5,K6,K7,K8,K9,K10,K11,K12; Partial=K4.
- Documentation: Confirmed (run)=D1,D2,D7,D12; Confirmed (static)=D4,D5,D6,D8,D10,D11; Confirmed (run/static)=D9; Partial=D3.

## US1 blocker state update (2026-10-11)

| Finding ID | Remediation state | Evidence links | Notes |
| --- | --- | --- | --- |
| B1 | fixed | [src/kentik_api/core/rest_runtime.py](../../src/kentik_api/core/rest_runtime.py), [tests/generated/test_endpoint_schema_coverage.py](../../tests/generated/test_endpoint_schema_coverage.py) | Unknown enum parsing now raises a KentikError-path exception instead of raw ValidationError. |
| B2 | fixed (live) | [scripts/generate_sdk.py](../../scripts/generate_sdk.py), [tests/generator/test_generate_sdk.py](../../tests/generator/test_generate_sdk.py), [tests/generated/test_alert_acknowledgement.py](../../tests/generated/test_alert_acknowledgement.py) | A versioned name that would overwrite an existing schema keeps its prefix. Live proof on 2026-10-13: `alert_list` with a `startedAt` filter returned 122 real alerts. All 122 parsed, and each `acknowledgement` is an `AlertAcknowledgement` object. The earlier 400 came from the call, not the SDK: the backend rejects an alert list with no `startedAt` range (other filters, pagination and sorting alone also fail). |
| B3 | deferred | [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_extctx.py](evidence/gencode/repro_extctx.py), [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | Needs schema-aware oneof required-field handling in generator pipeline. |
| B4 | deferred | [reports/pre-pr-audit-2026-10-10/evidence/generator/mitigation_lost.py](evidence/generator/mitigation_lost.py), [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | Needs pb tree layout redesign and wrapper generation updates. |
| B5 | fixed | [src/kentik_api/core/rest_runtime.py](../../src/kentik_api/core/rest_runtime.py), [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | Credential normalization and transport failure hardening prevent token leakage in error text. |
| B6 | fixed | [src/kentik_api/transports/grpc_client.py](../../src/kentik_api/transports/grpc_client.py), [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | Post-close gRPC calls are now rejected with ConfigurationError before channel use. |
| B7 | fixed | [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py), [tests/runtime/test_grpc_runtime.py](../../tests/runtime/test_grpc_runtime.py) | gRPC per-call overrides now allow timeout-only changes from with_timeout and fail fast otherwise. |
| B8 | fixed | [pyproject.toml](../../pyproject.toml), [src/kentik_api/core/api_config.py](../../src/kentik_api/core/api_config.py), [tests/runtime/test_api_config.py](../../tests/runtime/test_api_config.py) | `httpx<1` cap. Proxy routing uses `urllib.request.getproxies()`, not `httpx._utils`. Live check 2026-10-12: real REST call passed, a dead proxy broke the call, `NO_PROXY` bypassed it, and the SDK imported on httpx 1.0.dev6. |
| B9 | fixed | [src/kentik_api/transports/grpc_client.py](../../src/kentik_api/transports/grpc_client.py), [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py), [tests/runtime/test_grpc_transport.py](../../tests/runtime/test_grpc_transport.py) | The channel allows 40 MiB and takes `grpc_options`. An oversize response raises `TransportError`, not a 429. Live check 2026-10-13: a real `list_devices` call with a 1 KiB limit raised the new error for a 153566-byte response. |
| B10 | fixed | [src/kentik_api/core/rest_runtime.py](../../src/kentik_api/core/rest_runtime.py), [tests/generated/test_endpoint_schema_coverage.py](../../tests/generated/test_endpoint_schema_coverage.py) | Enum values now use wire representation for path and query encoding. |
| B11 | deferred | [reports/pre-pr-audit-2026-10-10/evidence/gencode/wrapper_names.py](evidence/gencode/wrapper_names.py), [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | Public naming stability needs generator naming-strategy redesign. |
| B12 | fixed | [scripts/generation/error_package.py](../../scripts/generation/error_package.py), [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py), [tests/generator/test_error_package.py](../../tests/generator/test_error_package.py), [tests/runtime/test_grpc_runtime.py](../../tests/runtime/test_grpc_runtime.py) | Response error classes extend their operation class. gRPC raises the same class as REST. Live check 2026-10-13: a real 404 was caught by `GetDeviceError` on REST (`GetDeviceUnexpectedError 404`) and on gRPC (`GetDeviceUnexpectedError 404 NOT_FOUND`). |
| B13 | fixed | [tests/e2e/conftest.py](../../tests/e2e/conftest.py), [tests/e2e/test_endpoints_e2e.py](../../tests/e2e/test_endpoints_e2e.py) | Live e2e now requires explicit flag, no forced api.example.com override, and stricter pass criteria. |

## US2 generator and release state update (2026-10-12)

| Finding ID | Remediation state | Evidence links | Notes |
| --- | --- | --- | --- |
| P1 | fixed | [scripts/generation/parity.py](../../scripts/generation/parity.py), [tests/generator/test_parity.py](../../tests/generator/test_parity.py) | An empty swagger selection now raises before generation. |
| P4 | partial | [scripts/generate_sdk.py](../../scripts/generate_sdk.py), [tests/generator/test_parity.py](../../tests/generator/test_parity.py) | A protoc failure now re-raises and fails the run. Staging-directory atomic swap is deferred. |
| P5 | fixed | [scripts/generation/parity.py](../../scripts/generation/parity.py), [tests/generator/test_wrapper_generation.py](../../tests/generator/test_wrapper_generation.py) | Versions compare by year-month, then alpha < beta < final, then number. Unparsed names such as `v1` sort lowest. |
| P6 | partial | [scripts/generation/api_surface.py](../../scripts/generation/api_surface.py), [scripts/release_notes.py](../../scripts/release_notes.py), [tests/generator/test_release_notes.py](../../tests/generator/test_release_notes.py) | The surface record (schema 3) keeps parameters and return types. Removed or retyped parameters and changed returns are breaking. The changelog gate needs a whole token in a code span. Unresolvable `--since`, ancestor-tag baselines, and `packaging`-based requirement parsing are deferred. |
| P7 | fixed | [scripts/generate_sdk.py](../../scripts/generate_sdk.py) | Patched swagger temp files go to the system temp directory, not the schema checkout. A regeneration gave a byte-identical tree. |

### L1-L13 triage

None of L1-L13 is triggered by the current schema. A regeneration at the local
schema checkout is byte-identical to the committed tree. Each fix needs a
generator design choice (naming policy, proto relinking, or template escaping).
All 13 are deferred to the next schema-sync work and recorded in the deferred-
risk ledger. No `fixup.py` change was made (T033).

Verification (2026-10-12): `make generate local` leaves the tree unchanged, and the mocked layers pass (2966 passed, 145 skipped).

## US3 runtime state update (2026-10-12)

| Finding ID | Remediation state | Evidence links | Notes |
| --- | --- | --- | --- |
| R1 | fixed | [src/kentik_api/core/rest_runtime.py](../../src/kentik_api/core/rest_runtime.py), [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | A non-UTF-8 body now raises an `HTTPException`, on both the error and the success path. |
| R2 | partial | [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | The non-UTF-8 and non-JSON 200 paths raise `HTTPException`. The JSON `null` and list shapes need generated-code changes and are deferred. |
| R3 | fixed | [src/kentik_api/errors/__init__.py](../../src/kentik_api/errors/__init__.py), [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | `HTTPException` and its subclasses now survive a pickle round trip. |
| R8 | fixed | [src/kentik_api/core/api_config.py](../../src/kentik_api/core/api_config.py), [src/kentik_api/client.py](../../src/kentik_api/client.py), [tests/runtime/test_rest_runtime.py](../../tests/runtime/test_rest_runtime.py) | `inf` and `nan` timeouts raise `ConfigurationError`. A non-string `region` raises `ConfigurationError`. |
| R12 | partial | [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py), [tests/runtime/test_grpc_runtime.py](../../tests/runtime/test_grpc_runtime.py) | A bad gRPC argument now raises `ConfigurationError`, not `ParseError`. The missing `update_mask` argument is deferred. |
| R4, R5, R6, R7, R9, R11, R14, R16 | deferred | [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | Each needs a design change in the config, transport or generator. |
| R10 | partial | [src/kentik_api/core/rest_runtime.py](../../src/kentik_api/core/rest_runtime.py) | Traced: httpx encodes a space in a query value as `+`. Only one live call can show whether Envoy decodes it. e2e runs are opt-in, so this stays open. |
| R13 | partial | [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py) | Confirmed: `map_grpc_error` ignores `google.rpc` error details. Quota comes from the initial metadata only. Deferred: no consumer needs the details today. |
| R15 | partial | Generated models | Traced to the model output step, not the runtime. Deferred to generator work. |

Verification (2026-10-12): runtime and generated suites pass (2708 passed, 145 skipped).

## US4 test-gap state update (2026-10-12)

| Finding ID | Remediation state | Evidence links | Notes |
| --- | --- | --- | --- |
| T2 | partial | [tests/runtime/test_credentials.py](../../tests/runtime/test_credentials.py) | A test now proves the transport attaches the credentials plugin with exact metadata. The in-process `grpc.server` test is deferred. |
| T5 | fixed | [tests/runtime/test_grpc_runtime.py](../../tests/runtime/test_grpc_runtime.py) | Existing tests already assert the per-call `timeout` reaches the stub. |
| T6 | fixed | [tests/smoke/test_client_mounts_and_calls.py](../../tests/smoke/test_client_mounts_and_calls.py) | Credential precedence was already tested. A new test checks the REST and gRPC hosts for `us` and `eu`. |
| T8 | fixed | [tests/generated/test_retry_eligibility.py](../../tests/generated/test_retry_eligibility.py) | Counts now derive from `api_surface.json`. |
| T10 | fixed | [tests/generated/test_grpc_stub_wiring.py](../../tests/generated/test_grpc_stub_wiring.py) | The mixin is parsed with `ast`. A new test checks every service with a wrapper is covered. |
| T1, T3, T4, T7, T9 | deferred | [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | Each needs swagger-derived fixtures or a gRPC routing record. |

Verification (2026-10-12): full mocked suite passes (2992 passed, 145 skipped).

## US5 packaging and docs state update (2026-10-12)

| Finding ID | Remediation state | Evidence links | Notes |
| --- | --- | --- | --- |
| K1 | deferred | [deferred-risks.md](deferred-risks.md) | `dist/` was git-ignored build output. The owner deleted it before any upload. |
| K2 | partial | [.github/workflows/release.yml](../../.github/workflows/release.yml), [tests/smoke/test_packaging_contract.py](../../tests/smoke/test_packaging_contract.py) | The notes job now needs `publish`. The build job checks the version against the tag and the pre-release flag. Trusted publishing needs PyPI-side setup and is deferred. |
| K4, K5, K6 | fixed | [pyproject.toml](../../pyproject.toml), [uv.lock](../../uv.lock), [tests/smoke/test_packaging_contract.py](../../tests/smoke/test_packaging_contract.py) | Floors raised to dotenv 1.2.1, hatchling 1.27.0, googleapis-common-protos 1.73.1. The lock is refreshed. |
| K7 | fixed | [.github/workflows/tests.yml](../../.github/workflows/tests.yml) | CI uses `uv sync --locked`. |
| K9 | fixed | [pyproject.toml](../../pyproject.toml) | The sdist now holds only source, tests and top-level metadata. A local build confirmed it. |
| K10 | fixed | [README.md](../../README.md), [docs/sphinx/guides/quickstart.md](../../docs/sphinx/guides/quickstart.md) | Install commands use `pip install -U "kentik-api>=2"`. |
| K11 | fixed | [LICENSE](../../LICENSE) | The markdownlint comment is gone. |
| K12 | fixed | [scripts/tasks.py](../../scripts/tasks.py), [AGENTS.md](../../AGENTS.md) | The `deep-clean` task keeps `uv.lock`. |
| K3, K8 | deferred | [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | K3 needs a published docs site or a short PyPI README. K8 needs a clean-venv wheel job. |
| D7, D8, D9, D10 | fixed | [tests/smoke/test_docs_contract.py](../../tests/smoke/test_docs_contract.py) | CHANGELOG command, the literal `\n`, the 1.x Python row, the `make help` regex, and the agent front matter are corrected. The pagination claim in `docs/README.md` is deferred. |
| D3, D4, D6, D11 | deferred | [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | These are hand-written doc rewrites and need owner review. |
| D1, D2, D5, D12 | deferred | [reports/pre-pr-audit-2026-10-10/deferred-risks.md](deferred-risks.md) | These need generator and template changes. |

Verification (2026-10-12): the full mocked suite passes (3004 passed, 145
skipped), `uv lock --check` passes, and a local `uv build` gives a clean sdist.
The Sphinx build was not run because `make docs` regenerates from the schema.

## Final verification gates (2026-10-12)

| Gate | Result |
| --- | --- |
| `make test` | 3004 passed, 145 skipped, 468 deselected |
| `uv run ruff check .` and `ruff format --check .` | Pass |
| `make typecheck` | Pass (one `ty` ignore comment corrected in `tests/runtime/test_transport_symmetry.py`) |
| `make check-specs` | Pass (the 004 tasks now cite every FR and SC) |
| `make check-changelog SINCE=HEAD` | Pass |
| `uv lock --check` | Pass |
| `sphinx-build -W --keep-going` | Build succeeded |
| `make generate local` | Tree unchanged (run after the generator fixes) |

### Manual spot-check replay

| Check | Finding | Verdict | Reading |
| --- | --- | --- | --- |
| C1 | B13 | reproduced (probe) | The probe copies the old test harness and does not drop `api_config_override`. The real test in `tests/e2e/test_endpoints_e2e.py` drops it and asserts the host. B13 stays fixed. |
| C2 | B5 | inconclusive | The leak no longer shows in the probe output. This matches the fix. |
| C3 | B6 | inconclusive | The probe exits non-zero without a segfault marker. A closed channel now raises `ConfigurationError`. This matches the fix. |
| C4, C5 | B7, B1 | not run | They call the real API. Live runs are opt-in, and nobody opted in. Mocked tests cover both. |

## Blockers

- B1: Confirmed (run). Evidence:
  [enum_resp2.py](evidence/me/enum_resp2.py),
  [enum_response.py](evidence/rest/enum_response.py),
  [enum_evolution.py](evidence/grpc/enum_evolution.py)
- B2: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_ack.py](evidence/gencode/repro_ack.py), [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_ack_call.py](evidence/gencode/repro_ack_call.py)
- B3: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_extctx.py](evidence/gencode/repro_extctx.py), [reports/pre-pr-audit-2026-10-10/evidence/grpc/oneof_required.py](evidence/grpc/oneof_required.py)
- B4: Confirmed (run). Evidence:
  [mitigation_lost.py](evidence/generator/mitigation_lost.py),
  [repro_mitig_grpc.py](evidence/gencode/repro_mitig_grpc.py),
  [collisions.py](evidence/grpc/collisions.py)
- B5: Confirmed (run). Evidence:
  - [reports/pre-pr-audit-2026-10-10/evidence/rest/token_leak.py](evidence/rest/token_leak.py)
  - [reports/pre-pr-audit-2026-10-10/evidence/me/token_leak.py](evidence/me/token_leak.py)
  - [reports/pre-pr-audit-2026-10-10/manual-spot-check-artifacts/20261010T171954Z-C2.json](manual-spot-check-artifacts/20261010T171954Z-C2.json)
- B6: Confirmed (run). Evidence:
  - [reports/pre-pr-audit-2026-10-10/evidence/me/grpc_close.py](evidence/me/grpc_close.py)
  - [reports/pre-pr-audit-2026-10-10/evidence/rest/grpc_use_after_close.py](evidence/rest/grpc_use_after_close.py)
  - [reports/pre-pr-audit-2026-10-10/manual-spot-check-artifacts/20261010T172057Z-C3.json](manual-spot-check-artifacts/20261010T172057Z-C3.json)
- B7: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/override_grpc.py](evidence/rest/override_grpc.py)
- B8: Confirmed (static). Evidence: [pyproject.toml](../../pyproject.toml#L30), [src/kentik_api/core/api_config.py](../../src/kentik_api/core/api_config.py#L9)
- B9: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/packaging/scripts/grpc_maxsize.py](evidence/packaging/scripts/grpc_maxsize.py)
- B10: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/enum_wire.py](evidence/rest/enum_wire.py), [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_path_enum.py](evidence/gencode/repro_path_enum.py)
- B11: Confirmed (run). Evidence:
  [method_retarget.py](evidence/generator/method_retarget.py),
  [wrapper_names.py](evidence/gencode/wrapper_names.py),
  [repro_rename.py](evidence/release/repro_rename.py)
- B12: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/tests/error_class_probe.py](evidence/tests/error_class_probe.py), [reports/pre-pr-audit-2026-10-10/evidence/me/err_hierarchy.py](evidence/me/err_hierarchy.py)
- B13: Partial. Items 1, 2, and 4 were confirmed by run. Item 3 was
  confirmed by static checks and a partial run. Evidence:
  [e2e_target_probe.py](evidence/tests/e2e_target_probe.py),
  [e2e_logic_probe.py](evidence/tests/e2e_logic_probe.py),
  [e2e_kwargs_probe.py](evidence/tests/e2e_kwargs_probe.py),
  [e2e_fixture_probe.py](evidence/tests/e2e_fixture_probe.py),
  [conftest.py](../../tests/e2e/conftest.py#L23),
  [pyproject.toml](../../pyproject.toml#L92)

## Generation pipeline

- P1: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/vacuous_gate.py](evidence/generator/vacuous_gate.py)
- P2: Confirmed (static). Evidence: [scripts/generate_sdk.py](../../scripts/generate_sdk.py#L52), [scripts/generate_sdk.py](../../scripts/generate_sdk.py#L325), [scripts/generate_sdk.py](../../scripts/generate_sdk.py#L468), [pyproject.toml](../../pyproject.toml#L55)
- P3: Confirmed (static). Evidence: [.github/workflows/tests.yml](../../.github/workflows/tests.yml#L101), [.github](../../.github)
- P4: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/vacuous_gate.py](evidence/generator/vacuous_gate.py)
- P5: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/version_order.py](evidence/generator/version_order.py)
- P6: Confirmed (run). Evidence:
  [repro_params.py](evidence/release/repro_params.py),
  [repro_rename.py](evidence/release/repro_rename.py),
  [repro_changelog_match.py](evidence/release/repro_changelog_match.py),
  [repro_version_bump.py](evidence/release/repro_version_bump.py),
  [repro_deps.py](evidence/release/repro_deps.py),
  [repro_baseline.sh](evidence/release/repro_baseline.sh),
  [repro_baseline_rc.sh](evidence/release/repro_baseline_rc.sh)
- P7: Confirmed (static). Evidence: [scripts/generate_sdk.py](../../scripts/generate_sdk.py#L248)

## Latent hazards

- L1: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_merge_overwrite.py](evidence/generator/case_merge_overwrite.py), [reports/pre-pr-audit-2026-10-10/evidence/generator/case_merge_overwrite_reversed.py](evidence/generator/case_merge_overwrite_reversed.py)
- L2: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/stale_dep.py](evidence/generator/stale_dep.py)
- L3: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_cross_file_input.py](evidence/generator/case_cross_file_input.py), [reports/pre-pr-audit-2026-10-10/evidence/generator/empty_response.py](evidence/generator/empty_response.py)
- L4: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/keyword_opid.py](evidence/generator/keyword_opid.py)
- L5: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_keyword_placeholder.py](evidence/generator/case_keyword_placeholder.py)
- L6: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_metadata_param.py](evidence/generator/case_metadata_param.py)
- L7: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_opid_normalization.py](evidence/generator/case_opid_normalization.py)
- L8: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_model_shadows_typing.py](evidence/generator/case_model_shadows_typing.py), [reports/pre-pr-audit-2026-10-10/evidence/generator/case_typing_opid.py](evidence/generator/case_typing_opid.py)
- L9: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_case_only.py](evidence/generator/case_case_only.py)
- L10: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_description_escapes.py](evidence/generator/case_description_escapes.py)
- L11: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/case_ancestor_named_pb.py](evidence/generator/case_ancestor_named_pb.py)
- L12: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/grpc/wkt_usage.py](evidence/grpc/wkt_usage.py)
- L13: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/gencode/collisions.py](evidence/gencode/collisions.py), [reports/pre-pr-audit-2026-10-10/evidence/gencode/clean_collisions.py](evidence/gencode/clean_collisions.py)

## Test gaps

- T1: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/generator/body_coverage_blind_spot.py](evidence/generator/body_coverage_blind_spot.py)
- T2: Partial. Coverage gap is shown by static inspection and grpc probe scripts, but there is no single dedicated pass/fail script in this session for auth metadata assertions.
- T3: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/tests/grpc_contract_probe.py](evidence/tests/grpc_contract_probe.py)
- T4: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/tests/grpc_request_probe.py](evidence/tests/grpc_request_probe.py)
- T5: Confirmed (static). Evidence: [src/kentik_api/core/grpc_runtime.py](../../src/kentik_api/core/grpc_runtime.py#L130)
- T6: Confirmed (run/static). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/empty_creds.py](evidence/rest/empty_creds.py), [tests/smoke/test_client_mounts_and_calls.py](../../tests/smoke/test_client_mounts_and_calls.py#L13)
- T7: Partial. Evidence scripts exist, but the specific CI-skip claim needs a dedicated CI-context run.
- T8: Confirmed (static). Evidence: [tests/generated/test_retry_eligibility.py](../../tests/generated/test_retry_eligibility.py#L49)
- T9: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/tests/e2e_kwargs_probe.py](evidence/tests/e2e_kwargs_probe.py), [reports/pre-pr-audit-2026-10-10/evidence/gencode/success_bodies.py](evidence/gencode/success_bodies.py)
- T10: Confirmed (static). Evidence: [tests/generated/test_grpc_stub_wiring.py](../../tests/generated/test_grpc_stub_wiring.py#L27)

## Runtime defects

- R1: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/tests/nonutf8_probe.py](evidence/tests/nonutf8_probe.py), [reports/pre-pr-audit-2026-10-10/evidence/rest/response_probe.py](evidence/rest/response_probe.py)
- R2: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/response_probe.py](evidence/rest/response_probe.py)
- R3: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/pickle_probe.py](evidence/rest/pickle_probe.py)
- R4: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/ratelimit_keys.py](evidence/rest/ratelimit_keys.py), [reports/pre-pr-audit-2026-10-10/evidence/packaging/scripts/ratelimit_keys.py](evidence/packaging/scripts/ratelimit_keys.py)
- R5: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/timeout_bound.py](evidence/rest/timeout_bound.py)
- R6: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/fork_probe.py](evidence/rest/fork_probe.py)
- R7: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/empty_creds.py](evidence/rest/empty_creds.py)
- R8: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/timeout_probe.py](evidence/rest/timeout_probe.py)
- R9: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/rest/mutation.py](evidence/rest/mutation.py)
- R10: Partial. Traced claim. Wire behavior and encoding behavior were inspected, but envoy-side decode semantics need live environment confirmation.
- R11: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/grpc/freeform_drop.py](evidence/grpc/freeform_drop.py)
- R12: Confirmed (run/partial). ParseError direction is supported by evidence scripts, though one dedicated script exits non-zero due harness assumptions.
- R13: Partial. Evidence scripts exist but need a focused run with the expected local grpc fixture files.
- R14: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/grpc/pool_conflict.py](evidence/grpc/pool_conflict.py)
- R15: Partial. Traced/model-analysis claim.
- R16: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/release/field_shapes.py](evidence/release/field_shapes.py)

## Release and packaging

- K1: Confirmed (static). Evidence: ignored `dist/` output and [LICENSE](../../LICENSE#L1)
- K2: Confirmed (static). Evidence: [.github/workflows/release.yml](../../.github/workflows/release.yml)
- K3: Confirmed (static/partial). Evidence: [pyproject.toml](../../pyproject.toml#L5), [README.md](../../README.md)
- K4: Partial. Static floor confirmed at [pyproject.toml](../../pyproject.toml#L26); FIFO runtime repro script needs dedicated local fixture handling.
- K5: Confirmed (static). Evidence: [pyproject.toml](../../pyproject.toml#L42)
- K6: Confirmed (static). Evidence: [pyproject.toml](../../pyproject.toml#L27)
- K7: Confirmed (static). Evidence: [.github/workflows/tests.yml](../../.github/workflows/tests.yml#L21)
- K8: Confirmed (static). Evidence: [.github/workflows/build.yml](../../.github/workflows/build.yml#L19)
- K9: Confirmed (static). Evidence: [pyproject.toml](../../pyproject.toml)
- K10: Confirmed (static). Evidence: [README.md](../../README.md), [docs/sphinx/guides/quickstart.md](../../docs/sphinx/guides/quickstart.md)
- K11: Confirmed (static). Evidence: [LICENSE](../../LICENSE#L1)
- K12: Confirmed (static). Evidence: the historical Makefile; the task now lives in [scripts/tasks.py](../../scripts/tasks.py).

## Documentation

- D1: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/release/check_docs.py](evidence/release/check_docs.py)
- D2: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/release/check_docs.py](evidence/release/check_docs.py), [reports/pre-pr-audit-2026-10-10/evidence/packaging/scripts/check_example_attrs.py](evidence/packaging/scripts/check_example_attrs.py)
- D3: Partial. Several sub-claims are static-document checks and branch-history checks, not all reproduced in this session.
- D4: Confirmed (static). Evidence: [.specify/memory/constitution.md](../../.specify/memory/constitution.md#L114)
- D5: Confirmed (static). Evidence: [src/kentik_api/gen/README.md](../../src/kentik_api/gen/README.md#L45)
- D6: Confirmed (static). Evidence: [docs/sphinx/guides/rest-vs-grpc.md](../../docs/sphinx/guides/rest-vs-grpc.md#L129)
- D7: Confirmed (run). Evidence: [CHANGELOG.md](../../CHANGELOG.md#L12), command result for make release-notes SINCE=v1.0.7 exits non-zero.
- D8: Confirmed (static). Evidence: [docs/sphinx/authentication.md](../../docs/sphinx/authentication.md#L5), [docs/sphinx/guides/migrating-from-1x.md](../../docs/sphinx/guides/migrating-from-1x.md#L17), [docs/README.md](../../docs/README.md#L12)
- D9: Confirmed (run/static). Evidence: the historical Makefile; feature 007 moved the tasks to [pyproject.toml](../../pyproject.toml).
- D10: Confirmed (static). Evidence: [.github/agents/kentik-sdk-autogen.agent.md](../../.github/agents/kentik-sdk-autogen.agent.md#L1)
- D11: Confirmed (static). Evidence: [specs/001-validate-schema-checkout/quickstart.md](../../specs/001-validate-schema-checkout/quickstart.md#L30)
- D12: Confirmed (run). Evidence: [reports/pre-pr-audit-2026-10-10/evidence/gencode/docstrings.py](evidence/gencode/docstrings.py)

## Final validation outcome

- No finding was disproven by the evidence corpus.
- Most blocker and runtime findings are directly reproducible in this environment.
- A small subset is validated by static inspection or requires targeted external fixtures/scratch setup.
- The report is directionally and technically correct enough to use as the remediation driver.
