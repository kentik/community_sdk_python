<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# Generator Phase Modules

[`scripts/generate_sdk.py`](../generate_sdk.py) builds the SDK from Kentik's OpenAPI schema.
It handles CLI parsing and orchestration only. Each module in this
package owns one concern of SDK generation.

## Modules

| Module | Owns | Public interface |
| --- | --- | --- |
| [`parity.py`](parity.py) | Swagger file selection, joining the local schema base ([`schema/openapi/`](../../schema/openapi/)) to upstream, dropping files that newer files fully replace, schema structural validation, and directory parity checks | `select_latest_swagger_files_by_service()`, `merge_local_schema_base()`, `drop_superseded_swagger_files()`, `validate_schema_files_or_raise()`, `validate_selected_services_or_raise()`, `validate_generated_service_parity()` |
| [`error_package.py`](error_package.py) | Error class generation and error dispatch | `generate_service_error_package()`, `inject_service_error_handling()`, `collect_operation_error_responses()`, `merge_operation_error_responses()` |
| [`fixup.py`](fixup.py) | Generated-code post-processing: import patching, model init rebuild, file cleanup | `fix_generated_service()` |
| [`wrapper_generation.py`](wrapper_generation.py) | Service wrapper and client mixin generation. The mixin mounts a REST-only service (from the local schema base) on `_v5_transport` | `generate()`, `public_method_names()` |
| [`public_names.py`](public_names.py) | The public name of every Service, client method, and model, read from and added to [`public_names.json`](../../public_names.json). Fails when an entry no longer matches the schema | `PublicNames`, `operation_key()`, `model_key()`, `NameDriftError` |
| [`docs_rendering.py`](docs_rendering.py) | The runtime architecture page (a Mermaid call path and the dependency explorer), the `gen/` root README, service READMEs, the explorer assets in `docs/sphinx/_static/`, and the `kentik-gen` blocks in `docs/sphinx/guides/*.md` and [`docs/sphinx/README.md`](../../docs/sphinx/README.md) | `generate()` |
| [`explorer_docs.py`](explorer_docs.py) | Embeds an interactive diagram explorer in a Sphinx page, and writes its scoped CSS and script | `fragment()`, `write_static_assets()`, `explorer_css()` |
| [`diagram_kit.py`](diagram_kit.py) | A copy of the diagrams skill's kit, with its CSS, script, and theme tokens in [`diagram_assets/`](diagram_assets/). Draws the explorer SVG and checks its geometry | `node()`, `seg()`, `svg()`, `legend()`, `check()` |
| [`endpoint_docs.py`](endpoint_docs.py) | Per-endpoint Sphinx documentation, and [`schema_operations.json`](../../schema_operations.json), the swagger-derived operation record | `EndpointDocsCollector` |
| [`api_surface.py`](api_surface.py) | Records the public API surface (operations with their client methods, gRPC routes, and error classes, model fields, enum values) to [`api_surface.json`](../../api_surface.json), and compares two recordings to make release notes | `generate()`, `capture()`, `diff()`, `breaking_changes()`, `render_markdown()`, `read()`, `recorded_at()`, `render_regeneration_alert()` |
| [`_shared.py`](_shared.py) | Constants and helpers shared by two or more phase modules | `PROJECT_ROOT`, `SDK_OUTPUT_DIR`, `REGENERATE_COMMAND`, `INTERNAL_GEN_DIRS`, `iter_service_dirs()`, `discover_service_model_classes()`, `service_to_pascal_case()`, `normalize_symbol()`, `write_text_lf()`, `mermaid_init()`, `RestOperation`, `parse_generated_rest_module()`, `WrapperMethod`, `parse_wrapper_methods()`, `GrpcCall`, `grpc_call()`, `grpc_stub_services()` |

Keep a helper in [`_shared.py`](_shared.py) only when two or more phase modules call
it. Put a single-consumer helper in the one module that calls it
instead.

## Call order

`generate_modular_sdk()` in [`scripts/generate_sdk.py`](../generate_sdk.py) calls the phase
modules in this order. Each arrow names what the step before it leaves on disk.

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "elk", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
flowchart TD
  subgraph window["Schema checkout open · get_schema_root()"]
    s1("1. parity.select_latest_swagger_files_by_service()"):::blue
    s2("2. parity.validate_schema_files_or_raise()<br/>parity.validate_selected_services_or_raise()<br/>parity.drop_superseded_swagger_files()<br/>PublicNames.services() and .models()"):::blue
    s3("3. Generate REST code per swagger file<br/>endpoint_docs_collector.extract() runs here"):::orange
  end
  s4("4. parity.validate_generated_service_parity()"):::blue
  s5("5. fixup.fix_generated_service()<br/>once per service: import patching,<br/>model init, file cleanup"):::green
  s6("6. error_package.generate_service_error_package()<br/>once per service, named after client methods"):::green
  s7("7. wrapper_generation.generate()<br/>PublicNames.methods(), then public_names.json is saved"):::green
  s8("8. docs_rendering.generate()"):::violet
  s9("9. endpoint_docs_collector.render(), then .write_record()"):::violet
  s10("10. api_surface.generate()<br/>last, must see the final formatted output"):::cyan
  s11("11. Write the schema commit to schema.lock<br/>only a completed run"):::cyan

  s1 -->|"newest swagger files"| s2
  s2 -->|"valid files + public names"| s3
  s3 -->|"gen/ service directories"| s4
  s4 -->|"service directories"| s5
  s5 -->|"patched REST modules"| s6
  s6 -->|"error packages"| s7
  s7 -->|"wrappers + client_mixin.py"| s8
  s8 -->|"architecture page + READMEs"| s9
  s9 -->|"service pages + schema_operations.json"| s10
  s10 -->|"api_surface.json"| s11

  click s1 "parity.py"
  click s2 "parity.py"
  click s3 "../generate_sdk.py"
  click s4 "parity.py"
  click s5 "fixup.py"
  click s6 "error_package.py"
  click s7 "wrapper_generation.py"
  click s8 "docs_rendering.py"
  click s9 "endpoint_docs.py"
  click s10 "api_surface.py"
  click s11 "../../schema.lock"

  classDef blue fill:#e7f5ff,stroke:#1971c2,color:#1864ab
  classDef orange fill:#fff4e6,stroke:#e8590c,color:#d9480f
  classDef green fill:#ebfbee,stroke:#2f9e44,color:#2b8a3e
  classDef violet fill:#f3f0ff,stroke:#7048e8,color:#5f3dc4
  classDef cyan fill:#e3fafc,stroke:#1098ad,color:#0b7285
  classDef blue,orange,green,violet,cyan stroke-width:2px,rx:10px
  style window fill:none,stroke:#868e96,stroke-width:2px
  linkStyle default stroke-width:2px,stroke-linecap:round,stroke-linejoin:round
```

> [!WARNING]
> Call `endpoint_docs_collector.render()` only after
> `wrapper_generation.generate()` finishes. `render()` reads wrapper
> method signatures from the files that `wrapper_generation.generate()`
> writes.

## Import rules

[`scripts/generate_sdk.py`](../generate_sdk.py) runs as a direct script:
`uv run python scripts/generate_sdk.py`. Python puts [`scripts/`](../README.md) on
`sys.path` automatically for a direct script run. `generate_sdk.py`
imports this package as `from generation import ...`.

Tests import the same modules as `from scripts.generation import ...`.
The `pythonpath = ["."]` setting in [`pyproject.toml`](../../pyproject.toml) adds the repo root
to `sys.path` for tests.

Both import styles load the same files under different top-level
names. Use a relative import (`from ._shared import ...`) for every
import between files inside this package. A relative import resolves
correctly under either name. An absolute `scripts.generation.*` import
inside this package breaks `generate_sdk.py`'s import path.

## Add a new phase module

1. Create `scripts/generation/<name>.py`.
2. Give it one small public interface. A single `generate()` function
   is usually enough. Use more than one function only when the
   module's steps run at different points in the orchestration.
3. Import shared helpers from `._shared` with a relative import.
4. Call the new module from `generate_modular_sdk()` in
   [`scripts/generate_sdk.py`](../generate_sdk.py).
5. Add tests under `tests/generator/test_<name>.py`.

## Run the tests

```bash
uv run poe test-generator
```

This command runs only the tests in [`tests/generator/`](../../tests/generator/README.md). Most tests
build their own temporary swagger fragment or fake generated-file
fixture with `tmp_path` and need no schema checkout. One exception:
`test_the_real_alert_schema_keeps_acknowledgement_an_object` in
[`test_generate_sdk.py`](../../tests/generator/test_generate_sdk.py) reads the real local `../api-schema-public`
checkout. It skips when that checkout is absent.
