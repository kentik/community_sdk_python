<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# OpenAPI Generator Templates

This folder holds custom Jinja2 templates. [`generate_sdk.py`](../generate_sdk.py) passes them to
`openapi-python-generator` with `--custom-template-path` (see `openapi_generator_cmd()` in
[../generate_sdk.py](../generate_sdk.py)). They override the
generator's default per-operation and per-module output, so every
generated call goes through the shared REST runtime instead of
hand-rolled HTTP code.

## Files

| Template | Replaces | Purpose |
| --- | --- | --- |
| [`httpx.jinja2`](httpx.jinja2) | Per-operation function body | Writes the operation summary and description as the docstring, builds `query_params`/`header_params`, calls `request_json(...)`, and converts the raw JSON body into the declared Pydantic model or list. The service wrapper copies that docstring. |
| [`service.jinja2`](service.jinja2) | Per-service module header | Imports `request_json` and the wildcard model/`typing` imports that every generated operation needs. |
| [`models_pydantic_2.jinja2`](models_pydantic_2.jinja2) | Per-model class | Writes the schema title and description as the docstring, and each field's schema text as `Field(description=...)`. |
| [`_macros.jinja2`](_macros.jinja2) | Nothing (imported) | `docstring()` and `string()` turn schema text into Python literals. |

The generator renders with `autoescape=True`, which writes `"` as `&#34;`.
Schema text must go through a [`_macros.jinja2`](_macros.jinja2) macro, which escapes it for
Python and marks it `safe`.

## Why these exist

Without a custom template, `openapi-python-generator` emits a direct
`httpx` call per operation. That duplicates auth headers, error
handling, and status checks across every generated
service. [`httpx.jinja2`](httpx.jinja2) calls
[`request_json()`](../../src/kentik_api/core/rest_runtime.py) instead: the
single shared function that owns all of that. See the "shared
connection handler" section of the repository root
[AGENTS.md](../../AGENTS.md) for why this pattern must not regress.

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "elk", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
flowchart TD
  svc("service.jinja2<br/>per-service module header"):::greenSrc
  op("httpx.jinja2<br/>per-operation body"):::blueSrc
  inj("inject_service_error_handling()<br/>error_package.py"):::violet
  mod("Generated REST module<br/>gen/{service}/services/<br/>import request_json<br/># __ERROR_IMPORTS_PLACEHOLDER__<br/>def operation(...)"):::hub
  rj("request_json()<br/>core/rest_runtime.py"):::hub
  hx("httpx.Client<br/>one per APIConfig"):::orangeSrc

  j1@{ shape: f-circ }
  class j1 join
  svc --- j1
  op --- j1
  j1 -->|"rendered Python"| mod
  inj -->|"from ..error import ... in place of the sentinel<br/>error_cls= per function"| mod
  mod -->|"request arguments"| rj
  rj -->|"HTTP request"| hx
  hx -->|"HTTP response"| rj
  rj -->|"parsed JSON"| mod

  click svc "service.jinja2"
  click op "httpx.jinja2"
  click inj "../generation/error_package.py"
  click rj "../../src/kentik_api/core/rest_runtime.py"

  classDef blueSrc fill:#a5d8ff,stroke:#1971c2,color:#1864ab
  classDef greenSrc fill:#b2f2bb,stroke:#2f9e44,color:#2b8a3e
  classDef violet fill:#f3f0ff,stroke:#7048e8,color:#5f3dc4
  classDef orangeSrc fill:#ffd8a8,stroke:#e8590c,color:#d9480f
  classDef hub fill:#f8f9fa,stroke:#495057,color:#212529
  classDef blueSrc,greenSrc,violet,orangeSrc,hub stroke-width:2px,rx:10px
  classDef join fill:#868e96,stroke:#868e96
  linkStyle default stroke-width:2px,stroke-linecap:round,stroke-linejoin:round
```

## Editing a template

1. Change the `.jinja2` file here, not the generated output.
2. Regenerate: `uv run python scripts/generate_sdk.py --local-repo
   ../api-schema-public`.
3. Compare a generated service module with its earlier version, and make sure that the output has the new shape.
4. Run [`uv run poe test-generated`](../../pyproject.toml) to make sure that generated calls still exercise
   `request_json` and every declared response status.

> [!WARNING]
> `service.jinja2` must keep emitting both the
> `from kentik_api.core.rest_runtime import request_json` import line and
> the `# __ERROR_IMPORTS_PLACEHOLDER__` sentinel right after it.
> `error_package.inject_service_error_handling()` replaces that sentinel to
> wire in per-service error classes. When the sentinel is missing, it falls
> back to the `request_json` import line. `fixup._fix_path_parameters()` also
> matches that line. When the anchor is missing, generation fails with
> `ValueError`. Rename either anchor only together with both functions.
