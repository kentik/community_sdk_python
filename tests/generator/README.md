<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Generator Tests

This layer is mocked and uses no network. It holds unit tests for the SDK generator itself (see
[scripts/generation/README.md](../../scripts/generation/README.md)),
not for the SDK that it produces. See the layered strategy in
[../README.md](../README.md) for how this layer fits with the other
four.

## Files

| File | Covers |
| --- | --- |
| [`test_parity.py`](test_parity.py) | Swagger selection, schema structural validation, generated/schema directory parity, and `iter_service_dirs()`: the single rule for which directories under `gen/` are Services. |
| [`test_error_package.py`](test_error_package.py) | Error class naming, error-response extraction and merging, and the runtime error-dispatch injection seam (including the `ValueError` guard when the anchor is absent). |
| [`test_fixup.py`](test_fixup.py) | Post-generation fixups: `models/__init__.py` rebuild, wildcard-export replacement, file-level content patches, function deduplication, and docstring normalization. |
| [`test_wrapper_generation.py`](test_wrapper_generation.py) | Annotation qualification and end-to-end wrapper and client-mixin generation against a temp directory. |
| [`test_public_names.py`](test_public_names.py) | [`public_names.json`](../../public_names.json): version-free keys, default names, and the failure when an entry no longer matches the schema. |
| [`test_rest_module_parser.py`](test_rest_module_parser.py) | `parse_generated_rest_module()` in [`scripts/generation/_shared.py`](../../scripts/generation/_shared.py): the shared REST-operation parser that [`tests/_discovery.py`](../_discovery.py) also uses. |
| [`test_endpoint_docs.py`](test_endpoint_docs.py) | `parse_wrapper_methods()`/wrapper-signature parsing in [`scripts/generation/endpoint_docs.py`](../../scripts/generation/endpoint_docs.py) and [`_shared.py`](../../scripts/generation/_shared.py), the derived `AUTO-GENERATED` provenance header, and that a failed extraction propagates its error and does not swallow it. |
| [`test_docs_rendering.py`](test_docs_rendering.py) | The consistency of `_GROUP_CONFIG`/`_module_group`/`_LAYER_NAMES` (architecture-diagram module grouping) in [`scripts/generation/docs_rendering.py`](../../scripts/generation/docs_rendering.py). |
| [`test_generate_sdk.py`](test_generate_sdk.py) | The top-level helpers in [`scripts/generate_sdk.py`](../../scripts/generate_sdk.py): schema-name cleanup, request-body `$ref` inlining through `patched_swagger` (the path that a real run uses), generated gRPC import rewriting, and the validate-before-clean ordering guard. |
| [`test_api_surface.py`](test_api_surface.py) | [`scripts/generation/api_surface.py`](../../scripts/generation/api_surface.py). Builds surface dicts directly instead of generating an SDK. `capture()` runs against a minimal fixture tree. |
| [`test_release_notes.py`](test_release_notes.py) | The [`CHANGELOG.md`](../../CHANGELOG.md) check in [`scripts/release_notes.py`](../../scripts/release_notes.py). |
| [`test_impact_report.py`](test_impact_report.py) | The impact report's classification, which decides what a reviewer looks at first. |
| [`test_openapi_templates.py`](test_openapi_templates.py) | The custom OpenAPI templates, rendered with the generator's own Jinja settings. |
| [`test_toolchain_versions.py`](test_toolchain_versions.py) | The declared runtime floors in [`pyproject.toml`](../../pyproject.toml) against the versions protoc stamps into the generated stubs. |

## Run

```bash
uv run poe test-generator
# or
uv run pytest tests/generator/
```

## Add a test here

Add a test when logic in `scripts/generation/*.py` changes. Most
tests build their own minimal swagger fragment or fake generated-file
fixture with `tmp_path` and need no schema checkout. One exception:
`test_the_real_alert_schema_keeps_acknowledgement_an_object` in
[`test_generate_sdk.py`](test_generate_sdk.py) reads the real local `../api-schema-public`
checkout. It skips when that checkout is absent.

To run a whole phase end to end, use the `sandbox` fixture in
[`conftest.py`](conftest.py). It copies the hand-written runtime and three
committed services (`device`, `alerting`, `core`) into `tmp_path`. It also points
the `PROJECT_ROOT` and `SDK_OUTPUT_DIR` of each phase module at the copy. The real
phase function then runs against the copy, and a test can compare its output with the
committed files. For example, a regenerated wrapper must match the committed one
byte for byte. Some output depends on which services exist (counts, the first
listed operation). A test normalizes those parts before it compares that output.

While you edit [`scripts/generate_sdk.py`](../../scripts/generate_sdk.py),
[`scripts/generation/`](../../scripts/generation/README.md), or template behavior, run this suite first.
Then run [`uv run poe test-generated`](../../pyproject.toml) to test the SDK that the generator produces.
