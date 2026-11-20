# Research: V5 Query and Batch Support in the Generated SDK

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-10-16

Each section records one decision, why it was made, and what else was
considered. File and line references point at the `feat/005-v5-query-batch`
tree on 2026-10-16.

## R1. Where the V5 description lives, and its format

- **Decision**: One hand-maintained OpenAPI 3 JSON file in the repository at
  `schema/openapi/v5/v5/v5.swagger.json`. It describes only the six V5
  endpoints that have no V6 equivalent: `POST /query/topXdata`,
  `POST /query/topXchart`, `POST /query/url`, `POST /batch/tags`,
  `POST /batch/customdimensions/{dimensionName}/populators`, and
  `GET /batch/{guid}/status`. The paths are relative to the V5 base URL
  (`https://api.kentik.com/api/v5`), so they carry no `/api/v5` prefix. The
  operations use two tags, `QueryService` and `BatchService`.
- **Rationale**:
  - The generator expects OpenAPI 3 (`components/schemas`,
    `scripts/generate_sdk.py` lines 586 to 594), not Swagger 2.
  - `parity._swagger_file_metadata()` needs at least three path parts below
    the base: `<service>/<version>/<file>`. `v5/v5/v5.swagger.json` gives
    service `v5` and version `v5`.
  - Wrapper generation keeps only REST modules whose name ends in `Service`,
    and it names a module after the first tag of its operations
    (`wrapper_generation.py` lines 320 to 332). Two tags give two REST modules
    under one wrapper, as `alerting` already does.
  - Relative paths make the public name keys short and version-free:
    `POST /query/topXdata`.
- **Alternatives considered**:
  - Swagger 2: rejected, the transforms read `components/schemas`.
  - A hand-written client: rejected by Principles I and II and by FR-007.
  - Paths with `/api/v5` and a host-only base URL: rejected. Spec FR-006a sets
    the base URL to include `/api/v5`, and the docs give it in that form.

## R2. How the generator reads the local schema base

- **Decision**: `generate_modular_sdk()` reads two OpenAPI bases: the upstream
  `<schema_root>/gen/openapiv3/kentik` and the local schema base
  `PROJECT_ROOT/schema/openapi`. `parity.select_latest_swagger_files_by_service()`
  runs on each base. The source service set, the parity check, the
  public-name resolution, and the per-file generation loop all use the union.
  A service name that appears in both bases fails the run with
  `RuntimeError`. The generator records the services that came from the local
  base and passes that set to `wrapper_generation.generate()` and to
  `api_surface`.
- **Rationale**:
  - Without the union, the parity check fails with "Extra generated
    directories: v5" (`parity.py` lines 154 to 176), and `public_names` raises
    `NameDriftError` because `v5` is not in the candidates
    (`public_names.py` lines 65 to 75).
  - The local schema base has no `proto/` directory. The proto lookup already skips a
    missing directory ("No proto directory found, skipping gRPC.",
    `generate_sdk.py` line 1005), and `_discover_grpc_methods()` returns
    nothing. So no gRPC code is made, and nothing crashes.
  - `validate_schema_files_or_raise()` must also run on the local file, so a
    broken edit fails before `gen/` is touched.
- **Alternatives considered**:
  - Copy the local file into the upstream checkout at run time: rejected. It
    hides the source of the file and breaks `make generate local` on a clean
    sibling checkout.
  - A CLI flag for extra schema bases: rejected for now. One fixed local
    schema base is
    enough, and a flag adds a second way to get a different SDK.

## R3. The V5 host, and how V5 calls avoid gRPC

- **Decision**: `KentikAPI` builds a second `APIConfig` for V5 and a second
  `RestTransport` (`self._v5_transport`) on it, for every `protocol`. The V5
  base URL comes from the region (`us`: `https://api.kentik.com/api/v5`, `eu`:
  `https://api.kentik.eu/api/v5`) or from a new keyword argument,
  `v5_base_url`. The generated mixin mounts every service from the local
  schema base on
  `self._v5_transport` instead of `self._transport`. `KentikAPI` gets a
  `v5_api_config` property, and `close()` closes both transports.
- **Rationale**:
  - `request_json()` sends a relative path through the `httpx.Client` of its
    `APIConfig`, whose `base_url` is the V6 host (`api_config.py` lines 255 to
    261). A V5 call needs an `APIConfig` with the V5 host.
  - The host change is built in one hand-written place, in the open, from the
    region or from an explicit argument. This follows the rule in CLAUDE.md
    that a credential redirect stays visible at its call site.
  - The `v5` wrapper always gets a `RestTransport`, so its REST branch always
    runs. That meets FR-005 for gRPC clients, with no fallback logic in a
    wrapper.
  - httpx joins a base URL that has a path with a relative request path
    (`https://api.kentik.com/api/v5` plus `/query/topXdata`), so the path
    stays relative. A unit test pins this.
- **Alternatives considered**:
  - Route on the path prefix inside `request_json()`: rejected. It hides the
    host choice inside the shared runtime.
  - Rewrite the V6 URL (remove `grpc.`, add `/api/v5`): rejected in the
    clarification session.
  - Absolute URLs in the description file: rejected, they fix the region.

## R4. Unknown enum values

- **Decision**: The V5 description declares no `enum` keyword. Fields such as
  `metric`, `viz_type`, `fastData`, `direction`, and `imageType` are plain
  `string` fields, and their descriptions list the known values.
- **Rationale**: The generator renders `enum` as `class X(str, Enum)`, and an
  unknown value fails validation and raises `HTTPException(502)`
  (`rest_runtime.py` lines 98 to 128). A plain string meets FR-010 with no
  template change. Permissive enums for all services stay a separate item in
  the audit follow-up list.
- **Alternatives considered**: An enum template with a `_missing_` hook:
  rejected here. It changes every service and needs its own spec.

## R5. Result rows with columns that the request did not predict

- **Decision**: A result row in the description is
  `{"type": "object", "additionalProperties": true}`, so it becomes
  `Dict[str, Any]`. The row keys depend on the dimensions and metrics of the
  query (the live check returned `i_protocol_name`, `key`,
  `avg_bits_per_sec`, `p95th_bits_per_sec`, `max_bits_per_sec`, and
  `timeSeries`).
- **Rationale**: FR-003. The row shape is not fixed, so a fixed model would
  drop columns.
- **Checked 2026-10-16 (T001)**: `openapi-python-generator` 2.1.2 renders
  an item schema with `additionalProperties: true` as `List[Dict[str, Any]]`,
  and the template keeps it. No change was needed.

### R5a. Request models that keep unknown fields

- **Decision**: `Query`, `QueryItem`, and `BatchCriterion` declare
  `additionalProperties: true`. The model template adds `"extra": "allow"`
  to `model_config` when a schema sets `additionalProperties` to the literal
  `true`, so the model keeps unknown fields and sends them back. The
  description types only the fields that the Kentik documentation lists.
- **Rationale**: The V5 SDK `Query` has about 40 more fields, most of them
  portal display options (`generatorPanelMinHeight`, `cutFnRegex`). Users
  copy query JSON from Data Explorer ("Show API Call"), which carries them.
  Passing them through keeps V5 behavior without a large, fragile model
  (FR-002). The template keeps Pydantic's default (drop unknown fields) for
  every other schema. Upstream V6 schemas use `additionalProperties` only
  with a type, for maps, so V6 output does not change. A generator test
  pins that.
- **Alternatives considered**: Type all 40 fields by hand: rejected. It
  copies undocumented portal internals into a public model.
- **Checked 2026-10-16 (T001, T003)**: without a change, the generated model
  dropped unknown fields. The template now adds `"extra": "allow"` for
  `additionalProperties: true` only. `tests/generator/test_openapi_templates.py`
  pins both cases, and `make generate local` gave no diff in upstream
  services.

## R6. A response body that is a JSON string (`query/url`)

- **Decision**: The `url` response schema is `{"type": "string"}`. The wrapper
  returns `str`.
- **Rationale**: The live check returned a JSON string with a portal link. It
  is the API's real shape.
- **Checked 2026-10-16 (T001)**: for a `string` success schema, the
  generated function is typed `-> str` and returns the parsed body as is,
  without `parse_response_model()`. The 202 status is passed through as
  `expected_status=202`. No change was needed.

## R7. Chart decoding

- **Decision**: The generated chart call returns a model with `dataUri: str`.
  A hand-written helper, `kentik_api.v5_tools.decode_chart(response)`, returns
  `ChartImage(image_type: str, data: bytes)`. A data URI that is not valid
  raises `HTTPException` with status 502 and a clear message, as every other
  unusable response does.
- **Rationale**: The generator makes models from the wire shape. Decoding is a
  small pure function and not connection code, so it does not touch
  Principle II.
- **Alternatives considered**: Decode inside a model validator in the
  template: rejected, it adds a special case to the generic template.

## R8. Batch helpers

- **Decision**: `kentik_api.v5_tools` has three batch helpers:
  - `split_batch(upserts, deletes, *, replace_all, max_bytes=4_000_000)`
    returns a list of `BatchPart` models. Only the last part has
    `complete=True`. A part never exceeds `max_bytes` when serialized.
  - `send_batch(send, parts)` calls `send(part)` for each part, copies the
    `guid` of the first response into the later parts, and returns the
    `guid`. If a part fails, it raises `BatchSendError` with the parts sent
    and the `guid`. It never resends.
  - `wait_for_batch(client, guid, *, timeout, interval)` polls
    `client.v5.batch_status` until `is_complete` is true, or raises
    `BatchWaitTimeout` with the last status.
- **Rationale**: The Knowledge Base sets a 4 MB limit for each part and says
  that each part after the first carries the `guid`. Splitting by size, not
  by item count, follows that limit. The helpers call the generated wrapper,
  so every request still goes through `request_json()`.
- **Alternatives considered**: An item-count split (V5 SDK style): rejected,
  the API limit is in bytes.

## R9. End-to-end tests for read-only POST calls

- **Decision**: A hand-written `tests/e2e/test_v5_query_e2e.py` (marker
  `e2e`) runs `top_x_data` and `query_url` against the real API, and runs
  `top_x_chart` as `xfail(raises=TransportError, strict=False)` with a short
  timeout. The query uses the first device name from `device.list_devices`.
  `GET /batch/{guid}/status` is a GET, so the auto-discovered read suite
  covers it. A 404 for an unknown ID counts as an answer.
- **Rationale**: The e2e suites split cases by verb only, so a POST lands in
  the skipped mutating set (`test_endpoints_e2e.py` lines 51 to 53).
  `test_alert_list_e2e.py` already covers a read-only POST in this way.
- **Alternatives considered**: A read-only flag in the description file:
  rejected for now. Two calls do not justify a new mechanism.

## R10. Tests that assume every mounted service has gRPC

- **Decision**: `api_surface` records `"rest_only": true` for services from
  the local schema base. `SCHEMA_VERSION` goes from 7 to 8, and older records read as
  `rest_only: false`. `tests/generated/test_grpc_stub_wiring.py` skips
  `rest_only` services. A new test asserts that a `rest_only` wrapper works on
  a client built with `protocol="grpc"`.
- **Rationale**: `test_grpc_stub_wiring.py` lines 61 to 74 require a gRPC stub
  on every mounted wrapper, which `v5` cannot have. The flag also lets docs
  and release notes name these calls REST-only.

## R11. The analytics extra

- **Decision**: The extra is `kentik-api[analytics]`, with `pandas>=2.3`,
  `pyarrow>=21`, and `pyyaml>=6.0.2`. The package is `kentik_api.analytics`
  (`definitions`, `cache`, `flatness`). The cache stores Parquet files through
  pyarrow. Definitions load with `yaml.safe_load`. A `@fixup:` mapping and a
  SQL definition each fail with a clear error.
- **Rationale**: Parquet and `safe_load` cannot run code on read (FR-018,
  FR-019). pyarrow is the pandas default Parquet engine. fastparquet, which V5
  used, is not needed.
- **Alternatives considered**: Pickle or `yaml.load`: rejected, both can run
  code (SC-005).

## R12. Device lookup

- **Decision**: `kentik_api.devices.DeviceLookup` is in the base install,
  because it needs no pandas. It loads devices and interfaces once through the
  V6 `device` and `interface` services, finds them by ID or by name, builds
  `device:interface` link names, and returns link speeds. `save()` and
  `load()` use JSON.
- **Rationale**: FR-021 and FR-010a. The data comes from V6, so no V5 endpoint
  is added. JSON cannot run code (SC-005).

## R13. Public names

- **Decision**: The service is `v5`. The planned method names are
  `top_x_data`, `top_x_chart`, `query_url`, `batch_tags`, `batch_populators`,
  and `batch_status`. The operationIds are chosen so that
  `_wrapper_method_names()` gives these names. If the rule gives other names,
  the first run's entries in `public_names.json` are set to these names before
  the commit.
- **Rationale**: Public names are frozen on the first commit, so they are set
  once, on purpose.

## R14. Quota on V5 calls

- **Decision**: No runtime change. V5 sends no `X-RateLimit-*` headers, so the
  `RateLimit` on results and errors has empty fields. The rate limiting guide
  says so, and gives a 429 retry recipe with a fixed backoff that does not
  depend on quota headers.
- **Checked 2026-10-16 (T002)**: with no quota headers, `RateLimit.from_headers()`
  returns `None`. The result, the error, and `api_config.rate_limits` hold no
  quota. `tests/runtime/test_rest_runtime.py` pins it.

## R15. Generated documentation for a REST-only service

- **Decision**: `endpoint_docs` reads the `rest_only` set. For those services,
  the example text says "REST only. A client created with protocol=\"grpc\"
  also sends these calls over REST", instead of "Both transports work"
  (`endpoint_docs.py` line 394). `docs_rendering` lists `v5` as REST-only in
  the architecture page and states the local schema source in the `gen/`
  README.

## R16. Generation drift in CI

- **Decision**: No change. The drift job regenerates from the checkout, which
  contains `schema/openapi/`, so a change to the V5 description without
  regenerated output fails the job, as an upstream change does. `schema.lock`
  pins only the upstream commit.
