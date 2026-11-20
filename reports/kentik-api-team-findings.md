# Upstream Issues Affecting Kentik SDK

> [!WARNING]
> This report includes findings from a lab account. It does not establish
> authorization behavior for private routes. Keep it within the API and SDK
> teams until they review the schema exposure findings.

Reviewed: 2026-11-19. This is the single current tracker for upstream issues
that affect the Kentik Community Python SDK. It links supporting evidence under
[`upstream/`](upstream/). It distinguishes confirmed behavior from old claims
that need a safe recheck.

## Executive summary

The review covers 16 unresolved upstream items across runtime behavior, schema
publication, rate-limit documentation, and the generator dependency. The
latest read-only E2E run passed 92 tests, skipped 145 mutating operations,
deselected 277 tests, and reported 17 expected xfails. The xfails are evidence
of known behavior, not unexpected test failures.

The current SDK mitigates two issues: it sends proto field names for two REST
updates that reject the documented JSON names, and it suppresses deadlines on
six gRPC services that fail when a deadline is present. The SDK cannot repair
server-side 500 or 501 responses, missing REST bindings, or unclear API
contracts.

## Finding register

| ID | Finding | Current state | Latest evidence | SDK effect |
| --- | --- | --- | --- | --- |
| UP-01 | REST update body keys conflict with the published contract | Confirmed; SDK workaround | 2026-10-27 | Two updates work through REST only because the SDK sends proto field names. |
| UP-02 | `CreateFlowTag` returns HTTP 500 | Confirmed over REST; gRPC untested | 2026-10-27 | Flow-tag creation is unavailable over the tested REST path. |
| UP-03 | AutoAck `Replace` returns `SyntaxError` | Observed; separate from body parsing | 2026-10-27 | The real-record update path remains unresolved. |
| UP-04 | gRPC deadline causes `RangeError` on six services | Confirmed; SDK workaround | 2026-10-27 | The SDK omits server deadlines and cancels calls locally. |
| UP-05 | Filtered `CreateSavedFilter` returns HTTP 500 | Old result; recheck needed | 2026-10-26 | Filter creation may fail; current status is unknown. |
| UP-06 | Missing custom application returns HTTP 200 with an empty object | GET confirmed; repeated DELETE is stale | 2026-10-27 | The response can look successful unless callers inspect the empty ID. |
| UP-07 | Missing AS group or site market returns HTTP 400 | Confirmed | 2026-10-27 | Missing resources use `INVALID_ARGUMENT`, unlike other services. |
| UP-08 | Missing IDs return HTTP 500 in alerting, audit, and vault | Reproduced by current E2E xfails | 2026-11-19 | Callers receive server errors for missing resources. |
| UP-09 | Malformed IDs return HTTP 500 | Reproduced by current E2E xfails | 2026-11-19 | Invalid path values reach handlers instead of returning `INVALID_ARGUMENT`. |
| UP-10 | Published operations return HTTP 501 | Reproduced by current E2E xfails and a separate probe | 2026-11-19; 2026-10-27 | Generated methods exist, but the server does not implement several. |
| UP-11 | Public `kptr` and `deviceconf` RPCs have no HTTP bindings | Confirmed in the pinned schema | Pin `9f58fdd`; audit `dbe7ce6` | 13 candidate RPCs have no generated REST methods. |
| UP-12 | Private or protected services publish REST operations | Confirmed in schema; authorization unknown | Pin `9f58fdd`; audit `dbe7ce6` | The SDK exposes routes marked `PRIVATE` or `PROTECTED`; access was not tested. |
| UP-13 | Rate-limit documentation conflicts with observed headers | Scope observed; other limits unverified | 2026-10-27 | Clients cannot tell whether an account-wide or per-endpoint budget governs. |
| UP-14 | V5 `topXchart` does not return a response | Current expected xfail | 2026-11-19 | A chart call can time out while the server may still hold a query slot. |
| UP-15 | V5 batch success response contract is unclear | HTTP 200 observed; contract unresolved | 2026-10-27 | Callers do not know which success status or batch ID to rely on. |
| UP-16 | Generator installs unused formatter packages | Confirmed for locked version 2.1.2 | Lockfile review | `black`, `isort`, and `orjson` remain required despite `--formatter none`. |

## Runtime defects and behavior gaps

### UP-01: REST update body keys conflict with the published contract

**State:** Confirmed on 2026-10-27. The SDK has a workaround.

`UpdateASGroup` and `UpdateSiteMarket` reject the OpenAPI camelCase body keys
`asGroup` and `siteMarket`. The same calls work when the body uses proto names
`as_group` and `site_market`. The SDK rewrites those keys, so its calls work,
but clients that follow the published schema still fail. The common server-side
cause is not confirmed.

**Ask:** Accept the documented JSON keys while merging the URL-bound ID into
the same object. See the [body-merge report](upstream/upstream-rest-update-body-merge.md).

### UP-02: `CreateFlowTag` returns HTTP 500

**State:** Confirmed over REST on 2026-10-27. The gRPC create path was not
checked.

The create request returns HTTP 500 `StatusCodeError`, including a minimal
name-only request. The successful `UpdateFlowTag` check on the same date means
the old claim that every FlowTag write fails is stale.

**Ask:** Return a valid created object or a client error for an invalid body.
Check gRPC create with an approved disposable tag before claiming that both
transports fail.

### UP-03: AutoAck `Replace` returns `SyntaxError`

**State:** Observed on 2026-10-27. This is not the REST body-merge failure.

A missing-ID validation control showed that the server reads the documented
camelCase `autoAck` body. The separate real-record `Replace` call returned
`SyntaxError`; the cause and affected payload remain unclear.

**Ask:** Inspect the recorded server request and provide a safe reproduction
with an approved disposable rule. Keep this separate from UP-01.

### UP-04: gRPC deadlines fail on six services

**State:** Reproduced on 2026-10-27 for `alerting`, `audit`,
`custom_application`, `custom_dimension`, `plan`, and `saved_filter`.
The SDK has a workaround.

The server returns `RangeError` when these calls carry `grpc-timeout`. Source
inspection and a local reproduction point to a cyclic grpc-js call object
being passed through a recursive `camelify` function. Production logs have
not confirmed that cause. The SDK sends no server deadline for these services
and cancels each call at the configured deadline.

**Ask:** Confirm the cause in server logs. Avoid recursively transforming the
call object or register these services without camelification. The strict
mutating canary is in
[`test_upstream_workarounds_e2e.py`](../tests/e2e/test_upstream_workarounds_e2e.py).

### UP-05: Filtered `CreateSavedFilter` returns HTTP 500

**State:** A prior result from 2026-10-26. It has not been rechecked.

Requests with a filter group and rule returned `ValidationError`; a name-only
request succeeded. The available evidence does not establish whether the
problem still occurs or which filter shape triggers it.

**Next step:** Recheck only with an approved disposable saved filter and
guaranteed cleanup. Do not file it as a current confirmed defect until then.
See [historical reproduction details](archive/upstream-jira-drafts.md#4-createsavedfilter-with-a-filter-rule-returns-500-validationerror).

### UP-06: Missing custom application returns HTTP 200 with an empty object

**State:** The empty GET response was confirmed on 2026-10-27. A repeated
DELETE returned 500 in an older test and needs a new check.

GET of a missing custom application returns an object whose ID is empty. This
does not look like a not-found response to callers who check only HTTP status.
The E2E cleanup helper detects this empty ID, but normal SDK calls still
return the generated model.

**Ask:** Return 404 for a missing ID, or document and standardize an empty
response. Recheck repeated DELETE only with a disposable application.

### UP-07: Missing AS groups and site markets return HTTP 400

**State:** Confirmed on 2026-10-27.

Missing AS group and site-market IDs return HTTP 400 `INVALID_ARGUMENT` with
“does not exist” messages. A missing FlowTag returns HTTP 404 `NOT_FOUND`.
This forces callers to interpret endpoint-specific status codes for the same
condition.

**Ask:** Use `NOT_FOUND` consistently, or document why these endpoints use
`INVALID_ARGUMENT`.

### UP-08: Missing IDs return HTTP 500 in alerting, audit, and vault

**State:** Reproduced in the read-only E2E suite on 2026-11-19.

The failing operations include AutoAck, comments, silence notifications,
suppressions, audit event reads, and vault secret reads. The read-only suite
uses strict expected failures, so an upstream fix will produce an XPASS and
require removal of the canary.

**Ask:** Return `NOT_FOUND` for missing objects. See the operation list in
[`upstream_bugs.py`](../tests/e2e/upstream_bugs.py).

### UP-09: Malformed IDs return HTTP 500

**State:** Reproduced in the read-only E2E suite on 2026-11-19.

Malformed IDs in alerting, custom application, and KMI reads can reach the
handler and return HTTP 500 instead of HTTP 400 `INVALID_ARGUMENT`. The gRPC
policy read also has a known malformed-ID failure.

**Ask:** Validate path values at the gateway or handler boundary and return a
client error that names the invalid field.

### UP-10: Published operations return HTTP 501

**State:** Reproduced in the read-only E2E suite on 2026-11-19. A separate
`ktbgp` probe returned 501 on 2026-10-27.

The current E2E xfails cover `kagent.get_capability`,
`kagent.list_capabilities`, `kmeta.get_service_now_config`,
`kmeta.list_service_now_configs`, and
`synthetics.get_bulk_update_tests_status`. The `ktbgp.RouteService.List`
probe also returned `UNIMPLEMENTED`.

**Ask:** Implement each published operation or remove it from public OpenAPI
until the server supports it. The SDK should not silently hide these methods
without an upstream decision.

### UP-14: V5 `topXchart` does not return a response

**State:** The expected-failure E2E test still timed out on 2026-11-19. A
180-second live probe also timed out in October.

The same query succeeds through `topXdata`. A chart request can continue to
hold one of the Query API's four server-side slots after the client times out.
The E2E test runs last for this reason.

**Ask:** Confirm whether V5 chart generation is supported and bounded. Avoid
batching or looping this call until the API team explains the timeout.
See the [V5/V6 parity report](upstream/v5-feature-parity-audit.md).

## Schema and publication gaps

### UP-11: Public `kptr` and `deviceconf` RPCs have no HTTP bindings

**State:** Confirmed in the SDK's schema pin, `9f58fdd`. An offline audit of
schema HEAD `dbe7ce6` finds the same affected files; only unrelated `kagent`
files differ from the pin.

Four `kptr` RPCs and nine eligible `deviceconf` RPCs have no
`google.api.http` binding. `deviceconf.ExecuteCommand` is method-private and
is excluded. The two `diagnostic` RPCs are marked `PUBLIC_KENTIK` and remain
out of scope. The SDK therefore generates models but no REST operations for
these methods.

**Ask:** Add HTTP bindings or confirm these methods are gRPC-only. See the
[HTTP-binding report](upstream/upstream-kptr-missing-http-annotations.md).

### UP-12: Private and protected operations appear in public OpenAPI

**State:** Confirmed in the SDK's schema pin. Whether an ordinary customer
token can call these routes is unknown and was not tested.

The public schema publishes 10 `PRIVATE` REST operations across `ktbgp`,
`vault`, and kagent's `CapabilityAdminService`, plus three `PROTECTED` reads
from `CapabilityReleaseService`. The custom visibility option is not carried
into OpenAPI, so downstream generators cannot honor it. This report does not
claim a security vulnerability or that authorization is absent.

**Ask:** Define `PRIVATE`, `PROTECTED`, and `PUBLIC_KENTIK`; confirm whether
ordinary customer tokens may call these routes; and expose visibility in
OpenAPI or omit non-public operations. See the
[visibility report](upstream/upstream-service-visibility-exposure.md).

## Documentation and dependency issues

### UP-13: Rate-limit documentation conflicts with observed headers

**State:** Per-endpoint behavior was observed on 2026-10-27. Concurrency,
soft-delay, hourly limits, and exceed behavior remain unverified.

The API advertised `60, 60;w=60`. REST and gRPC calls to the device-list
endpoint shared a counter. Site and site-market calls used separate counters.
The Knowledge Base describes per-customer limits and additional limits that
the response headers do not show. The probe was read-only and did not exhaust
any quota.

**Ask:** State which limits apply to V6, which counter the headers describe,
and whether the documented concurrency, delay, and hourly limits remain in
force. See the [rate-limit report](upstream/upstream-ratelimit-scope-undocumented.md).

### UP-15: V5 batch success contract is unclear

**State:** HTTP 200 was observed on 2026-10-27. No request ID was captured.

The evidence does not settle whether 200 is the intended success code or
whether the response must contain a batch ID.

**Ask:** Confirm the documented success code and required response fields.
Do not present this as a confirmed defect until the contract is clear.

### UP-16: `openapi-python-generator` installs unused formatter packages

**State:** Confirmed against locked version 2.1.2. The draft issue is not
recorded as filed.

The SDK runs the generator with `--formatter none`, but the package still
requires `black`, `isort`, and `orjson`. These packages remain in the locked
development dependency graph.

**Ask:** Make formatter and alternate JSON packages optional, or provide a
no-formatter extra with a clear missing-dependency error. The request draft
is in [upstream/](upstream/upstream-openapi-python-generator-optional-formatters.md).

## Stale or out-of-scope findings

- The alert-list `startedAt` requirement did not reproduce on 2026-10-27.
  Seven request bodies returned HTTP 200. Keep the older report as history.
- The claim that all FlowTag writes fail is stale. `UpdateFlowTag` accepted
  the documented body on 2026-10-27. The `CreateFlowTag` failure remains UP-02.
- The AutoAck body parses camelCase in a missing-ID control. Its `SyntaxError`
  remains a separate UP-03 issue.
- `P3a` and `K2` in the pre-PR ledger concern repository administration and
  release ownership. They are not upstream API findings.

## Next actions

1. Send separate API reports for confirmed runtime failures. Keep request
   shapes and services separate where the cause is unknown.
2. Ask the schema team to resolve the HTTP-binding and visibility questions.
3. Ask the API team to clarify V6 rate limits and the V5 batch response
   contract.
4. Recheck UP-05 and the repeated-delete part of UP-06 only with disposable
   resources and guaranteed cleanup.
5. File UP-16 with the `openapi-python-generator` maintainers and add its
   issue link to the SDK dependency guide.

## Review basis

This review did not make live API calls. It uses the 2026-11-19 read-only E2E
run, the dated local evidence, the SDK code and the schema audit. The schema
audit read commit `dbe7ce6`; a file-level comparison found no changes to the
affected services relative to the SDK pin `9f58fdd`.

Supporting reports, archived drafts, and probes live under
[`upstream/`](upstream/) and [`archive/`](archive/). Reusable probes live in
[`scripts/`](scripts/). Local account captures remain ignored under
[`local-evidence/`](local-evidence/).
