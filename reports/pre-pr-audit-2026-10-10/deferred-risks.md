# Deferred risk ledger

Date initialized: 2026-10-10

This ledger records findings that are intentionally deferred.

## Rules

- Use one row per deferred finding ID.
- Keep finding IDs exactly as they appear in validation.md.
- Every deferred blocker must include owner, mitigation, and revisit trigger.
- Keep this file append-only for history. If a risk is resolved, update status to resolved and add closure notes.

## Deferred risk entries

| Finding ID | Severity | Reason for deferral | User impact | Mitigation | Owner | Revisit trigger | Status | Evidence links | Last reviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B2 | blocker | Needs generator collision guard for object and enum short-name conflicts. | Alert acknowledgement payloads can fail validation on affected endpoints. | Keep issue visible in validation ledger and avoid relying on ack response body parsing for automation decisions. | sdk-generation | Revisit when US2 generator hardening tasks start. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_ack.py](evidence/gencode/repro_ack.py) | 2026-10-11 |
| B3 | blocker | Oneof-required conflict handling is missing in generated model shaping. | External-context writes can fail when schema marks multiple oneof members as required. | Treat affected flows as known-risk paths and avoid rollout claims for those endpoints until fixed. | sdk-generation | Revisit when oneof/schema reconciliation work is prioritized in generator backlog. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/gencode/repro_extctx.py](evidence/gencode/repro_extctx.py) | 2026-10-11 |
| B4 | blocker | Proto file-name collision handling needs pb layout redesign. | gRPC routes can be missing for specific services even when proto RPCs exist upstream. | Keep REST path as supported default for impacted methods and track explicit gRPC not-implemented behavior. | sdk-generation | Revisit when pb package-tree and import relinking work is scheduled. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/generator/mitigation_lost.py](evidence/generator/mitigation_lost.py) | 2026-10-11 |
| B8 | blocker | Packaging guard for httpx major bump and private import replacement is not implemented in this batch. | Future dependency resolution may break import-time behavior on new httpx major releases. | Pin release process checks for dependency drift and keep upgrade blocked until compatibility patch lands. | sdk-release | Revisit when packaging and release-hardening phase starts. | resolved | [pyproject.toml](../../pyproject.toml), [src/kentik_api/core/api_config.py](../../src/kentik_api/core/api_config.py) | 2026-10-11 |
| B9 | blocker | gRPC receive-size policy and RESOURCE_EXHAUSTED classification need deeper runtime change. | Large responses may fail with misleading quota-like errors. | Keep REST fallback guidance for large payload workflows and track gRPC response-size incidents. | sdk-runtime | Revisit when gRPC runtime sizing and error taxonomy tasks are active. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/packaging/scripts/grpc_maxsize.py](evidence/packaging/scripts/grpc_maxsize.py) | 2026-10-11 |
| B11 | blocker | Public-name stability requires generator naming policy redesign. | Minor schema evolution can cause user-facing API name drift across releases. | Continue publishing clear surface-change notes and avoid stability guarantees for pending name-policy areas. | sdk-generation | Revisit when wrapper naming strategy work enters implementation phase. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/gencode/wrapper_names.py](evidence/gencode/wrapper_names.py) | 2026-10-11 |
| B12 | blocker | Operation-specific error hierarchy alignment is incomplete across transports. | Catch clauses scoped to operation-specific classes may miss real raised exceptions. | Document current catch guidance and prefer broader KentikError handling at integration boundaries. | sdk-runtime | Revisit when transport-symmetry and error-hierarchy tasks are implemented. | resolved | [reports/pre-pr-audit-2026-10-10/evidence/tests/error_class_probe.py](evidence/tests/error_class_probe.py) | 2026-10-11 |
| P2 | latent | Pinning needs a dev-group dependency and CI changes. | A future upstream schema change can break generation or the release gate (generator toolchain unpinned). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| P3 | latent | Needs a pinned schema commit and a scheduled sync job. | A future upstream schema change can break generation or the release gate (CI follows a moving schema). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| P3a | release or docs | The weekly schema-sync job needs a repository setting that only an admin can change, after the PR merges. | Until then the job fails at `gh pr create`, so the schema pin does not move by itself. | Run `uv run poe sync-schema` by hand and open the pull request. | repository admin | Revisit when the V6 PR merges to `main`. | open | [docs/sphinx/guides/generation.md](../../docs/sphinx/guides/generation.md) | 2026-10-17 |
| P4 | latent | Staging-directory swap is a larger generator change. | A future upstream schema change can break generation or the release gate (generation is not atomic). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| P6 | latent | Ancestor-tag baselines, ref failure, and requirement parsing remain. | A future upstream schema change can break generation or the release gate (changelog gate gaps). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| L1 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| L2 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| L3 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L4 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L5 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L6 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L7 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L8 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L9 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L10 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L11 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| L12 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| L13 | latent | Not triggered by the current schema; the fix needs a generator design choice. | A future upstream schema change can break generation or the release gate (latent generator hazard). | Regenerate and review the diff on every schema sync. | sdk-generation | Revisit at the next schema sync. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-15 |
| R2 | runtime | JSON null and list shapes need generated-code changes. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R4 | runtime | Quota keys need a method and path-template scheme. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R5 | runtime | Total-deadline timeout needs a transport design. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R6 | runtime | Fork safety needs client pool lifecycle work. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R7 | runtime | Empty-string credentials need a resolution-order decision. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R9 | runtime | Mutability rules for config objects need a design decision. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R10 | runtime | Needs one live call to settle. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R11 | runtime | Free-form bodies need schema-aware gRPC encoding. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R12 | runtime | The missing update_mask argument needs generator work. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R13 | runtime | No consumer needs the error details today. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R14 | runtime | Wrapper generation hides the import cause. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R15 | runtime | Model output step must relax REQUIRED on message fields. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| R16 | runtime | Generator does not hoist inline objects. | Edge-case behavior differs from the documented contract. | Callers catch KentikError broadly. | sdk-runtime | Revisit at the next runtime hardening batch. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| T1 | test gap | Swagger-derived response fixtures are a large test-harness change. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| T2 | test gap | In-process grpc.server success-path test. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| T3 | test gap | Needs gRPC routes recorded in api_surface.json. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| T4 | test gap | Needs the real request builder run on populated bodies. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| T7 | test gap | Needs a committed swagger-derived record. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| T9 | test gap | Needs a sampler that fills every request-body field. | A defect in that area can pass the mocked suite. | The e2e layer and manual review cover it until then. | sdk-tests | Revisit when the test harness is next extended. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| K1 | release or docs | dist/ is local build output; the owner deletes it. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| K2 | release or docs | Publishing keeps the legacy SDK's `PYPI_TOKEN` setup until the PR is accepted and a release validates it; the owner of the PyPI project and token is not yet known. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | unknown (under investigation) | Revisit once the PyPI owner is found and the first 2.0.0 release has run. | open | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| K3 | release or docs | Needs a docs site or a short PyPI README. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| K8 | release or docs | Needs a clean-venv wheel job in CI. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D1 | release or docs | Generator must run extract() on the patched swagger. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| D2 | release or docs | Generator example snippets need import fixes. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |
| D3 | release or docs | CLAUDE.md rewrite needs owner review. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D4 | release or docs | Constitution change needs owner review. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D5 | release or docs | docs_rendering text needs a generator change. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D6 | release or docs | Waits for B4. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D11 | release or docs | Spec 001 quickstart commands need a rewrite. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-12 |
| D12 | release or docs | Needs template changes for docstrings. | Published artifacts or guidance stay partly inaccurate. | Reviewers read the PR description for the known list. | sdk-release | Revisit before the first 2.0.0 release. | resolved | [reports/pre-pr-audit-2026-10-10/report.md](report.md) | 2026-10-14 |

## Closure notes

- 2026-10-12: 53 entries remain open. Owners: sdk-generation 21, sdk-runtime 15, sdk-release 13, sdk-tests 6.
- B2, B8, B9 and B12 are resolved (live-verified 2026-10-12 and 2026-10-13). Each one is listed in the PR description.
- B3 is resolved (2026-10-13). The generator reads `oneof` groups from the protoc descriptor set and drops their members from the swagger `required` list. `repro_extctx.py` now passes both checks.
- B4 is resolved (2026-10-13) without a pb package tree. Only proto modules
  whose names collide inside a Service get their folder in the name
  (`mitigation_public_v202505_pb2`), and protoc's imports are rewritten by
  package path. All six `MitigationsService` operations now route over gRPC.
  `mitigation_lost.py` still reads the old `mitigation_pb2_grpc.py` path, so
  its last line fails.
- B4 live check (2026-10-13, lab account): all six `MitigationsService` RPCs
  reach the server over gRPC, and the SDK builds each request (duration, enum
  path value, int64 ids) without a local error. Every gRPC call returns the
  upstream alerting `500 RangeError`, so a successful gRPC response waits on
  Kentik's fix. REST create, get, act STOP and act DELETE succeeded on
  mitigation `10000`, which is now archived. The lab had no mitigation device,
  so the mitigation never started.
- B11 is resolved (2026-10-13). Wrapper method names no longer depend on file
  or route order: a name several REST modules declare gets the module prefix
  in every module, and a second HTTP route is named by its extra path
  parameters. Generation fails instead of adding a number suffix.
  `api_surface.json` (schema version 4) records each operation's client
  method, so a rename is a breaking change for `make check-changelog`.
  Renamed: 32 client methods in 10 Services, also dropping the Service word
  where two or more words remain (`audit.get_audit_event` to `get_event`). The
  CHANGELOG's "Renamed client methods" table lists them.
- D6 is resolved (2026-10-13). The REST vs gRPC guide now says all 234
  operations have a gRPC translation. `mitigation_lost.py` now checks the
  renamed stub modules.
- 2026-10-13: 47 entries remain open, none of them blockers.
- R15 is resolved (2026-10-13). The generator drops message-typed fields from
  `required` in every model a response can reach. Models used only in
  requests keep them. Nine fields became `Optional`, and a policy without a
  `baseline` now parses. 46 entries remain open.
- K1 is resolved (2026-10-13). The owner approved deleting `dist/`. It held a
  local `uv build` from 2026-08-18 with a fixed version 2.0.0, the MIT
  license and fork URLs. 45 entries remain open.
- R2 is resolved (2026-10-13) in the shared runtime, with no generated-code
  change. A non-JSON or JSON `null` success body raises `HTTPException` 502,
  as a wrong-shape body already did (a JSON list no longer gave `TypeError`).
  44 entries remain open.
- R12 is resolved (2026-10-13). A bad gRPC argument already raised
  `ConfigurationError`. For the missing `update_mask`, no argument is needed:
  grpc-gateway derives the mask from the PATCH body on REST, and
  `build_grpc_request` now does the same on gRPC. Only `UpdateCapability`
  qualifies today. `UpdateConfig` sends its `mask` in a `*` body. 43 entries
  remain open.
- R11 is resolved (2026-10-13). `build_grpc_request` parses the body
  strictly, so an unknown key or enum name raises `ConfigurationError` before
  the send. The proto descriptor is the schema, so no extra encoding is
  needed. A recursive check found all 235 typed request model and message
  pairs match, so only untyped `Dict` bodies (R16) can now fail. 42 entries
  remain open.
- R16 is resolved (2026-10-13). Earlier fixes had already typed 20 of the 24
  bodies. The generator now hoists the last 4 inline bodies into
  `<Service><Method>Body` schemas, so no `Dict[str, Any]` body remains. Typed
  bodies are serialized with `exclude_unset=True` on both transports: REST
  sent `null` for every unset field, which would clear fields on a PATCH. 41
  entries remain open.
- R5 is resolved (2026-10-13). A numeric `timeout` or `rest_timeout` is now a
  total deadline. The REST transport checks it when the headers arrive and on
  every body chunk, so a trickling server is cut off at most one read after
  the deadline. One gap remains: headers that trickle in are bounded per read
  only. An `httpx.Timeout` keeps httpx's per-phase meaning by design. 40
  entries remain open.
- R7 is resolved (2026-10-13). Decision: an explicit `email` or `api_token`
  argument that is empty or only whitespace raises `ConfigurationError` and
  never falls back. An empty environment variable still counts as unset, as
  shells commonly use it that way. 39 entries remain open.
- R6 is resolved (2026-10-13). `APIConfig.client` records the process ID. In
  a forked child it drops the inherited client without closing it (closing
  would send a TLS close_notify on the parent's connection), replaces the
  lock, and opens a new client. gRPC fork handling stays with gRPC
  (`GRPC_ENABLE_FORK_SUPPORT`). 38 entries remain open.
- R4 is resolved (2026-10-13). Generated REST calls pass the schema path to
  `request_json(path_template=...)`, and the quota key is
  `"<METHOD> <path template>"`, so the map holds one entry per endpoint. The
  guide reads the public `client.api_config.rate_limits`. 37 entries remain
  open.
- R9 is resolved (2026-10-13). Decision: settings are read-only after
  construction. `APIConfig` refuses assignment to its eight settings, and
  `KentikCredentials` exposes `email` and `api_token` as properties.
  `rate_limits` stays a shared, mutable map. The gRPC override check no longer
  compares fields, since a `with_timeout()` copy cannot change them. 36
  entries remain open.
- R10 is resolved (2026-10-13) without the live call. `request_json` encodes
  the query itself and writes a space as `%20`, which both Envoy and
  grpc-gateway decode as a space, so the answer to "does the server decode
  `+`?" no longer matters. httpx still renders the values (`True` as `true`).
  35 entries remain open.
- R13 is resolved (2026-10-13). `map_grpc_error` decodes
  `grpc-status-details-bin` into `details["rpc_status"]` (proto JSON, with an
  `@type`-only entry for a detail type with no descriptor). The generated REST
  error classes now store the body itself there, instead of a model dump that
  lost every detail field, so both transports match. `rate_limit_of_rpc` falls
  back to trailing metadata for trailers-only responses. 34 entries remain
  open.
- R14 is resolved (2026-10-13). Each generated wrapper keeps the exception
  its proto import raised, and the guard on each gRPC method raises
  `NotImplementedError` naming it, chained with `from`. The import still
  degrades instead of failing the client, so REST keeps working. 33 entries
  remain open.
- D3 is resolved (2026-10-13). CLAUDE.md now says: `make generate` clones
  and `local` reads the sibling checkout, with no fallback; `make all` builds
  no docs, and `make docs` regenerates from GitHub first; the guarded
  couplings name the template sentinel and `_fix_path_parameters`;
  `api_surface.py` is listed; the commit hashes that only the local
  `refactor` branch has are gone; the pre-PR steps list the five other CI
  gates. Owner review happens in the PR. 32 entries remain open.
- D4 is resolved (2026-10-13). Constitution 1.4.0: Principle VI states the
  real resolution order and forbids `load_dotenv`. The same revision fixes
  the schema-source, `make all`, gRPC-routing, and guarded-coupling drift.
  31 entries remain open.
- D5 is resolved (2026-10-13). `docs_rendering` and the regenerated
  `gen/README.md` say gRPC routing matches by HTTP rule. 30 entries remain
  open.
- D11 is resolved (2026-10-13). The spec 001 quickstart picks one file into
  `$target` before it truncates or restores, so a zsh redirect to a glob can
  no longer write to every device swagger version. 29 entries remain open.
- K8 is resolved (2026-10-13). The `build` workflow installs the wheel into a
  clean venv, runs from outside the checkout, imports every module (1317
  today), and builds a gRPC client whose 36 mounted wrappers must all have
  live stubs. Verified locally against a fresh `uv build`. 28 entries remain
  open.
- L11 is resolved (2026-10-13). fixup tests for `pb` and `error` against the
  path parts below the service directory, so a checkout under a directory
  with either name no longer skips every fixup. 27 entries remain open.
- K2 stays open (2026-10-14), by decision. `release.yml` already publishes
  the way the legacy SDK's workflow does: on a published GitHub release, with
  the `PYPI_TOKEN` secret. It keeps that setup until the PR is accepted and a
  release validates it. Trusted publishing needs the PyPI project owner, who
  is not yet known. The other K2 parts (`needs: publish`, the tag version
  gate, the pre-release rule) are already in place.
- K3 is resolved (2026-10-14). The package metadata now renders
  `README.pypi.md`, a short README with absolute links only. A packaging test
  fails on any relative link in it, or if the sdist leaves it out. The
  repository `README.md` is unchanged. A docs site is not part of this fix.
  26 entries remain open.
- D1 is resolved (2026-10-14). The generator passes the patched swagger to
  `extract()`, so every model name on a service page exists in the SDK, all
  10 required bodies show as required, and 21 of the 24 two-node model
  diagrams now show the operation models. A test fails when a committed page
  names a model the SDK does not define. 25 entries remain open.
- D2 is resolved (2026-10-14). Each service page example imports the models
  it constructs from `kentik_api.gen.<service>.models`, and a `Dict`
  argument renders as `{}`. R16 had already removed the 4 `Dict` bodies. A
  test parses every committed example and fails on a name it uses but does
  not define, or an import that does not resolve. 24 entries remain open.
- D12 is resolved (2026-10-14). The generator renders with `autoescape=True`,
  which caused the `&#34;` and `&#39;` in 5 model docstrings. Custom templates
  now escape schema text for Python instead. Each REST function and its
  wrapper method get the operation summary and description (232 of 234; two
  operations have neither). A custom model template adds
  `Field(description=...)` to 1447 of 2421 fields, every field the v3 schema
  describes. The v3 schema drops the description next to a `$ref`, so about
  390 such fields stay undescribed until upstream keeps it. The Sphinx
  build escapes RST markup in field descriptions, so text like `c_` renders
  as written. 23 entries remain open.
- P2 is resolved (2026-10-14). `openapi-python-generator==2.1.2` is in the
  `dev` group, so `uv.lock` pins it and its dependencies. Generation runs it
  and `grpc_tools.protoc` with the project interpreter, instead of `uvx` and
  `uv run --with grpcio-tools`, which resolved outside the lock. CI needed no
  change: every job already runs `uv sync --locked`. A regeneration with the
  pin changed no generated file. A fork still runs through `uvx` when
  `OPENAPI_GENERATOR_FROM` or `OPENAPI_GENERATOR_CMD` is set. 22 entries
  remain open.
- T2 is resolved (2026-10-14). `test_grpc_end_to_end.py` calls
  `device.get_device` through the real `GrpcTransport` to an in-process
  server that runs the generated `DeviceService` servicer. Only the TLS
  credentials are swapped, for gRPC local credentials. The server checks the
  auth metadata, the deadline, and the path argument. The client checks a
  populated nested response and a 404 error class. An auth plugin that sends
  no metadata fails the test. 21 entries remain open.
- T9 is resolved (2026-10-14). `build_all_kwargs` fills every field of a
  request body, nested optional fields included, except one that would
  recurse. All 339 top-level body fields now get a value (93 before). The
  e2e tests keep required fields only, since they call a real account.
- T4 is resolved (2026-10-14). The mapping test runs the real
  `build_grpc_request` on those bodies. `proto_sample_body` first swaps each
  sample the proto rejects (well-known types, int64 strings, zero enums, a
  second oneof member) and keeps unknown keys, so wrong nesting still fails
  `ParseDict`. The test checks that the body is the caller's data, at the root
  or under one field, and that every field it sends is set in the request.
  A dropped body and a body nested under the wrong field both fail it. 19
  entries remain open.
- T3 is resolved (2026-10-14). `api_surface.json` (schema version 5) records
  the RPC each operation calls on gRPC, or `null`. All 234 operations route
  today. A lost or moved route is a breaking change for
  `make check-changelog`. The wrapper contract and request mapping tests
  accept `NotImplementedError` only where the record has no route, and a
  routed call must reach the recorded RPC. A wrapper without gRPC code must
  have no `pb` stubs. Breaking the `get_device` route fails both tests. 18
  entries remain open.
- T7 is resolved (2026-10-14). `make generate` writes
  `schema_operations.json` from the patched swagger: each operation's
  operationId, parameters, body, and response codes (234 operations in 42
  services). CI's drift check keeps it in step with the schema.
  `test_schema_operations.py` holds the generated REST modules to it without a
  schema checkout, and replaces the test that always skipped in CI. A dropped
  query argument and a dropped body both fail it. The respx routes still match
  on method and path only. 17 entries remain open.
- T1 is resolved (2026-10-14). Success responses come from the proto
  descriptors, not the SDK's models: `sample_grpc_response` sets every field
  of the recorded RPC's output, except `INTERNAL` fields that the published
  schema omits. The REST coverage test and the gRPC contract test both parse
  it and require the model to dump back to the same message, so a wrong type
  or a dropped field fails. Restoring B2 fails all four alert operations on
  both transports. Decision (option A): an unknown enum value stays strict.
  gRPC now validates through REST's `parse_response_model`, so it raises the
  same `HTTPException` 502, not a raw `ValidationError`, and a test pins that
  on both transports. 16 entries remain open.
- P3 is resolved (2026-10-14). `schema.lock` pins the schema commit
  (`9de9a68`). `make generate` fetches that commit, and every completed run
  writes the commit it used, so CI's drift job (now
  `generated-output-matches-schema-pin`) no longer follows upstream HEAD.
  `make sync-schema` moves the pin. The weekly `schema-sync` workflow runs it
  and opens a pull request with the surface delta when the output changes. A
  pull request that GITHUB_TOKEN opens starts no CI, so a maintainer closes
  and reopens it. `dependabot.yml` covers `github-actions` and `uv`, and every
  action is pinned by commit SHA. Regenerating from GitHub at the pin
  reproduces the committed tree exactly. 15 entries remain open.
- P3a is opened (2026-10-14). After the merge, an admin must allow GitHub
  Actions to create pull requests, and each `schema-sync` pull request needs a
  close and reopen to start CI. The steps are in the generation guide and in
  the post-merge list in report.md. 16 entries remain open.
- P4 is resolved (2026-10-14). Before the wipe, the generator now fails when
  a schema service folder has no swagger file. The CLI copies every generated
  output (`gen/`, `client_mixin.py`, `docs/sphinx/`, `api_surface.json`,
  `schema_operations.json`, `schema.lock`) aside before the run and puts it
  back on any failure, Ctrl-C included. Decision: a snapshot, not a staging
  directory, because the phase modules write to fixed paths. Only a hard kill
  can leave a half-built tree. A run against a schema with a broken
  `user/v202211/user.proto` failed after the wipe, restored the tree with no
  differences, and `import kentik_api` still worked. 15 entries remain open.
- 2026-10-15: B11's second rule is fixed. An audit of all 234 client methods
  found 12 that broke snake_case, all with a double underscore from protoc's
  default operationId `<Module>_<Method>`. The wrapper now drops the module
  prefix; if one word is left, the module noun stays (`ktbgp.route_list`).
  Renamed: 8 in kagent, 3 in ktbgp, 1 in nms. Every other name is already
  snake_case. B11's third rule (version strings in 50 model class names) is
  still open.
- 2026-10-15: B11 is fully resolved. `public_names.json` now holds the public
  name of every Service, client method, and model, keyed by version-free
  upstream values. A run only adds entries, and fails with `NameDriftError`
  when an entry no longer matches the schema. 50 versioned model names lost
  their version (`labelv202210Label` to `Label`). A simulated upstream change
  (label version bump, operationId rename, moved DELETE path) failed once,
  naming only `delete_label`; after a one-line fix every label name was
  unchanged. Error class names still follow the operationId.
- 2026-10-15: error classes now follow the client method name
  (`list_labels` raises `ListLabelsError`), so `public_names.json` protects
  them too. An operationId rename no longer renames an error class, and
  operations that share an operationId (eight `List` in `alerting`) no longer
  share one class. `ERROR_BY_OPERATION` became `ERROR_BY_METHOD`.
- 2026-10-17: the Makefile is gone (feature 007), so P3a's mitigation now
  names `uv run poe sync-schema`. P3a and K2 stay open.
