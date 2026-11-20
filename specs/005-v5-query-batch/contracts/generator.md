# Contract: generator changes

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md) R2, R10, R15

## Input

- `schema/openapi/` is the local schema base, kept in this repository. It
  holds only hand-maintained descriptions of endpoints that upstream does
  not publish. Its
  layout is `<service>/<version>/<file>.swagger.json`, the same as the
  upstream base below `gen/openapiv3/kentik/`.
- The only file is `schema/openapi/v5/v5/v5.swagger.json`.

## Behavior

1. `validate_schema_files_or_raise()` checks the files of both bases before
   `gen/` is touched.
2. `select_latest_swagger_files_by_service()` runs on each base. A service
   that appears in both bases raises `RuntimeError` that names it.
3. The source service set is the union. `public_names`, the parity check, the
   generation loop, and `EndpointDocsCollector` use the union.
4. A service from the local schema base has no proto lookup, no `pb/` stubs, and no
   gRPC routes.
5. `wrapper_generation.generate()` takes the local service set. The mixin
   mounts a local service as `V5ServiceWrapper(self._v5_transport)`.
6. `api_surface` writes `"rest_only": true` for a local service, and
   `SCHEMA_VERSION` becomes 8. A record before version 8 reads as
   `rest_only: false`.
7. `endpoint_docs` writes the REST-only example text for a local service.
   `docs_rendering` names the local schema source in the `gen/` README and
   marks the service as REST-only on the architecture page.
8. `models_pydantic_2.jinja2` adds `"extra": "allow"` to `model_config`
   when a schema sets `additionalProperties` to the literal `true`. Every
   other schema keeps the default.

## Unit tests (`tests/generator/`)

- Two bases with different services give the union, and the parity check
  passes.
- The same service in both bases fails the run.
- A local service gets no gRPC branch and mounts on `_v5_transport`.
- `api_surface` writes and reads `rest_only`, and a version 7 record reads as
  `rest_only: false`.
- A broken local file fails `validate_schema_files_or_raise()`.
- A schema with `additionalProperties: true` gives a model that keeps and
  sends unknown fields. Regenerating the upstream schema gives no diff.
