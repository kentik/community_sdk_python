<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](pyproject.toml). Edit directly. -->

# Kentik Community Python SDK

This SDK is a typed Python client for the Kentik API, built on
Pydantic v2. [`scripts/generate_sdk.py`](scripts/generate_sdk.py) generates it from Kentik's
public OpenAPI v3 schema. This file covers the runtime shape of the
generated SDK and the generator that builds it.

## Language

Each term below has one meaning in this repository. The last line of
each entry names the words to avoid for that term.

### Service

A top-level grouping of the Kentik API, for example `device`,
`alerting`, or `synthetics`. Each service maps to one directory
under [`src/kentik_api/gen/`](src/kentik_api/gen/README.md) and one attribute on `KentikAPI`, for
example `client.device`. Not every directory in `gen/` is a Service.
The generator also writes internal directories for itself. Today the only
one is [`pb_companions`](src/kentik_api/gen/pb_companions/) (the shared proto descriptor registry).
`iter_service_dirs()` in [`scripts/generation/_shared.py`](scripts/generation/_shared.py) is the one
place that decides which is which. A Service with no operations is still a
Service.

Avoid the words module and package.

### Operation

A single OpenAPI operation: one `operationId`, unique per HTTP
method and path within a merged service. Each operation becomes one
generated REST function and one method on a service's
`ServiceWrapper`.

Avoid the words endpoint, function, and method.

### Swagger family

The `(service, namespace, filename)` grouping key of the generator.
When several versioned swagger files exist, the generator uses this key
to pick the latest schema version. The generator generates only the
newest version in each family and skips older versions. It also skips a
file when newer files in its service write all of that file's REST
modules.

### Local schema base

The [`schema/openapi/`](schema/openapi/) directory in this repository. It holds
hand-maintained OpenAPI descriptions of endpoints that upstream does not
publish. The generator reads it next to the upstream schema. Today it
holds `v5`, the V5 query and batch endpoints. Every service from it is
REST only.

Avoid the words second schema root and local root.

### Phase module

One of the independently testable units in [`scripts/generation/`](scripts/generation/README.md)
(`parity`, `error_package`, `fixup`, `wrapper_generation`,
`docs_rendering`, `endpoint_docs`, `api_surface`, `public_names`). Each phase module owns one concern of SDK
generation. The orchestration in [`scripts/generate_sdk.py`](scripts/generate_sdk.py) calls them in
sequence.

Avoid the words generator step and stage.

### Service error package

The `error/__init__.py` file that the
[`error_package`](scripts/generation/error_package.py) phase module
generates for one service. It defines a base error class, one class per
operation, and one leaf class per declared error response. Each
operation class takes the name of the operation's client method
(`label.list` raises `ListError`). The runtime dispatches errors through
`error_cls.from_response`.

### Parity validation

The check that compares the set of generated service directories
against the public names that [`public_names.json`](public_names.json) gives the top-level
schema service directories. If any
directory does not match, the check fails the whole generation run.

### EndpointDocsCollector

The object with three methods (`extract()`, `render()`, `write_record()`) that accumulates
per-endpoint documentation. `extract()` runs while swagger files are
available. `render()` builds Sphinx stubs from that documentation
afterward. `render()` must run after wrapper generation, because its
examples read real method signatures that wrapper generation writes.
`write_record()` writes [`schema_operations.json`](schema_operations.json).

Avoid the words doc builder and doc generator.
