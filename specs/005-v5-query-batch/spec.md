# Feature Specification: V5 Query and Batch Support in the Generated SDK

**Feature Branch**: `feat/005-v5-query-batch`

**Created**: 2026-10-16

**Status**: Draft

**Input**: User description: "The V5 query and batch endpoints still answer, and
a V6 query service is still planned. Spec out support for the V5 query API and
similar functionality, with as little friction as possible, in the modern
generated SDK. Give at least a similar experience to V5, plus more. Where the
modern way breaks some V5 behavior, lean toward the modern way."

## Background

The V5 SDK (1.x, on `origin/main`) gave users two capabilities that the V6
SDK (2.x) does not have:

- The query API: `query.sql`, `query.data` (top-X data), `query.chart` (a
  chart image), and `query.url` (a Data Explorer link). It was the only way
  to get flow and traffic data through the SDK.
- The batch API: bulk create, update, and delete of flow tags and of custom
  dimension populators, with a status call to follow progress.

On top of the query API, the optional `analytics` package turned results into
pandas DataFrames, cached them on disk, and found flat-traffic periods on
links. `DeviceCache` mapped device and interface names to devices and link
speeds.

Kentik confirmed on 2026-10-16 that the V5 query and batch endpoints still
answer, and that a V6 query service is planned but not yet published. The
V6 public schema has no description of the V5 endpoints, so the generator
cannot produce them today. [The V5 to V6 audit](../../reports/upstream/v5-feature-parity-audit.md)
lists these gaps.

A live check on 2026-10-16 (see the audit's "Live check" section) showed:

- `query/topXdata` and `query/url` answer. `query/topXchart` gave no response
  in 180 seconds. `query/sql` returns 403, and the Kentik Knowledge Base says
  that Kentik retired it on 2025-05-01.
- The batch status endpoint answers.
- Every other V5 endpoint that the V5 SDK called has a V6 equivalent.
- V5 responses carry no rate limit headers.

## Clarifications

### Session 2026-10-16

- Q: Which V5 endpoints does the SDK add? → A: Only V5 endpoints that have no
  V6 equivalent (the query and batch endpoints). A V5 endpoint with a V6
  equivalent is not added. The migration guide maps it to the V6 call, so the
  new SDK never has two calls for the same thing.
- Q: How does a 2.x client find the host for the V5 endpoints? → A: From
  its region (`us` uses `https://api.kentik.com/api/v5`, `eu` uses
  `https://api.kentik.eu/api/v5`). A separate, optional V5 base URL setting
  covers custom hosts.
- Q: Should the SDK include the chart query, which gave no response in 180
  seconds in the live check? → A: Yes. The docs mark it as not verified, its
  end-to-end test treats a timeout as an expected failure, and we ask Kentik
  about it. The docs also give step-by-step instructions to test it by hand.
- Q: What public name do the V5-backed calls get on the client? → A: One
  service, `client.v5`, that holds the query and batch calls (for example
  `client.v5.top_x_data(...)`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Query flow data from a V6 client (Priority: P1)

A network engineer has a V5 script that runs a top-X query and reads
the result rows. They upgrade to 2.x. They call the query from the same
`KentikAPI` client that they use for every other service, with typed request
models, and they get typed results back.

**Why this priority**: The query API was the only way to get flow data
through the SDK. Without it, every V5 query user is blocked from upgrading.

**Independent Test**: With only this story built, a user runs a top-X data
query, a chart query, and a URL query from a 2.x client against a mocked API,
and gets result rows, an image, and a URL.

**Acceptance Scenarios**:

1. **Given** a V5 script that used `query.sql`, **When** the user reads the
   migration guide, **Then** the guide says that Kentik retired the SQL
   endpoint and shows the same data as a top-X query.
2. **Given** a top-X query with several buckets, **When** the user runs it,
   **Then** the SDK returns the results of each bucket, including the time
   series of each row when the query asks for it.
3. **Given** a chart query, **When** the user runs it and passes the
   response to one SDK helper, **Then** the helper returns the image as
   bytes, with its image type, and the user writes no decoding code.
4. **Given** a URL query, **When** the user runs it, **Then** the SDK
   returns the Data Explorer link as text.
5. **Given** a client that the user created with `protocol="grpc"`, **When**
   the user runs any query, **Then** the query works, because the V5
   endpoints exist only on REST.
6. **Given** a query that the API rejects, **When** the user runs it,
   **Then** the SDK raises the same exception types as every other 2.x
   operation, with the status and the message.

---

### User Story 2 - Bulk-sync flow tags and populators (Priority: P2)

An automation engineer syncs thousands of flow tags or populator entries from
a CMDB or an IPAM system. They send the whole set in one batch request, then
wait until Kentik finishes it, and they see how many items succeeded or
failed.

**Why this priority**: Without the batch API, a sync becomes thousands of
single calls. That is slow and uses up the rate limit. This story serves a
smaller group of users than Story 1.

**Independent Test**: With only this story built, a user sends a batch of
flow tag upserts and deletions against a mocked API, waits for completion,
and reads the final status.

**Acceptance Scenarios**:

1. **Given** a list of flow tag upserts and deletions, **When** the user
   sends them as one batch, **Then** the SDK returns the batch identifier
   that the API gives.
2. **Given** a populator batch for one custom dimension, **When** the user
   sends it, **Then** the SDK sends it for that dimension only.
3. **Given** a batch identifier, **When** the user asks for its status,
   **Then** the SDK returns the counts of upserts and deletions, the errors,
   and whether the batch is complete.
4. **Given** a sent batch, **When** the user asks the SDK to wait for it,
   **Then** the SDK polls the status until the batch is complete or a time
   limit that the user sets expires.
5. **Given** a set that is larger than one request can hold, **When** the
   user sends it, **Then** the SDK splits it into parts of one batch and
   marks the last part complete.

---

### User Story 3 - Analyze query results with pandas (Priority: P3)

A data analyst who used the V5 `analytics` package installs the analytics
extra. They turn query results into DataFrames, keep their saved query
definitions, cache results on disk, and run the flat-traffic analysis.

**Why this priority**: It restores the V5 analytics experience, which is
the most valuable layer on top of the query API. It depends on Story 1.

**Independent Test**: With Stories 1 and 3 built, a user loads a saved query
definition from a YAML file, gets a DataFrame for a time range from a mocked
API, caches it, and runs the flat-traffic analysis on it.

**Acceptance Scenarios**:

1. **Given** the analytics extra is installed, **When** the user converts a
   query result, **Then** the SDK returns a DataFrame with typed columns and
   a time index.
2. **Given** a V5 YAML query definition, **When** the user loads it,
   **Then** it runs without changes, except for SQL definitions, which
   Kentik retired, and options that executed code.
3. **Given** a definition that asks to execute code (the V5 `@fixup:`
   option), **When** the user loads it, **Then** the SDK refuses it with a
   clear error that names a safe alternative.
4. **Given** cached results for part of a time range, **When** the user asks
   for the whole range, **Then** the SDK fetches only the missing part and
   removes duplicate rows.
5. **Given** device and interface data and a traffic DataFrame, **When**
   the user runs the flat-traffic analysis, **Then** the SDK reports the
   links and the time windows where outbound traffic stayed flat.
6. **Given** the analytics extra is not installed, **When** the user calls
   an analytics helper, **Then** the SDK raises an error that names the
   extra to install. The rest of the SDK keeps working.

---

### User Story 4 - Migrate a V5 script with little friction (Priority: P2)

A user with a working V5 query, batch, or analytics script follows the
migration guide. For each V5 call, the guide gives the 2.x call. Ported
examples show the full workflow.

**Why this priority**: The value of Stories 1 to 3 depends on users finding
and adopting them. Low friction is an explicit goal of this feature.

**Independent Test**: A reviewer takes each V5 query, batch, and analytics
example from `origin/main` and ports it with only the migration guide and
the 2.x examples.

**Acceptance Scenarios**:

1. **Given** any V5 call, **When** the user looks it up in the migration
   guide, **Then** the guide gives the 2.x equivalent, or says why there is
   none.
2. **Given** each V5 example that used queries, batches, or analytics,
   **When** the user opens the 2.x examples, **Then** a ported example does
   the same work.
3. **Given** a V5 field name that the modern model renames, **When** the
   user reads the guide, **Then** the guide gives the old and the new name.

---

### User Story 5 - Move to the V6 query service when it ships (Priority: P3)

When Kentik publishes the V6 query service, the SDK gains it from the next
schema update. Users of the V5-backed query calls keep working, and they
read which V6 calls replace them.

**Why this priority**: The V6 query service does not exist yet. This story
makes sure that this feature does not block it or break users when it
arrives.

**Independent Test**: A reviewer adds a fake V6 query service to a test
schema, regenerates, and confirms that both the V6 service and the
V5-backed calls are present and that no public name changed.

**Acceptance Scenarios**:

1. **Given** a schema update that adds a V6 query service, **When** the SDK
   is regenerated, **Then** the V6 service appears under its own name, and
   no V5-backed public name changes.
2. **Given** the V6 query service exists, **When** a user calls a V5-backed
   query, **Then** the documentation names the V6 replacement, and the call
   still works until Kentik retires the V5 endpoint.

### Edge Cases

- A top-X query returns zero rows: the SDK returns an empty result,
  and the analytics helpers return an empty DataFrame with the expected
  columns.
- A query has no `device_name`: the API returns 400 even when `all_selected`
  is true, and the SDK raises the normal 2.x error with that message.
- A query returns columns that the request model did not predict: the SDK
  keeps them in the result rows and does not fail.
- The API returns an enum value that the SDK does not know in a query or
  batch response: the call succeeds and keeps the raw value.
- A chart response has a data URI that is not valid: the SDK raises a clear
  error, not a decoding error from a library.
- A chart query gets no response in the timeout: the SDK raises the normal
  2.x `TransportError`, and the user can raise the timeout for that call.
- V5 responses carry no rate limit headers: the quota of a V5-backed call is
  empty, and a 429 raises the normal 2.x error without quota data.
- A batch status call fails while the SDK waits: the SDK raises the error
  and does not resend the batch.
- The user sets a wait time limit, and the batch does not finish in that
  time: the SDK raises a timeout error with the last status it read.
- A batch part fails in the middle of a split set: the SDK stops, reports
  which parts it sent, and does not resend the parts that succeeded.
- The cache directory holds a file that the SDK did not write: the SDK
  ignores it and never executes its content.
- Kentik retires a V5 endpoint: the call raises the normal 2.x error for
  the status that the API returns.

## Requirements *(mandatory)*

### Functional Requirements

#### Query API

- **FR-001**: The SDK MUST give the V5 query operations that still answer
  (top-X data, top-X chart, and Data Explorer URL) on the `KentikAPI` client.
  It MUST NOT give the retired SQL operation.
- **FR-002**: Each query operation MUST take a typed request model that
  types every field that the Kentik Query API documentation lists. The
  model MUST keep and send every other field it gets, so that every field
  of the V5 SDK's query models, and query JSON copied from Data Explorer,
  reaches the API unchanged.
- **FR-003**: The SDK MUST return query results as typed models. Result rows
  MUST keep columns that the request model did not predict.
- **FR-004**: The chart operation MUST return the response as the API
  sends it, and an SDK helper MUST decode that response to the image bytes
  and the image type (see research R7). Until a live call returns a chart,
  the documentation MUST mark the chart operation as not verified.
- **FR-004a**: The documentation MUST give step-by-step instructions to test
  the chart operation by hand against the real API, including how to raise
  the timeout and how to report the result.
- **FR-005**: Query operations MUST work on a client with either transport
  setting, because the V5 endpoints exist only on REST.
- **FR-006**: Query and batch operations MUST use the same shared
  connection path as every other 2.x operation. They MUST get the same
  credential handling, timeouts, proxy support, and error types. Their quota
  is empty, because V5 sends no rate limit headers.
- **FR-006a**: The client MUST pick the V5 base URL from its region: `us`
  uses `https://api.kentik.com/api/v5`, and `eu` uses
  `https://api.kentik.eu/api/v5`. The client MUST also take an optional V5
  base URL setting, separate from the V6 base URL, for custom hosts. A
  custom V5 base URL MUST use `https`, or the client raises
  `ConfigurationError`. The SDK
  MUST NOT derive the V5 URL by rewriting the V6 URL.
- **FR-007**: The query and batch operations (the HTTP calls and their
  models) MUST be produced by the same generation pipeline as every other
  service. Their input MUST be a machine-readable description of the V5
  endpoints, kept in the repository. Hand-written helpers MAY call the
  generated operations, and MUST NOT send HTTP requests themselves.
- **FR-008**: The public names of the `v5` service, its
  operations, and their models MUST be recorded and protected like every
  other public name, and they MUST appear in the recorded API surface.
- **FR-009**: All V5-backed calls MUST be in one service named `v5`
  (`client.v5`, `kentik_api.gen.v5`). It MUST NOT take a name that the V6
  query service is likely to use, such as `query`.
- **FR-010**: Query responses MUST accept enum values that the SDK does not
  know, and keep the raw value.
- **FR-010a**: The SDK MUST NOT add a V5 endpoint that has a V6 equivalent.
  Only V5 endpoints with no V6 equivalent are in scope.

#### Batch API

- **FR-011**: The SDK MUST give the V5 batch operations for flow tags and
  for populators of one custom dimension, and the batch status operation.
- **FR-012**: The SDK MUST give a helper that waits for a batch to finish,
  with a time limit and a poll interval that the user sets.
- **FR-013**: The SDK MUST give a helper that splits a large set into the
  parts of one batch, and marks only the last part complete.
- **FR-014**: The SDK MUST NOT resend a batch request automatically.

#### Analytics

- **FR-015**: The SDK MUST give an optional extra, named `analytics` as in
  V5, that installs the data analysis dependencies. The base install MUST
  NOT require them.
- **FR-016**: The SDK MUST convert top-X results into DataFrames, with
  column types and a time index, as the V5 query definitions did.
- **FR-017**: The SDK MUST read V5 query definition files and dictionaries,
  including their time placeholders and column mappings. A SQL definition
  MUST fail with an error that says Kentik retired the SQL endpoint.
- **FR-018**: Query definitions MUST NOT execute code from a file or a
  string. A definition that asks for code execution MUST fail with an
  error that names a safe alternative.
- **FR-019**: The SDK MUST cache DataFrames on disk by time range, fetch
  only missing ranges, and remove duplicate rows. The cache MUST use a data
  format that cannot execute code when it is read.
- **FR-020**: The SDK MUST give the V5 flat-traffic analysis with the same
  inputs and outputs.
- **FR-022**: When the analytics extra is not installed, an analytics
  helper MUST raise an error that names the extra. Other SDK functions MUST
  keep working.

#### Helpers (base install)

- **FR-021**: The SDK MUST give a device lookup helper that loads devices
  and interfaces once, finds them by ID or by name, builds link names, and
  returns link speeds. It MUST save and load its data only in a format that
  cannot execute code. It needs no extra.

#### Migration and documentation

- **FR-023**: The migration guide MUST map every V5 call to its 2.x
  equivalent, including each V5 endpoint that already has a V6 equivalent,
  with old and new names for each renamed field. It MUST say why a V5 call
  has no equivalent (for example, the retired SQL endpoint).
- **FR-024**: The SDK MUST ship a ported example for each V5 example that
  used queries, batches, or analytics, and a test MUST fail when an example
  no longer matches the SDK.
- **FR-025**: The documentation MUST state that the `v5` service is
  a bridge until the V6 query service ships, and MUST name the V6
  replacement of each call once it exists.
- **FR-026**: The documentation MUST state that V5-backed calls report no
  quota, and give a retry recipe for a 429 response that does not depend on
  quota headers.

#### Testing

- **FR-027**: The mocked test suites MUST cover every query and batch
  operation, every request field, and every response status, as for every
  other service.
- **FR-028**: The opt-in end-to-end suite MUST cover every query operation
  against the real API. A chart timeout MUST count as an expected failure,
  not a pass, until Kentik confirms the endpoint. Batch end-to-end coverage
  MUST use only disposable data with guaranteed cleanup, and it MUST be
  called out when it is added.

### Key Entities

- **Query request**: one or more queries, each with a bucket name, the
  dimensions, the metrics, the time range (fixed or a lookback), the
  filters, the device selection, and the chart options.
- **Query result**: for each bucket, the result rows, and for top-X queries
  the time series of each row. For a chart, the data URI, which a helper
  decodes to the image bytes and type. For a
  URL query, the link.
- **Batch part**: a set of upserts and deletions, a replace-all flag, a
  complete flag, and the batch identifier that links the parts.
- **Batch status**: the counts of received and processed upserts and
  deletions, the errors, and whether the batch is complete.
- **Query definition**: a saved query with time placeholders and a column
  mapping, written in a file or a dictionary.
- **Result cache**: stored DataFrames, keyed by query and time range.
- **Device lookup**: devices and interfaces by ID and by name, with link
  names and link speeds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the V5 query and batch operations that still answer
  have a 2.x equivalent, and 100% of the other V5 calls have an entry in the
  migration guide.
- **SC-002**: Each V5 example that used queries, batches, or analytics runs
  on 2.x after a port, and each port changes no more than the client setup,
  the call names, and the field names that the migration guide lists.
- **SC-003**: For the same query and time range, the 2.x analytics helpers
  return the same columns and the same values as the V5 helpers.
- **SC-004**: A user can sync 10,000 flow tags with no more than 1% of the
  API calls that one call per tag needs.
- **SC-005**: No query definition, cache file, or device lookup file can
  execute code when the SDK reads it.
- **SC-006**: When the V6 query service ships, the SDK gains it from one
  schema update with no change to a V5-backed public name.
- **SC-007**: The mocked suites cover 100% of the query and batch
  operations, request fields, and response statuses.
- **SC-008**: A user who knows only the 2.x client finds the query, batch,
  and analytics calls from the documentation index in under 5 minutes.

## Assumptions

- The V5 query and batch endpoints keep their current request and response
  shapes until Kentik retires them. Kentik confirmed on 2026-10-16 that
  they still answer, and a live check confirmed it for `topXdata`, `url`, and
  the batch status call.
- The V5 endpoints use the same credentials as the V6 REST API, but other
  hosts (see FR-006a).
- A machine-readable description of the V5 endpoints does not exist
  upstream. This feature writes and maintains one in the repository, from
  the V5 SDK models and the Kentik API documentation, until the V6 query
  service replaces it.
- The modern way wins where it conflicts with V5 behavior, as the user
  asked. In particular:
  - Results are typed models, not V5 dataclasses.
  - Request fields keep the wire names of the API, as every other 2.x
    model does.
  - There is no automatic retry. A 429 raises the normal 2.x error with
    the quota, and the documentation gives a retry recipe.
  - Errors are the 2.x exception types, not the V5 error classes.
  - There is no compatibility layer for V5 import paths.
- The V5-backed calls live in one service, `v5` (see FR-009). This reserves
  `query` for the V6 service. The method names are decided in planning and
  recorded in `public_names.json`.
- The analytics extra keeps the V5 name, `analytics`, so that existing
  install commands work.
- Notebook demos and chart visualization beyond the image bytes are out of
  scope.
- The V6 query service is out of scope for this feature. Only its future
  arrival is planned for.
