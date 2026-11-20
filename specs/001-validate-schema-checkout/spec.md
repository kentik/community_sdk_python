# Feature Specification: Validate Schema Checkout Before Generating

**Feature Branch**: `001-validate-schema-checkout`

**Created**: 2026-08-26

**Status**: Draft

**Input**: User description: "Add a pre-flight validation check to the SDK
generator that detects when the local schema checkout used by `make generate
local` is corrupted, truncated, or otherwise structurally suspicious, and
fails the generation run loudly instead of silently producing an incomplete
SDK. This closes a gap found on 2026-08-26 where a locally corrupted
`../api-schema-public` checkout caused `make generate local` to silently
drop the kagent and monitoring services entirely, undetected by the
existing parity check."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generator refuses to run against an obviously broken schema checkout (Priority: P1)

As an SDK maintainer running `make generate local`, when my local
`../api-schema-public` checkout has been accidentally corrupted or truncated
(an interrupted edit, a bad find/replace, stale/partial content), I want the
generator to stop immediately with a clear error identifying which file(s)
look wrong, instead of silently producing an SDK that's missing services or
has gutted models.

**Why this priority**: This is the entire problem this feature exists to
solve. Today, a corrupted local checkout produces no error at all: the
generator runs to completion, the parity check passes (it only compares
generated output to that same corrupted input), and the maintainer only
discovers it later when a service has silently vanished from the SDK. This
is the only story needed for a viable first version.

**Independent Test**: Truncate a swagger file in a scratch schema checkout
to a few bytes, run `make generate local` against it, and confirm the run
fails with a clear error before writing any generated output, rather than
completing and silently omitting the affected service.

**Acceptance Scenarios**:

1. **Given** a local schema checkout where every discovered swagger file
   parses as valid, non-trivially-sized JSON with the expected top-level
   OpenAPI structure, **When** `make generate local` runs, **Then**
   generation proceeds exactly as it does today.
2. **Given** a local schema checkout containing a swagger file that is
   empty, truncated, or fails to parse as valid JSON, **When** `make
   generate local` runs, **Then** the generator stops before generating any
   output and reports the specific file path(s) that failed validation.
3. **Given** a local schema checkout containing a swagger file that parses
   as valid JSON but is missing required top-level OpenAPI keys (e.g.
   `paths`, `info`), **When** `make generate local` runs, **Then** the
   generator stops and reports the specific file and the missing key(s).

### Edge Cases

- What happens when the schema source is the network-cloned fallback (no
  `--local-repo`) instead of a local checkout? The clone is fresh from the
  canonical remote each time, so it's inherently less likely to be
  corrupted, but the same validation MUST still run against it for
  consistency and to catch transient clone/network truncation too.
- What happens when a swagger file is legitimately tiny (e.g. a service
  with only one operation)? Validation MUST NOT reject small-but-valid
  files. The check is structural validity (parses as JSON, has the
  expected top-level keys), never a bare size threshold.
- What happens when multiple files are corrupted at once? All of them MUST
  be reported in one run, not just the first, so the maintainer can fix
  everything before re-running.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The generator MUST validate every swagger file it selects
  to generate from (the newest file of each swagger family) before
  generating any code from it.
- **FR-002**: Validation MUST reject a file that is empty or fails to parse
  as JSON.
- **FR-003**: Validation MUST reject a file that parses as JSON but is
  missing required top-level OpenAPI keys (`paths`, `info`, and one of
  `swagger`/`openapi`).
- **FR-004**: When validation fails for one or more files, the generator
  MUST stop before generating or writing any output for that run, and MUST
  report every failing file path together with the specific reason it
  failed.
- **FR-005**: Validation MUST run identically regardless of whether the
  schema source is the local checkout (`--local-repo`) or the
  network-cloned fallback.
- **FR-006**: Validation failure MUST produce a non-zero process exit code,
  so it fails `make`/CI invocations rather than merely printing a warning.

### Key Entities *(include if feature involves data)*

- **Schema file validation result**: one discovered swagger file, whether
  it passed or failed, and (if failed) the specific reason.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `make generate local` against a schema checkout with
  at least one truncated/empty/invalid-JSON swagger file fails with a
  non-zero exit code and a clear listing of every offending file, before
  any file under `src/kentik_api/gen/` is written or modified.
- **SC-002**: Running `make generate local` (or `make generate`) against a
  fully valid schema checkout behaves exactly as before this change, with zero
  difference in output for the non-corrupted case.
- **SC-003**: The specific 2026-08-26 incident (a swagger file truncated
  from 1625 lines to 1) is caught by this check, verified by a regression
  test using a fixture file of that shape.

## Assumptions

- "Corrupted" is scoped to structural validity (parses as JSON, has the
  expected top-level OpenAPI keys). This feature does not attempt semantic
  schema validation (e.g. full OpenAPI schema conformance), which is a much
  larger effort and not what the 2026-08-26 incident needed.
- This validates the schema *source* files before generation; it is not a
  substitute for the existing parity check, which validates generator
  *output* against that same source. Both remain necessary: this one
  catches corrupted/truncated input, not e.g. a service legitimately
  removed upstream.
- This feature validates the *content* of each discovered swagger file. It
  does not detect a whole service directory silently disappearing from the
  schema tree (which is a *file-discovery* problem, not a *file-content*
  problem). On 2026-08-26 the `kagent`/`monitoring` services were missing
  from the corrupted checkout's directory listing entirely, a distinct
  mechanism from the confirmed `device.swagger.json` content truncation
  this feature targets. Catching a shrinking service count would need a
  separate check (e.g. comparing the freshly discovered service list
  against what's currently committed under `src/kentik_api/gen/`) and is
  intentionally out of scope here.
