<!-- HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly. -->

# AGENTS.md

Guidance for coding agents that work in this repository. Claude Code reads it
through the one-line `@AGENTS.md` import in [`CLAUDE.md`](CLAUDE.md). Edit this file, never
`CLAUDE.md`.

## What this project is

`kentik-api` is the Kentik Community Python SDK: a
type-safe client for the Kentik API v6, built on Pydantic v2 and
HTTPX. This SDK is not hand-written. [`scripts/generate_sdk.py`](scripts/generate_sdk.py)
generates it end-to-end from Kentik's public OpenAPI v3 schema
([`kentik/api-schema-public`](https://github.com/kentik/api-schema-public)), plus the local schema base
[`schema/openapi/`](schema/openapi/) (see "The local schema base" below). It orchestrates the phase modules in
[`scripts/generation/`](scripts/generation/README.md) (see "The generator's phase modules" below).
This project uses `uv` to manage the environment and dependencies
(lockfile [`uv.lock`](uv.lock)). The build backend is `hatchling` with
`hatch-vcs` for dynamic versioning from git tags.

## Architecture: hand-written vs. generated

This split is the single most important thing to respect in this
repo.

These files are hand-written. Every regeneration keeps them:

- [`src/kentik_api/client.py`](src/kentik_api/client.py): `KentikAPI`, the main entrypoint
- [`src/kentik_api/auth/`](src/kentik_api/auth/README.md): credentials
- [`src/kentik_api/core/`](src/kentik_api/core/README.md): `api_config.py`, `rest_runtime.py`,
  `grpc_runtime.py` (shared runtime logic)
- [`src/kentik_api/errors/`](src/kentik_api/errors/README.md): base exception types
- [`src/kentik_api/transports/`](src/kentik_api/transports/README.md): REST/gRPC transport base classes
- [`scripts/openapi_templates/`](scripts/openapi_templates/): custom Jinja2 templates fed into
  the generator
- `scripts/generation/`: the generator's phase modules
  (`parity.py`, `error_package.py`, `fixup.py`,
  `wrapper_generation.py`, `docs_rendering.py`, `endpoint_docs.py`,
  `api_surface.py`, `public_names.py`, `explorer_docs.py`, `_shared.py`),
  orchestrated by `scripts/generate_sdk.py`, plus `diagram_kit.py` and
  `diagram_assets/`, a copy of the diagrams skill's kit
- [`public_names.json`](public_names.json): the public name of every Service, client
  method, and model. You edit it by hand. A run only adds entries (see
  "Public names" below)
- `schema/openapi/`: the local schema base. Hand-maintained OpenAPI
  descriptions of endpoints that upstream does not publish. Today only
  `v5/v5/v5.swagger.json`, the V5 query and batch endpoints. It is a
  generator input, like the upstream schema
- [`src/kentik_api/v5_tools.py`](src/kentik_api/v5_tools.py), [`src/kentik_api/devices.py`](src/kentik_api/devices.py), and
  [`src/kentik_api/analytics/`](src/kentik_api/analytics/) (the `analytics` extra): helpers on top
  of generated operations. They never send HTTP themselves:
  [`tests/smoke/test_helpers_no_direct_http.py`](tests/smoke/test_helpers_no_direct_http.py) checks that they import
  neither `httpx` nor `request_json`

These files are fully generated. Every `uv run poe generate` run wipes and rebuilds them:

- [`src/kentik_api/client_mixin.py`](src/kentik_api/client_mixin.py): mounts every generated service
  wrapper onto the client
- `src/kentik_api/gen/<service>/`: one directory per API service,
  each with `models/`, `services/` (raw REST functions + a unified
  `<Service>ServiceWrapper`), `error/`, `pb/` (gRPC stubs), and a
  `README.md`
- [`src/kentik_api/gen/README.md`](src/kentik_api/gen/README.md): the `gen/` root README
- [`docs/sphinx/sdk_runtime_architecture.md`](docs/sphinx/sdk_runtime_architecture.md): the runtime
  architecture page, with a Mermaid call path and an interactive dependency explorer
- `docs/sphinx/_static/explorer.css`, `explorer.js`, and `sequence-steps.js`: the explorer
  assets and the step-through controls of every Mermaid sequence diagram, written by
  `explorer_docs.write_static_assets()` from `scripts/generation/diagram_assets/`
- `docs/sphinx/services/<service>.md`, `index.md`, and `README.md`:
  one reference page per service and the two index pages, written by
  `endpoint_docs.EndpointDocsCollector.render()`
- [`schema_operations.json`](schema_operations.json): each service's operations as the patched
  swagger declares them, written by
  `EndpointDocsCollector.write_record()`
- [`api_surface.json`](api_surface.json): the public API surface, written by
  `api_surface.generate()` at the end of each run
- the `<!-- kentik-gen:... -->` marker blocks inside
  `docs/sphinx/guides/{quickstart,rest,grpc,generation,rest-vs-grpc}.md` and
  [`docs/sphinx/README.md`](docs/sphinx/README.md), rewritten by
  `docs_rendering._update_guide_snippets()`. The surrounding prose in
  those files is hand-written. The generator writes only the marker blocks.

> [!WARNING]
> Never hand-edit generated files. If output is wrong, fix
> the generator, a phase module in `scripts/generation/`, or a
> template in `scripts/openapi_templates/`. Then regenerate. A parity
> check (`parity.validate_generated_service_parity()`) fails the whole
> generation run when generated service directories do not exactly
> match the schema's service directories. Partial or manual patches
> do not survive this check.

gRPC transport is fully implemented, not a stub. Every generated
wrapper method routes a `GrpcTransport` call through `call_grpc()`
when an RPC shares that REST operation's HTTP rule: the same proto
service (the REST module's name), HTTP verb, and path. Matching by
RPC name alone is wrong, because `alerting` declares `Delete` on
several proto services. The generator reads each RPC's rule from the
descriptor protoc serialized into its `_pb2.py`. The bridge runs
`build_grpc_request()` (in `core/grpc_runtime.py`) → `call_grpc()` →
`parse_grpc_response()` (`MessageToDict`, then REST's own
`parse_response_model()`) against proto companions
compiled into `gen/pb_companions/`. `build_grpc_request()` transcodes
the way grpc-gateway does: each URL placeholder sets the field its
HTTP rule names at that position (GetDevice's `deviceid` sets `id`),
and each query parameter sets the dotted field path of its wire name
(`querynoCustomColumns` sets `query.no_custom_columns`). A path or
query argument that resolves to no field fails generation or raises
`ParseError`, never drops silently. A wrapper method raises
`NotImplementedError` for `GrpcTransport` in exactly two cases: the
service's proto companions failed to import at wrapper `__init__`
time ("gRPC proto modules for `<service>` service failed to import:
`<cause>`", chained from the import error), or no RPC shares that REST operation's HTTP rule
("gRPC translation for `<Operation>` is not yet
implemented"). Both REST and gRPC return identical Pydantic models
for every operation gRPC covers, and raise the same exception type
for the same failure. Every gRPC call carries a deadline:
`GrpcTransport`'s channel interceptor applies `APIConfig.grpc_deadline`
unless the call passes its own, so generated call sites never need one.
The services in `_NO_SERVER_DEADLINE` are the one exception (see "Upstream
workarounds").

### The generator's phase modules

`scripts/generate_sdk.py` is the entrypoint: CLI parsing
(`--local-repo`, `--schema-ref`) and the top-level orchestration loop in
`generate_modular_sdk()`. It calls out to `scripts/generation/`, a
subpackage of independently testable phase modules (see
[`tests/generator/`](tests/generator/README.md)):

- `parity.py`: swagger file selection (latest version per service,
  namespace, and filename), joining the local schema base to upstream
  (`merge_local_schema_base()`, which fails on a service in both),
  dropping a file whose REST modules newer
  files in its service all write (an upstream rename), and the
  directory parity check between
  generated output and the schema. Fully independent of the other
  phase modules.
- `error_package.py`: per-service error class generation
  (`generate_service_error_package()`) and the error-dispatch
  injection (`inject_service_error_handling()`, see the
  guarded-coupling note below). It runs after fixup, because each
  operation's error classes are named after its client method
  (`label.list` raises `ListError`), not its operationId.
- `fixup.py`: generated-code post-processing, called once per
  service directory after the schema availability window closes.
  Single public entrypoint: `fix_generated_service(service_dir)`.
  Internally: rebuilds `models/__init__.py` from a full directory
  scan, replaces wildcard exports with explicit named imports, and
  applies all file-level content patches (import aliases, path
  parameter sanitization, docstring normalization, and
  duplicate function renaming).
- `wrapper_generation.py`: generates service wrappers and the
  client mixin, collapsed into a single `generate()` entrypoint
  (wrappers first, then the mixin that imports them).
- `docs_rendering.py`: generates the runtime architecture page with
  an inline Mermaid dependency graph, writes the `gen/` root README,
  and writes per-service READMEs, collapsed into a single
  `generate()` entrypoint.
- `endpoint_docs.py`: exposes `EndpointDocsCollector`, not a plain
  function. `collector.extract(service, swagger_path)` must run once
  per swagger file, while the file is still available, during
  `generate_modular_sdk()`'s schema-availability window.
  `collector.render()` must run afterward, and only after
  `wrapper_generation.generate()` runs. `render()` builds Sphinx
  MyST stubs whose example snippets statically read the real
  generated wrapper method signatures off disk.
  `collector.write_record()` writes `schema_operations.json` after
  `render()`. The collector does not enforce this order.
  `generate_modular_sdk()` calls the methods in the correct order.
- `api_surface.py`: records the public API surface into
  `api_surface.json` on every run, and diffs two recordings. `uv run poe
  release-notes`, `uv run poe check-changelog`, and the end-of-run
  `API SURFACE CHANGED` alert all read it.
- `public_names.py`: reads `public_names.json`, adds an entry for
  each new Service, operation, and model, and raises `NameDriftError`
  when an entry no longer matches the schema. See "Public names".
- `_shared.py`: `PROJECT_ROOT`, `SDK_OUTPUT_DIR`,
  `REGENERATE_COMMAND` (the command every generated header names), and the helpers
  that more than one phase module genuinely uses:
  `iter_service_dirs()` and `INTERNAL_GEN_DIRS` (the single answer to
  "is this directory a Service"), `discover_service_model_classes`,
  `service_to_pascal_case`, `normalize_symbol` (the REST generator's
  own naming rule), `write_text_lf` (every generator write, so output
  has LF on Windows too), `mermaid_init()` (the house
  theme of every generated Mermaid diagram), and the generated-source parsers
  `parse_generated_rest_module` / `RestOperation`,
  `parse_wrapper_methods` / `WrapperMethod`, and `grpc_call` /
  `grpc_stub_services` / `GrpcCall`. Keep this list in step
  with [`scripts/generation/README.md`](scripts/generation/README.md).
  Everything else stays local to the one phase module (or
  `generate_sdk.py` itself) that calls it. Resist the urge to move a
  single-consumer helper here "for consistency."

`scripts/generate_sdk.py` runs as a script: `uv run python
scripts/generate_sdk.py`. This puts `scripts/` on `sys.path` at
runtime. `generate_sdk.py` then imports the subpackage as `from
generation import ...`. Tests import the same modules as `from
scripts.generation import ...`. `pythonpath = ["."]` in
`pyproject.toml`, plus `scripts/__init__.py`, puts the repo root on
`sys.path` for tests. Both import styles work because every
intra-subpackage import inside `scripts/generation/*.py` is relative
(`from ._shared import ...`). A relative import resolves correctly
under either top-level name. Never switch those relative imports to
absolute `scripts.generation.*` imports. That change breaks the
script's own direct-execution import path.

## The shared connection handler: protect this, do not undo it

The shared REST runtime is the single most significant piece of
hand-written engineering in this repo. It routes every generated
endpoint, across all 37 mounted services, through one connection path
instead of generating or hand-writing bespoke per-endpoint HTTP
code. This is not just a convention. It is structural. The source
code shows it directly:

- [`src/kentik_api/core/rest_runtime.py`](src/kentik_api/core/rest_runtime.py): `request_json()` is the
  only function that ever calls `httpx` for REST traffic. Every
  generated operation in every service calls this same function. It
  centralizes:
  - Kentik's auth headers (`X-CH-Auth-Email` /
    `X-CH-Auth-API-Token`), built by `auth_headers()` in
    [`src/kentik_api/auth/credentials.py`](src/kentik_api/auth/credentials.py), the scheme's one definition,
    which the gRPC auth plugin also derives from
  - the credentials check, before anything is sent
  - query-param cleaning
  - the request itself, over the one `httpx.Client` its `APIConfig`
    owns (one pooled connection per client, timeout passed per request)
  - transport-failure wrapping (`TransportError`); its
    `may_have_reached_server` is false only for REST connection or pool failures
    known to occur before send, and true otherwise
  - quota capture into `RateLimit`, on the result and on every error
  - a 401 raised as `AuthenticationError`, ahead of the generated
    error class, so generated error packages never see one
  - status-code checking
  - JSON error-body parsing
  - dispatch into per-operation error classes via
    `error_cls.from_response`
- [`src/kentik_api/core/grpc_runtime.py`](src/kentik_api/core/grpc_runtime.py): `call_grpc()` is the gRPC
  analogue of `request_json()`. It routes every generated gRPC wrapper
  call through one place, applies a per-call deadline override, and
  returns `(response, rate_limit)`. `map_grpc_error()` is extracted as
  a pure function (no I/O, no side effects) that classifies every
  non-OK `grpc.RpcError` status as `AuthenticationError`,
  `HTTPException`, or `TransportError`. Testable without a gRPC
  channel.
- [`src/kentik_api/core/api_config.py`](src/kentik_api/core/api_config.py): `APIConfig` is the one
  shared config object (base URL, auth email/token, TLS verify,
  timeouts, the shared HTTP client, per-endpoint quota) used in every
  call. A wrapper's `api_config_override` replaces it for one call,
  never merges with it, so an override that changes the host cannot
  inherit credentials. `with_timeout()` is the only derivation helper,
  and it can change timeouts only. Changing the host, credentials, or
  `verify` takes an explicit `APIConfig(...)`, which keeps any
  credential redirect visible at its call site.
- [`src/kentik_api/errors/__init__.py`](src/kentik_api/errors/__init__.py): one shared exception
  hierarchy (`KentikError` → `ConfigurationError`,
  `AuthenticationError`, `TransportError`, `HTTPException`) that
  every service's generated per-operation error classes build on.
- `src/kentik_api/transports/{base,rest_client,grpc_client}.py`:
  thin transport-selection code, not
  per-endpoint logic.

`KentikAPI` has a second `RestTransport`, `_v5_transport`, on its own
`APIConfig` for the V5 host (from `region`, or `v5_base_url`, which must
be https). It exists on every client, gRPC ones included. The generated
mixin mounts every service from the local schema base on it, so those
calls still go through `request_json()`, only with another base URL.
`client.v5_api_config` is its config. V5 responses carry no quota
headers, so V5 calls report no quota.

This design took several dedicated changes to get right: error
handling inside `request_json` (`TransportError`, `_raise_http_error`),
`.env`-based auth, and [`scripts/sample_consume_sdk.py`](scripts/sample_consume_sdk.py), which proves
the whole path end-to-end against both a mocked and a real API call.

> [!WARNING]
> Never regress this pattern. Do not generate, hand-write, or
> suggest per-endpoint connection, auth, or retry code. Do not
> "simplify" by inlining request logic into individual service
> wrappers. Instead, fix or extend `request_json` or `APIConfig`:
> every endpoint in every service shares them.

### Why this survives `uv run poe generate` / `scripts/generate_sdk.py`

To make sure of this, read `generate_modular_sdk()`. Its
cleanup step only iterates `SDK_OUTPUT_DIR` (`src/kentik_api/gen/`)
and removes subdirectories there. It never touches `core/`,
`errors/`, `transports/`, `auth/`, or `client.py`, because the wipe
loop never walks those paths. These files survive regeneration
structurally, not just by convention or discipline.

### Two files that look hand-written but are fully regenerated: never hand-edit

- [`src/kentik_api/client_mixin.py`](src/kentik_api/client_mixin.py) lives outside `gen/`, but
  `wrapper_generation.generate()` calls `mixin_file.write_text(...)`,
  a full overwrite, on every run. The next `uv run poe generate` silently
  overwrites any manual edits here.
- [`docs/sphinx/sdk_runtime_architecture.md`](docs/sphinx/sdk_runtime_architecture.md) and
  [`src/kentik_api/gen/README.md`](src/kentik_api/gen/README.md): `docs_rendering.generate()`
  fully rewrites these every run. The architecture page embeds its
  dependency graph as an inline Mermaid fence, so there are no
  separate diagram artifacts to track. By contrast,
  [`docs/sphinx/index.md`](docs/sphinx/index.md) is genuinely hand-written. The generator
  only inserts a toctree line into it if missing: a
  non-destructive append, not an overwrite.

### Guarded couplings worth knowing about

`error_package.inject_service_error_handling()` wires each freshly
generated per-service REST module to its error classes. It points each
function's `error_cls=` at the class named after its client method, and
replaces the `# __ERROR_IMPORTS_PLACEHOLDER__` sentinel that
[`scripts/openapi_templates/service.jinja2`](scripts/openapi_templates/service.jinja2) emits with a
`from ..error import ...` line. For a file without the sentinel, it
falls back to inserting that line after
`from kentik_api.core.rest_runtime import request_json`. With neither
anchor present, it raises `ValueError` (when there are operations to
inject) rather than silently skipping.

`fixup._fix_path_parameters()` matches that same `request_json`
import line to add the `path_segment` import next to it, and raises
`ValueError` when the line is missing. Rename or move `request_json`
only together with both functions and the template.

### Upstream workarounds

Each workaround below fixes an upstream API bug in the SDK. Each has
a live canary in [`tests/e2e/test_upstream_workarounds_e2e.py`](tests/e2e/test_upstream_workarounds_e2e.py): a strict
xfail that sends the documented request. When upstream fixes the bug, the
canary fails with `XPASS(strict)` in `uv run poe test-e2e-mutating`. Then
remove the workaround, regenerate, delete the canary, and update this list
and [`CHANGELOG.md`](CHANGELOG.md).

- REST body key for a URL that sets a nested field. The REST API drops a
  camelCase body key (`asGroup`) when the URL template sets a field inside it
  (`{as_group.id}`) and the rule has `body: "*"`. Confirmed on
  `UpdateASGroup` and `UpdateSiteMarket`. `send_proto_body_keys()` in
  [`scripts/generation/wrapper_generation.py`](scripts/generation/wrapper_generation.py), called from
  `_patch_generated_code()` in `generate_sdk.py`, makes those REST functions
  send the proto name (`as_group`). It applies to every rule with that shape,
  and the run prints the list. [`tests/generated/test_proto_body_keys.py`](tests/generated/test_proto_body_keys.py)
  pins the keys sent.
- gRPC deadline on six services. The gRPC server fails every call that
  carries a deadline (`internal error (name:RangeError ...)`) on `alerting`,
  `audit`, `custom_application`, `custom_dimension`, `plan`, and
  `saved_filter`. `_NO_SERVER_DEADLINE` in [`transports/grpc_client.py`](src/kentik_api/transports/grpc_client.py)
  lists them, by the service segment of the method path. For those, the
  interceptor sends no deadline and cancels the call at the deadline, and
  `call_grpc()` reports the cancel as `TransportError` `DEADLINE_EXCEEDED`.
  The cancel works only on a `future()` call, which is why `call_grpc()`
  uses `future()`. One canary per service. [`tests/runtime/test_grpc_transport.py`](tests/runtime/test_grpc_transport.py)
  pins the behavior against a local server.

## Public names

`public_names.json` is the one place that sets the public name of
every Service (`client.<service>`, `kentik_api.gen.<service>`), client
method, and model. Each entry maps a public name to a version-free
upstream value: the schema directory, `VERB /path` with `<version>`
and `{}`, or the schema model name with `<version>`. The generator
only adds entries. It never changes one. Its naming rules
(`_wrapper_method_names()`, `default_model_name()`) give only the
first name of a new thing.

- When upstream renames or moves something, the run fails with
  `NameDriftError` before it touches `gen/`. Fix it by changing the
  entry's value in `public_names.json`, never by changing a naming rule
  or hand-editing generated code.
- Changing a naming rule does not rename anything that already has an
  entry. To rename a public name, change its key and record the
  breaking change in `CHANGELOG.md`.
- Error class names follow the client method name, so the file names
  them too. Parameter names, model fields, and enum values still come
  from the schema.
- Commit `public_names.json` with every regeneration that adds
  entries, or CI's drift check fails.

### The local schema base

`schema/openapi/<service>/<version>/<file>.swagger.json` holds
hand-maintained OpenAPI 3 descriptions of endpoints that upstream does
not publish (constitution 1.4.2). Today that is `v5`: the V5 query and
batch endpoints, which have no V6 equivalent. Rules:

- Add an endpoint here only when no V6 endpoint does the same thing.
  [`tests/generator/test_v5_description.py`](tests/generator/test_v5_description.py) pins the six V5 operations.
- A service in both upstream and the local base fails the run. When
  upstream publishes the service, remove it here.
- Every service from the local base is REST-only: no protos, no `pb/`,
  `"rest_only": true` in `api_surface.json`, and mounted on
  `_v5_transport`. The gRPC stub test skips it by that flag.
- Declare no `enum`, so an unknown value never fails a call. A schema
  with `additionalProperties: true` gives a model that keeps unknown
  fields (`"extra": "allow"`).
- Change the description, then run `uv run poe generate --local`. Never edit
  `gen/v5/`.

### Services without a wrapper: out of scope, on purpose

REST paths in the OpenAPI schema drive wrapper generation. A
Service whose schema declares no paths gets models and proto stubs but
no wrapper, so it is not mounted on the client. Six Services are in
that state, and the split matters:

- `core`, `monitoring`, `net` genuinely declare no RPCs. Shared types
  only. Correct as is.
- `deviceconf` (10 RPCs), `kptr` (4), and `diagnostic` (2) declare real
  gRPC RPCs upstream, but none carry a `google.api.http` annotation, so
  `protoc-gen-openapiv2` emits no paths for them.

REST paths are this SDK's contract. Proto-driven wrapper generation
is deliberately out of scope: it needs a second generation path
alongside the swagger one, including proto-derived request and response
models, for 16 RPCs. The gap is an upstream schema gap, and it closes
here automatically if upstream adds those annotations. Do not "fix" it by
hand-editing `client_mixin.py`, which every run fully overwrites.

Note this is not the same question as service visibility. `kptr` is
annotated `SERVICE_VISIBILITY_PUBLIC` upstream, while `ktbgp` and
`vault`, which the SDK does mount, are annotated
`SERVICE_VISIBILITY_PRIVATE`. That annotation never reaches the swagger,
so no generator can act on it today.

## Generation pipeline

- `uv run poe generate` fetches
  `https://github.com/kentik/api-schema-public.git` at the commit
  pinned in [`schema.lock`](schema.lock). `uv run poe sync-schema` fetches schema HEAD
  instead. `uv run poe generate --schema-ref <ref>` fetches any other ref.
  `uv run poe generate --local` reads the sibling checkout
  `../api-schema-public/` instead, and fails if it is absent. There
  is no automatic fallback between the two.
- Every completed run writes the schema commit it used to
  `schema.lock`, so commit that file with the regenerated tree. A
  local checkout with uncommitted changes to tracked files leaves the
  pin unchanged. The scheduled `schema-sync` workflow runs
  `uv run poe sync-schema` weekly and opens a pull request when the output
  changes. It needs the repository setting that allows GitHub Actions to
  create pull requests, and each of its pull requests needs a close and
  reopen to start CI (see "Automated update pull requests" in
  [`docs/sphinx/guides/generation.md`](docs/sphinx/guides/generation.md)).
- A run that fails or is interrupted puts every generated output back
  as it was (`restored_on_failure()` around `generate_modular_sdk()`).
  Only a hard kill can leave a half-built tree. `git checkout` fixes it.
- The generator uses only the newest version per swagger family (see
  [CONTEXT.md](CONTEXT.md)) when multiple versioned swagger files exist.
- See [`docs/sphinx/local_generation_workflow.md`](docs/sphinx/local_generation_workflow.md) for full details,
  including how to test a forked `openapi-python-generator` via env
  vars without editing code.
- See [`docs/sphinx/sdk_runtime_architecture.md`](docs/sphinx/sdk_runtime_architecture.md) for the runtime
  architecture: the module dependency graph and the
  generated-vs-hand-written boundary.

### Per-service API docs: real MyST text, not rendered diagram images

`endpoint_docs.EndpointDocsCollector.render()` generates
`docs/sphinx/services/<service>.md` as real Sphinx/MyST text, not
rendered diagram images. This is deliberate. A rendered "API table"
and model-class-diagram image become unreadable and uncopyable once
a service has more than a handful of operations or models. For
example, an image of `alerting`'s model diagram runs to 4329×1686px.

- Endpoints: one section per operation, with a parameter table,
  a response table, and an auto-generated Python usage example.
  `extract_endpoint_docs()` builds each section by parsing each
  swagger file's `paths` directly. `EndpointDocsCollector.extract(
  service, swagger_path)` accumulates these sections per service. It
  runs once per file, during the per-swagger-file loop, because
  schema files are only available inside the `with
  get_schema_root(...)` block. Swagger files with zero operations
  correctly contribute no endpoint section at all. This is common in
  multi-file services: `alerting` merges 20 files, and 12 of them
  have none.
- Data models: `sphinxcontrib.autodoc_pydantic`
  (`autopydantic_model`) renders every model as a real field table
  and JSON schema, instead of a diagram. Enum classes (`class X(str,
  Enum)`) must use `autoclass` instead. Feeding an enum class into
  `autopydantic_model` crashes the whole Sphinx build
  (`AttributeError: ... __pydantic_decorators__`).
  `_autodoc_directive_for_model()` checks each class's base list
  first, to avoid this.
- The generator matches each example snippet to its endpoint by
  `(method, path)`, never by `operationId` alone. Multi-swagger-file
  services legitimately reuse generic operationIds across different
  underlying REST modules. For example, `alerting`'s `AlertService`,
  `SuppressionService`, and `MitigationsService` each declare an
  operation literally named `List`. Matching by operationId alone
  silently picks whichever wrapper method the generator parsed last.
  The result is a real-looking but wrong example (wrong method, wrong
  request model). Method and path together are unique per operation
  within a merged service. `parse_wrapper_method_signatures()` (in
  [`scripts/generation/endpoint_docs.py`](scripts/generation/endpoint_docs.py)) resolves this by statically
  reading the wrapper's import aliases. The generator itself never
  imports or executes generated code. That stays test-only by
  design (see [`tests/_discovery.py`](tests/_discovery.py)).

## Key commands

Every task lives in `[tool.poe.tasks]` in [`pyproject.toml`](pyproject.toml) and runs the same
on Windows, macOS, and Linux after `uv sync`. Run `uv run poe` to list them,
and `uv run poe -h <task>` to list a task's options. The poe agent skill is
in [`.claude/skills/poethepoet/`](.claude/skills/poethepoet/SKILL.md). After a poethepoet upgrade, run
`uv run poe _install_skill .claude/skills --upgrade` (a smoke test fails
until you do). A task must not set `envfile`: `.env` holds real credentials.

- `uv run poe all`: `generate`, then `test`. Docs are opt-in.
- `uv run poe generate`: regenerate SDK from the pinned schema commit on
  GitHub
- `uv run poe sync-schema`: regenerate from schema HEAD on GitHub and
  move the pin in `schema.lock`
- `uv run poe generate --local`: regenerate from the local
  `../api-schema-public/` checkout
- `uv run poe generate --local-repo /path/to/api-schema-public`:
  regenerate from an arbitrary local schema path
- `uv run poe generate --schema-ref <ref>`: regenerate from another ref
- `uv run poe docs`: regenerate from GitHub, then build Sphinx docs
  (`docs/sphinx` → `docs/build/html`) with warnings as errors. To build
  from the committed tree only, run `uv run poe docs-build`.
- `uv run poe release-notes` (`--since <ref>`, `--out <file>`): lists the API
  surface changes since a ref (default: the highest-versioned earlier release
  tag reachable from HEAD that has a surface record), field and enum level
  included. An unknown `--since` ref fails. `uv run poe check-changelog` fails
  when a breaking change in that list has no mention in `CHANGELOG.md`'s
  Unreleased section. CI runs it on every pull request against the merge base.
- `uv run poe impact-report` (`--since <ref>`, `--no-checks`, `--out <file>`):
  run by hand after a regeneration. [`scripts/impact_report.py`](scripts/impact_report.py) writes the
  facts of what changed (schema commit, files by kind, surface delta, floors,
  checks) to `reports/regeneration-impact-<date>.html`. It never overwrites an
  earlier report, and it leaves the Findings section to a person.
- `uv run poe test`: full pytest run (mocked layers only,
  never wires in `tests/e2e/`)
- `uv run poe test-generated` / `test-runtime` / `test-smoke` /
  `test-generator` / `test-analytics`: one mocked test layer at a time
- `uv run poe test-e2e` / `test-e2e-grpc` (required addition, see
  Testing strategy): opt-in end-to-end suites against the real
  Kentik API, REST and gRPC transports respectively. Must never
  appear in `test` or `all`. Both pass `--run-live-e2e`, without which
  [`tests/e2e/conftest.py`](tests/e2e/conftest.py) skips every live test. Plain pytest needs it
  too (`pytest -m e2e --run-live-e2e`).
- `uv run poe test-e2e-mutating`: create, update, and delete disposable
  `sdk-e2e-test-*` objects in the real account (`-m e2e_mutating`).
  [`tests/e2e/ledger.py`](tests/e2e/ledger.py) records each one. `uv run poe e2e-cleanup` lists
  leftovers and `--delete` removes them. Never let a test touch an object
  the ledger does not hold.
- `uv run poe lint`: `ruff check --fix`, `ruff format` (Python, and Python
  blocks in Markdown), and `rumdl check --fix` (Markdown rules).
  `uv run poe lint-check` runs the same checks without changing files, as CI
  does.
- `uv run poe typecheck`: ty on the whole repository
- `uv run poe check-specs`: FR/SC/task cross-references in `specs/`
- `uv run poe check-drift`: fails when the working tree differs from the
  commit. CI runs it after `generate`
- `uv run poe export-requirements`: rewrites `requirements.txt` from `uv.lock` (runtime
  dependencies with hashes, no project). `uv run poe check-requirements` fails when the file
  is stale, and CI runs it. Commit the file with every `uv.lock` change.
- `uv run poe audit`: `uv audit` of the locked dependencies
- `uv run poe clean`: removes `src/kentik_api/gen/`, `docs/build/`,
  generated `docs/sphinx/services/*.md`, and every `__pycache__` outside
  `.venv` (preserves `scripts/openapi_templates/`, `src/kentik_api/core/`,
  `docs/sphinx/local_generation_workflow.md`)
- `uv run poe deep-clean`: `clean` plus `.venv`, `.pytest_cache/`,
  `.ruff_cache/`. It keeps the tracked `uv.lock`. On Windows it keeps the
  running `.venv` and prints the command that removes it.

[`scripts/tasks.py`](scripts/tasks.py) holds the `clean`, `deep-clean`, and `check-drift`
tasks in Python, so no task needs a POSIX shell.

## Testing strategy (5 layers, see `tests/README.md`)

Mocked/offline layers (no network, safe to run anywhere, part of
`uv run poe test`):

- [`tests/generated/test_wrapper_contracts.py`](tests/generated/test_wrapper_contracts.py): auto-discovers
  every `*ServiceWrapper` method by AST-parsing
  `src/kentik_api/gen/*/services/*.py`. It then runs parametrized
  contract tests (forwarding behavior, gRPC-unimplemented check,
  kwarg validation, full-option forwarding). This auto-discovery
  picks up new services and endpoints automatically. Only add logic
  here when the wrapper contract itself changes globally.

- [`tests/generated/test_endpoint_schema_coverage.py`](tests/generated/test_endpoint_schema_coverage.py): for every
  discovered endpoint, drives the real `request_json` runtime and
  generated error classes (via `respx`-mocked HTTP) against every
  declared response status code. This includes both the success
  status and every entry in that service's generated
  `error/__init__.py::response_error_map`. Shared discovery and
  sample-building helpers live in `tests/_discovery.py` (at the
  tests root, not inside one layer, since `tests/e2e/` imports it
  too). The wrapper contract, schema coverage, path encoding, gRPC
  request mapping, retry eligibility, and auto-discovered e2e suites
  import these helpers. This keeps their discovery identical.

- [`tests/generated/test_schema_operations.py`](tests/generated/test_schema_operations.py): holds the generated
  REST modules to `schema_operations.json`: the same operations, a
  `data` argument wherever the swagger has a body, an argument for
  each swagger parameter, and a declared success status. Runs
  without a schema checkout.

- [`tests/runtime/test_rest_runtime.py`](tests/runtime/test_rest_runtime.py): shared request/auth/error
  behavior in `src/kentik_api/core`.

- [`tests/smoke/test_client_mounts_and_calls.py`](tests/smoke/test_client_mounts_and_calls.py): lightweight
  client-wiring checks. Keep this suite small and fast.

- `tests/generator/`: unit tests for `scripts/generation/*.py`
  (see "The generator's phase modules" above), for example
  `test_parity.py`, `test_error_package.py`,
  `test_wrapper_generation.py`, and `test_public_names.py`.
  [`tests/generator/README.md`](tests/generator/README.md) lists every file. These test
  the generator itself, not the SDK it produces. They build minimal
  swagger or fixture data with `tmp_path`, instead of needing a real
  or local schema checkout.

- Prefer deterministic unit tests (monkeypatch/mocks) over live
  network calls for all five of the above.

- If generation output changed, follow these steps before opening a
  PR:
  1. Regenerate: `uv run poe generate --local`.
  2. Read the message at the end of the run. If it says `⚠️ API SURFACE
     CHANGED`, write a `CHANGELOG.md` Unreleased entry for each listed
     change, naming each breaking change exactly as the alert does. Then
     run `uv run poe check-changelog --since HEAD`. `uv run poe generate` never writes
     release notes or `CHANGELOG.md` itself. Skipping this step fails the
     `changelog` CI job. See "Update the release notes after every
     regeneration" in `docs/sphinx/guides/generation.md`.
  3. Run the relevant focused suite.
  4. Run `uv run poe test`.

  CI also runs these gates on every pull request. Run them locally
  first:

  - the full mocked test suite on Python 3.12, 3.13, and 3.14 on Linux,
    and on 3.12 on Windows and macOS (the `test` job)
  - `uv run poe typecheck` on all three operating systems
  - `uv run poe lint-check` on all three operating systems
  - `uv run poe check-specs`
  - `uv run poe check-changelog` against the merge base (the `changelog`
    job)
  - the Sphinx build with `-W` (`uv run poe docs-build`)
  - the built wheel, installed into a clean virtual environment
    outside the checkout ([`build.yml`](.github/workflows/build.yml))
  - generated-output drift: CI runs `uv run poe generate` at the commit in
    `schema.lock`, then `uv run poe check-drift`, on all three operating
    systems, and fails if the tree differs from what is committed. Commit
    `schema.lock` with every regeneration, or this gate regenerates from
    the wrong commit.

Live layer (real network, opt-in only, not part of `uv run poe test`):

- `tests/e2e/`: end-to-end tests against the real Kentik API. See
  the requirement below. This directory and target are a required
  addition, not optional polish.
- [`tests/e2e/test_endpoints_e2e_grpc.py`](tests/e2e/test_endpoints_e2e_grpc.py) (`uv run poe test-e2e-grpc`, `-m
  e2e_grpc`): the gRPC-transport variant of the same read-only
  coverage. A `NotImplementedError` counts as a passing outcome here
  (see "gRPC transport is fully implemented" above). Today every
  operation of a service with protos has a gRPC translation, so it means
  the service's proto companions failed to import. A future operation
  also raises it when no RPC shares its HTTP rule. Services from the
  local schema base are REST-only and always use `_v5_transport`.

### Test coverage requirement

Generated and contract tests must exercise every endpoint and
every option discoverable from the OpenAPI schemas for each
service. This means every `operationId` (path × HTTP method), every
declared request parameter and request-body field, and every
declared response status code, including error responses, not a
representative subset. This is a standing rule, not a one-time task.
It applies every time someone adds tests or regenerates `gen/`,
including whenever a schema update adds new services, endpoints, or
parameters. Treat incomplete endpoint or option coverage as a bug in
the test suite or the generator, not an acceptable gap.

This mocked coverage only proves the SDK is internally
self-consistent: it correctly handles every status the schema
declares. It cannot prove the SDK still matches the real API's
current behavior. That requires the end-to-end layer below.

### End-to-end testing requirement

You must also generate and run end-to-end tests against the real Kentik
API. This is required, not optional. This is a standing rule
alongside the mocked coverage requirement above, not a one-time
task.

- Location: `tests/e2e/`, mirroring the auto-discovery style
  `tests/generated/` already uses. Derive the endpoint list from
  `tests/_discovery.py`, rather than hand-listing operations. This
  way, new endpoints get e2e coverage automatically as the schema
  grows.
- Credentials: the real project-root `.env` (`KENTIK_EMAIL` and
  `KENTIK_API_TOKEN`). Tests load these the same way `KentikAPI()`
  does. Never hardcode credentials in test code. Never read or print
  `.env` contents (see Auth/config below).
- Opt-in only, never part of the default pipeline. `.env`
  holds real credentials against a real account. e2e tests must not
  run automatically via `uv run poe test`, `uv run poe all`, or CI, without
  explicit opt-in. Gate them behind a dedicated `test-e2e` /
  `test-e2e-grpc` poe task, a pytest marker (for example `-m
  e2e`/`-m e2e_grpc`) excluded by default, or both. `uv run poe test` and
  `uv run poe all` must keep passing without ever touching this layer.
- Default to safe, non-mutating operations (List- and Get-style
  reads). Create, Update, and Delete calls against a real account
  are hard to reverse, and they can corrupt real data. Only cover
  mutating endpoints against a disposable, sandboxed resource with
  guaranteed cleanup, for example create-then-delete in a
  `finally` block or fixture teardown. Call out adding such coverage
  explicitly. Do not add it silently as a side effect of other work.
- If a real response no longer matches the generated models or
  error classes, that is a genuine bug to fix (schema sync or
  generator). Never paper over it inside the e2e test itself.

## Auth/config

`KentikAPI` resolves credentials in this order: explicit
`email`/`api_token` args, then the `KENTIK_EMAIL`/`KENTIK_API_TOKEN`
environment variables, then the `env_file` arg (`.env` by default,
searched upward from the cwd, and `None` disables it). The client reads the file
with `dotenv_values` into a dict, and only when a value is still
missing. An explicit argument that is empty or only whitespace raises
`ConfigurationError` instead of falling back. Never switch this back to `load_dotenv`: writing the file
into `os.environ` leaks secrets into every subprocess, which breaks
callers that keep credentials encrypted (sops, age). Never read or print `.env` contents: it holds real
credentials.

## Constraints

- Do not introduce breaking API surface changes without calling
  them out explicitly.
- Keep changes focused. Avoid unrelated refactors.
- Known generator warnings are non-blocking. Track and reduce them
  over time. Do not ignore them silently.

## Branch naming and Jira

This repo follows the `<category>/<short-kebab-description>` rule in
the shared agent rules below. Do not use the branch name that Jira
generates. To link work to its Jira ticket, put the ticket key (for
example `FA-2`) at the start of the pull request title. Jira also
links a commit that names the key.

Until the V6 work merges into `main`, `feat/v6-sdk` is the base
branch. `main` does not have the V6 SDK yet. Create each new branch
from `feat/v6-sdk`, and merge it back with `git merge --no-ff`. The
maintainer opens the pull request from `feat/v6-sdk` into `main` by
hand.

## Remotes: the fork only

The remote `origin` is Kentik's repository. The remote `fork` is the
maintainer's personal fork.

- Push, merge, delete branches, or commit on a remote only in `fork`.
  Never do any of these in `origin`.
- Never open, update, comment on, or close a pull request in any Kentik
  repository (`kentik/*`). The maintainer does all of those by hand. When
  you are asked to open a pull request, open it inside the fork.

<!-- shared-rules:start -->
<!-- Synced from ~/.claude/CLAUDE.md; regenerate by re-running the
     agents-md skill instead of hand-editing this block. CLAUDE.md
     imports this file with `@AGENTS.md`, so Claude Code sees this
     section too. -->

## Shared agent rules

These rules apply in every project, regardless of which coding
agent is being used.

### Git branching

Never commit directly to the default branch (`main`/`master`).
Every unit of work gets its own branch, created from an up-to-date
default branch, and named `<category>/<short-kebab-description>`.

Branch categories, by the primary intent of the change:

| Prefix | Use for |
| --- | --- |
| `feat/` | New capability or user-visible functionality |
| `fix/` | Correcting broken behavior |
| `refactor/` | Restructuring with no behavior change |
| `perf/` | Optimization where observable behavior is unchanged |
| `docs/` | Documentation, comments, README/design docs only |
| `test/` | Adding or fixing tests only |
| `chore/` | Deps, tooling, CI, config, `.gitignore`, release prep |
| `security/` | Fixing a vulnerability or hardening a boundary |

Branch hygiene:

- One concern per branch. If a change needs "and" to describe it,
  it is probably two branches.
- Name the change, not the component. `fix/env-parse-order` beats
  `fix/cli`. Keep it under ~40 characters.
- Phased or numbered work carries the phase in the name, when a
  project plan uses one: `feat/phase-4-config-backup`.
- Delete the branch after it merges.
- Ask before force-pushing, rebasing shared history, or deleting a
  branch that was pushed to a remote.

Merging: where a remote supports pull requests, push the branch,
open a PR, and let the platform merge it, instead of merging
locally.

- Squash and merge: the default for most PRs. Collapses the branch
  into one commit on the default branch.
- Rebase and merge: use when the branch's commits are each clean
  and meaningful on their own, worth preserving separately.
- Merge commit (`--no-ff`): use for a long-lived branch worth
  keeping visible in history.
- For a purely local merge outside a PR platform, default to
  `--no-ff` over a plain fast-forward, unless the project's own
  instructions say otherwise.

Push and open a pull request: treat "opened a pull request," not
"committed," as the finish line for any repo with a remote you
don't solely maintain. Confirm with the user before pushing or
opening a PR, unless they have given standing authorization for
that repo. Skip this step for a personal, single-maintainer repo,
or once the user says they will handle it themselves.

### Writing style

- Never use em dashes: neither the `—` character nor a `--`
  stand-in used as punctuation. This applies everywhere: code, docs,
  docstrings, commit messages, agent instruction files, chat
  replies, in any project. Rewrite with a comma, a colon,
  parentheses, or a second sentence instead. Exception: `--` is fine
  as a literal CLI argument or flag separator, for example
  `git commit -- file` or `some-command --flag`.
- Comments and docstrings should be concise: state the WHY, not the
  WHAT, and skip restating what already-readable code shows.

<!-- shared-rules:end -->
