# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Runtime architecture docs (inline Mermaid), the gen/ root README, and per-service READMEs.

Also updates <!-- kentik-gen:MARKER --> blocks in docs/sphinx/guides/ files so every
reference to generated service names, method names, and class names stays
current without manual edits.
"""

import ast
import re
from pathlib import Path

from . import diagram_kit as dk
from ._shared import (
    PROJECT_ROOT,
    REGENERATE_COMMAND,
    SDK_OUTPUT_DIR,
    iter_service_dirs,
    mermaid_init,
    parse_generated_rest_module,
    parse_wrapper_methods,
    write_text_lf,
)
from .explorer_docs import fragment, write_static_assets

_GUIDES_DIR = PROJECT_ROOT / "docs" / "sphinx" / "guides"
# A Mermaid rect takes no CSS variable, so the gray must read on light and dark pages.
_SHARED_RUNTIME_BAND = "rgba(120,130,140,0.14)"

_GEN_ROOT_README = f"""\
<!-- AUTO-GENERATED: scripts/generation/docs_rendering.py, _generate_gen_root_readme() -->
<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->
# Generated Services (`kentik_api.gen`)

The generator builds every file in this folder. Each
[`{REGENERATE_COMMAND}`](../../../pyproject.toml) run deletes each subdirectory here,
builds it again, and writes this README again.

> [!WARNING]
> Do not edit any file in this folder, this README included. The next run deletes the edit.
> If the output is wrong, fix the generator ([`scripts/generate_sdk.py`](../../../scripts/generate_sdk.py)),
> a phase module in [`scripts/generation/`](../../../scripts/generation/README.md), or a template in
> [`scripts/openapi_templates/`](../../../scripts/openapi_templates/README.md). Then run the generator again.

## Layout

Each subdirectory is one Kentik API service (`device`, `alerting`, `user`, and others).
The generator builds it from the OpenAPI v3 schema files of that service.
Each service directory has the same shape:

```text
gen/device/
├── models/      Pydantic v2 request and response models
├── services/    one REST function per operation, and the DeviceServiceWrapper class
├── error/       one error class per operation, picked by the response status code
├── pb/          gRPC stubs (*_pb2.py, *_pb2_grpc.py) for the gRPC transport
└── README.md    a link to the Sphinx reference page of the service
```

## Where a call runs

No service directory here has its own HTTP, auth, or retry code.

- On a REST transport, each generated REST function calls `request_json()` in
  [`kentik_api.core`](../core/README.md). That one function sends the REST traffic of every service.
- On a gRPC transport, a wrapper method calls `call_grpc()` in [`kentik_api.core`](../core/README.md).
  The generator writes that call when an RPC has the same HTTP rule as the REST operation: the same
  proto service, verb, and path.

A wrapper method raises `NotImplementedError` on a `GrpcTransport` in two cases only:

1. The proto companions of the service did not import.
2. No RPC has the same HTTP rule as the operation.

[SDK Runtime Architecture](../../../docs/sphinx/sdk_runtime_architecture.md) shows the full call path.

## Full reference

The page `docs/sphinx/services/<service>.md` gives the parameters, the response shapes, and a usage
example for each operation of a service. The built Sphinx docs show the same pages.
"""


def _services_without_wrappers_section() -> list[str]:
    """Explains why some generated Services are absent from the client.

    Generated rather than hand-written prose so the service list cannot go stale:
    the gap closes on its own if upstream adds the missing HTTP bindings.
    """
    unmounted = [
        service_dir.name
        for service_dir in iter_service_dirs()
        if not any(
            parse_generated_rest_module(module)
            for module in (service_dir / "services").glob("*.py")
        )
    ]
    if not unmounted:
        return []

    return [
        "## Services Without A Wrapper",
        "",
        "The REST paths in the OpenAPI schema drive wrapper generation. If the schema",
        "of a Service declares no paths, the generator writes its models and proto",
        "stubs but no wrapper, and the client does not mount it. This is intentional.",
        "REST operations are the contract of this SDK. Wrapper generation from protos",
        "is out of scope.",
        "",
        f"{len(unmounted)} Services are in that state today: "
        + ", ".join(f"`{name}`" for name in unmounted)
        + ".",
        "",
        "Some of these Services declare gRPC RPCs upstream, but the RPCs have no",
        "`google.api.http` annotation, so no path reaches the schema. That is a gap",
        "in the upstream schema, not in the SDK. If upstream adds the annotation, the",
        "next run generates the wrapper.",
        "",
    ]


def _rest_only_services_section(rest_only: frozenset[str]) -> list[str]:
    """Names the Services generated from the local schema base, which are REST only."""
    if not rest_only:
        return []
    return [
        "## REST-Only Services",
        "",
        "These Services come from the local schema base, `schema/openapi/`. It holds",
        "descriptions, maintained by hand, of endpoints that upstream does not publish.",
        "Each client mounts these Services on a REST transport to their own host. A",
        'client with `protocol="grpc"` also sends their calls over REST: '
        + ", ".join(f"`{name}`" for name in sorted(rest_only))
        + ".",
        "",
    ]


def _generate_gen_root_readme() -> None:
    """Writes src/kentik_api/gen/README.md, kept in sync with the gen/ tree."""
    SDK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_text_lf(SDK_OUTPUT_DIR / "README.md", _GEN_ROOT_README)


def _generate_service_readmes(rest_only: frozenset[str] = frozenset()) -> None:
    """Generates README.md files inside each service directory."""
    print("Generating module READMEs...")
    for service_dir in iter_service_dirs():
        service_name = service_dir.name
        source = (
            "a description in the local schema base, `schema/openapi/`. It is REST only."
            if service_name in rest_only
            else "the Kentik OpenAPI v3 schema."
        )

        lines = [
            "<!-- AUTO-GENERATED: scripts/generation/docs_rendering.py, _generate_service_readmes() -->",
            f"<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->",
            f"# {service_name.replace('_', ' ').title()} Service",
            "",
            f"The generator builds this module from {source}",
            "",
            "See the [service reference][reference] for the data models.",
            "For each operation, it lists parameters, responses, and a usage example.",
            "",
            f"[reference]: ../../../../docs/sphinx/services/{service_name}.md",
        ]

        doc_content = "\n".join(lines) + "\n"

        write_text_lf(service_dir / "README.md", doc_content)


def _module_name_from_path(py_path: Path, package_root: Path) -> str:
    rel = py_path.relative_to(package_root).with_suffix("")
    return "kentik_api." + ".".join(rel.parts)


def _resolve_import_from(current_module: str, level: int, module: str | None) -> str:
    if level == 0:
        return module or ""

    parts = current_module.split(".")[:-1]
    if level > 0:
        ups = max(level - 1, 0)
        parts = parts[: len(parts) - ups] if ups <= len(parts) else []
    suffix = module.split(".") if module else []
    return ".".join(parts + suffix)


_GROUP_CONFIG: dict[str, tuple[str, str]] = {
    # label: (layer, source path under kentik_api/)
    "Client API": ("client", "client.py"),
    "Client Mixin": ("client", "client_mixin.py"),
    "Auth Credentials": ("foundation", "auth/"),
    "API Config": ("foundation", "core/api_config.py"),
    "REST Runtime": ("foundation", "core/rest_runtime.py"),
    "gRPC Runtime": ("foundation", "core/grpc_runtime.py"),
    "Rate Limit": ("foundation", "core/rate_limit.py"),
    "Error Types": ("foundation", "errors/"),
    "Transport Base": ("transport", "transports/base.py"),
    "REST Transport": ("transport", "transports/rest_client.py"),
    "gRPC Transport": ("transport", "transports/grpc_client.py"),
    "Generated Service Wrappers": ("generated", "gen/{service}/services/{service}.py"),
    "Generated REST Services": ("generated", "gen/{service}/services/"),
    "Generated Models": ("generated", "gen/{service}/models/"),
    "Generated Error Classes": ("generated", "gen/{service}/error/"),
    "Generated Proto Stubs": ("generated", "gen/{service}/pb/"),
}

_LAYER_NAMES: dict[str, str] = {
    "client": "Client Layer",
    "generated": "Generated Layer",
    "transport": "Transport Layer",
    "foundation": "Shared Foundation",
}

# Explorer parts, each a set of module groups. The layout is fixed by hand, so
# _dependency_explorer() checks every drawn wire against the scanned imports.
_PART_GROUPS: dict[str, tuple[str, ...]] = {
    "base": ("API Config", "Auth Credentials", "Error Types", "Rate Limit"),
    "rj": ("REST Runtime",),
    "cg": ("gRPC Runtime",),
    "tr": ("Transport Base", "REST Transport", "gRPC Transport"),
    "models": ("Generated Models",),
    "rest": ("Generated REST Services", "Generated Error Classes"),
    "pb": ("Generated Proto Stubs",),
    "wrap": ("Generated Service Wrappers",),
    "client": ("Client API", "Client Mixin"),
}

_W, _H = 200, 72
_COLS = (40, 330, 620)
_ROWS = (30, 170, 310, 450, 590)

# The import graph has one root, KentikAPI, so it starts at the top center and
# each arrow points from a part to a part that it imports.
# part: (column, row, family, kind, box lines, card title, role, if it stops)
_PARTS: dict[str, tuple[int, int, str, str, list[str], str, str, str]] = {
    "client": (
        1,
        0,
        "orange",
        "src",
        ["KentikAPI", "client.py", "client_mixin.py"],
        "KentikAPI client",
        "The starting point. Reads the credentials, picks the transport, and mounts every wrapper.",
        "Expected: nothing in the SDK can be called.",
    ),
    "wrap": (
        1,
        1,
        "green",
        "proc",
        ["Service wrappers", "client.{service}", "one per service"],
        "Service wrappers",
        "Send each call to the REST function or to call_grpc(), for the transport in use.",
        "Expected: the client does not mount that service, on either transport.",
    ),
    "tr": (
        2,
        1,
        "violet",
        "proc",
        ["Transports", "transports/", "REST and gRPC"],
        "Transports",
        "RestTransport holds the APIConfig. GrpcTransport holds the TLS channel and the default deadline.",
        "Expected: the client cannot be built, on either transport.",
    ),
    "rest": (
        0,
        2,
        "green",
        "proc",
        ["REST functions", "gen/{service}/services/", "+ error classes"],
        "REST functions and error classes",
        "One function per operation. Each one calls request_json() with its own error class.",
        "Expected: REST calls fail for that service. gRPC calls through the same wrapper keep working.",
    ),
    "models": (
        1,
        2,
        "green",
        "proc",
        ["Models", "gen/{service}/models/", "Pydantic v2"],
        "Models",
        "The request and response models of every operation. They import nothing else in the SDK.",
        "Expected: the REST functions and the wrappers of that service do not import, so it does not mount.",
    ),
    "pb": (
        2,
        2,
        "green",
        "proc",
        ["Proto stubs", "gen/{service}/pb/", "protoc output"],
        "Proto stubs",
        "The modules that protoc compiles. Wrappers call them on a gRPC transport.",
        "Expected: gRPC calls for that service raise NotImplementedError. REST calls keep working.",
    ),
    "rj": (
        0,
        3,
        "neutral",
        "hub",
        ["request_json()", "core/rest_runtime.py", "all REST traffic"],
        "request_json()",
        "The one function that sends REST traffic: auth headers, quota, and errors.",
        "Expected: every REST call fails. gRPC calls fail too, because they parse responses with it.",
    ),
    "cg": (
        2,
        3,
        "neutral",
        "hub",
        ["call_grpc()", "core/grpc_runtime.py", "all gRPC traffic"],
        "call_grpc()",
        "The one function that sends gRPC traffic: deadline, quota, and errors.",
        "Expected: every gRPC call fails. REST calls keep working.",
    ),
    "base": (
        1,
        4,
        "neutral",
        "hub",
        ["Shared foundation", "APIConfig, auth,", "KentikError, RateLimit"],
        "Shared foundation",
        "APIConfig, the auth headers, the KentikError hierarchy and RateLimit. Every other part imports it.",
        "Expected: nothing in the SDK imports, so every call fails.",
    ),
}

# wire id: (path, importer>imported keys, label, label position, anchor, arrow)
_WIRES: list[tuple[str, str, list[str], str | None, tuple[int, int], str, bool]] = [
    (
        "client_wrap",
        "M430,102 V170",
        ["client>wrap"],
        "wrappers",
        (438, 140),
        "start",
        True,
    ),
    (
        "client_tr",
        "M530,66 H720 V170",
        ["client>tr"],
        "transports",
        (625, 58),
        "middle",
        True,
    ),
    ("wrap_tr", "M530,206 H620", ["wrap>tr"], "transport", (575, 198), "middle", True),
    (
        "wrap_rest",
        "M330,206 H140 V310",
        ["wrap>rest"],
        "REST functions",
        (235, 198),
        "middle",
        True,
    ),
    (
        "wrap_models",
        "M430,242 V310",
        ["wrap>models"],
        "models",
        (422, 290),
        "end",
        True,
    ),
    (
        "wrap_pb",
        "M510,242 V260 H690 V310",
        ["wrap>pb"],
        "proto stubs",
        (698, 290),
        "start",
        True,
    ),
    (
        "wrap_cg",
        "M480,242 V290 H575 V486 H620",
        ["wrap>cg"],
        "call_grpc()",
        (583, 400),
        "start",
        True,
    ),
    (
        "rest_models",
        "M240,346 H330",
        ["rest>models"],
        "models",
        (285, 338),
        "middle",
        True,
    ),
    (
        "rest_rj",
        "M140,382 V450",
        ["rest>rj"],
        "request_json()",
        (148, 420),
        "start",
        True,
    ),
    ("cg_rj", "M620,506 H240", ["cg>rj"], "parsing", (439, 498), "middle", True),
    (
        "rj_base",
        "M140,522 V626 H330",
        ["rj>base"],
        "APIConfig, auth",
        (148, 570),
        "start",
        True,
    ),
    (
        "cg_base",
        "M720,522 V610 H530",
        ["cg>base"],
        "APIConfig, errors",
        (728, 570),
        "start",
        True,
    ),
    (
        "tr_base",
        "M820,206 H860 V640 H530",
        ["tr>base"],
        "APIConfig, auth",
        (852, 420),
        "end",
        True,
    ),
]

# Real imports the explorer leaves out, so the figure stays readable.
_UNDRAWN = {"client>base", "client>rest", "wrap>base", "rest>base"}

_PATHS = {
    "rest": {
        "label": "REST call",
        "family": "blue",
        "title": "What a REST call uses",
        "text": "KentikAPI calls a wrapper. The wrapper calls the REST function, which builds the request "
        "with the models and sends it with request_json().",
        "links": ["client>wrap", "wrap>rest", "rest>models", "rest>rj", "rj>base"],
    },
    "grpc": {
        "label": "gRPC call",
        "family": "violet",
        "title": "What a gRPC call uses",
        "text": "KentikAPI calls a wrapper. The wrapper builds the proto request with the stubs and sends it "
        "with call_grpc(), which parses the answer into the same models as REST.",
        "links": [
            "client>wrap",
            "wrap>pb",
            "wrap>models",
            "wrap>cg",
            "cg>rj",
            "cg>base",
        ],
    },
    "setup": {
        "label": "Client setup",
        "family": "orange",
        "title": "What building the client uses",
        "text": "KentikAPI builds one transport from the APIConfig and gives it to every wrapper that it mounts.",
        "links": ["client>tr", "client>wrap", "wrap>tr", "tr>base"],
    },
}

_GROUP_ROLES: dict[str, str] = {
    "Client API": "`KentikAPI`: reads the credentials and selects the transport.",
    "Client Mixin": "Mounts each service wrapper as `client.<service>`.",
    "Generated Service Wrappers": "Send each call to the REST function or to the gRPC stub, for the transport in use.",
    "Generated REST Services": "One function per operation in the OpenAPI schema. Each function calls `request_json()`.",
    "Generated Models": "Pydantic request and response models.",
    "Generated Error Classes": "One error class per operation, picked by the response status.",
    "Generated Proto Stubs": "The modules that protoc compiles. Wrappers call them on a gRPC transport.",
    "API Config": "`APIConfig`: base URL, credentials, TLS, timeouts, and the shared HTTP client.",
    "REST Runtime": "`request_json()`: the one function that sends REST traffic.",
    "gRPC Runtime": "`call_grpc()`: the one function that sends gRPC traffic.",
    "Error Types": "The shared exception hierarchy under `KentikError`.",
    "Auth Credentials": "Builds the Kentik auth headers for REST and for gRPC.",
    "Rate Limit": "`RateLimit`: the quota that each response reports.",
    "Transport Base": "The base class of both transports.",
    "REST Transport": "`RestTransport`: holds the `APIConfig` for REST calls.",
    "gRPC Transport": "`GrpcTransport`: the TLS channel, with auth and the default deadline.",
}


def _operation_counts() -> tuple[int, int]:
    """The number of services with operations, and the number of operations."""
    services = 0
    operations = 0
    for service_dir in iter_service_dirs():
        ops = sum(
            len(parse_generated_rest_module(module))
            for module in (service_dir / "services").glob("*.py")
        )
        services += ops > 0
        operations += ops
    return services, operations


def _system_overview_explorer() -> list[str]:
    """The overview: your code down through the SDK to the two Kentik APIs."""
    services, operations = _operation_counts()
    p = "ov"
    L, C, R = 90, 390, 690
    rows = (30, 180, 330, 480, 630)
    w, h = 200, 72
    # part: (column, row, family, kind, box lines, title, role, facts, if it stops)
    parts = {
        "code": (
            C,
            0,
            "orange",
            "src",
            ["Your code", "import kentik_api"],
            "Your code",
            "Builds one KentikAPI client, then calls client.<service>.<method>().",
            [
                "Gets the same Pydantic model on REST and gRPC",
                "Catches one exception hierarchy, KentikError",
            ],
            "Nothing is sent.",
        ),
        "client": (
            R,
            1,
            "orange",
            "proc",
            ["KentikAPI", "client.py", "picks REST or gRPC"],
            "KentikAPI client",
            "Reads the credentials, builds one transport, and mounts every service wrapper on it.",
            [
                "Credentials: arguments, then KENTIK_EMAIL and KENTIK_API_TOKEN, then .env",
                "V5 services always use a second REST transport, to the V5 host",
            ],
            "Expected: no client can be built, so nothing in the SDK can be called.",
        ),
        "wrap": (
            C,
            1,
            "green",
            "proc",
            ["Service wrappers", "client.{service}", "one per service"],
            "Service wrappers",
            "One per service. Each method sends the call down the path of the client's transport.",
            [
                f"{services} services, {operations} operations",
                "The same signature and the same models on REST and gRPC",
            ],
            "Expected: the client does not mount that service, on either transport.",
        ),
        "rest": (
            L,
            2,
            "blue",
            "proc",
            ["REST functions", "gen/{service}/services/", "one per operation"],
            "REST functions",
            (
                "Build the path, the query and the body of one operation, and call request_json() "
                "with that operation's error class."
            ),
            ["Generated from the OpenAPI schema"],
            "Expected: REST calls to that service fail. A gRPC client keeps working.",
        ),
        "rj": (
            L,
            3,
            "blue",
            "proc",
            ["request_json()", "core/rest_runtime.py", "all REST traffic"],
            "request_json()",
            "The one function that sends REST traffic: auth headers, quota, and errors.",
            [
                "One pooled HTTP client for each APIConfig",
                "A 401 raises AuthenticationError",
            ],
            (
                "Expected: every REST call fails, V5 included. gRPC calls fail too, because they "
                "parse responses with it."
            ),
        ),
        "cg": (
            R,
            3,
            "violet",
            "proc",
            ["call_grpc()", "core/grpc_runtime.py", "all gRPC traffic"],
            "call_grpc()",
            "The one function that sends gRPC traffic: deadline, quota, and errors.",
            [
                "Every call carries a deadline",
                "map_grpc_error() turns each status into a KentikError",
            ],
            "Expected: every gRPC call fails. A REST client keeps working.",
        ),
        "restapi": (
            L,
            4,
            "blue",
            "src",
            ["Kentik REST API", "V6: grpc.api.kentik.com", "V5: api.kentik.com"],
            "Kentik REST API",
            "Kentik's HTTPS endpoints. A proxy turns each V6 request into a gRPC call.",
            [
                'region="eu" uses the .kentik.eu hosts',
                "Reports the quota of each endpoint in headers",
            ],
            (
                "Expected: REST calls raise TransportError or HTTPException. A gRPC client keeps "
                "working, except for V5."
            ),
        ),
        "grpcapi": (
            R,
            4,
            "violet",
            "src",
            ["Kentik gRPC API", "grpc.api.kentik.com:443", "TLS, HTTP/2"],
            "Kentik gRPC API",
            "Kentik's gRPC services, for V6 only.",
            ["The same services and the same quota as the V6 REST API"],
            "Expected: gRPC calls raise TransportError. A REST client keeps working.",
        ),
    }
    top = {pid: rows[part[1]] for pid, part in parts.items()}
    # Each hop is a call going down and its answer coming back up, 60 px apart.
    # wire id: (path, link, label, label position, anchor, kind)
    wires = [
        (
            "code_wrap",
            f"M{C + 70},102 V180",
            "code>wrap",
            "arguments",
            (C + 62, 145),
            "end",
            "call",
        ),
        (
            "wrap_code",
            f"M{C + 130},180 V102",
            "wrap>code",
            "Pydantic model",
            (C + 138, 145),
            "start",
            "data",
        ),
        (
            "code_client",
            f"M{C + w},66 H{R + 100} V180",
            "code>client",
            None,
            (0, 0),
            "middle",
            "data",
        ),
        (
            "client_wrap",
            f"M{R},216 H{C + w}",
            "client>wrap",
            "transport",
            ((R + C + w + 18) // 2, 208),
            "middle",
            "data",
        ),
        (
            "wrap_rest",
            f"M{C},196 H{L + 70} V330",
            "wrap>rest",
            "arguments",
            ((C + L + 70) // 2, 188),
            "middle",
            "call",
        ),
        (
            "rest_wrap",
            f"M{L + 130},330 V236 H{C}",
            "rest>wrap",
            "Pydantic model",
            ((L + 130 + C - 18) // 2, 228),
            "middle",
            "data",
        ),
        (
            "wrap_cg",
            f"M{C + 160},252 V296 H{R + 130} V480",
            "wrap>cg",
            "proto request",
            ((C + 160 + R + 130) // 2, 288),
            "middle",
            "call",
        ),
        (
            "cg_wrap",
            f"M{R + 70},480 V316 H{C + 120} V252",
            "cg>wrap",
            "proto response + quota",
            (R + 62, 436),
            "end",
            "data",
        ),
        (
            "rest_rj",
            f"M{L + 70},402 V480",
            "rest>rj",
            "method, path, body",
            (L + 62, 436),
            "end",
            "call",
        ),
        (
            "rj_rest",
            f"M{L + 130},480 V402",
            "rj>rest",
            "JSON dict + quota",
            (L + 138, 436),
            "start",
            "data",
        ),
        (
            "rj_api",
            f"M{L + 70},552 V630",
            "rj>restapi",
            "HTTPS + auth headers",
            (L + 62, 586),
            "end",
            "call",
        ),
        (
            "api_rj",
            f"M{L + 130},630 V552",
            "restapi>rj",
            "JSON + quota headers",
            (L + 138, 586),
            "start",
            "data",
        ),
        (
            "cg_api",
            f"M{R + 70},552 V630",
            "cg>grpcapi",
            "gRPC call over TLS",
            (R + 62, 586),
            "end",
            "call",
        ),
        (
            "api_cg",
            f"M{R + 130},630 V552",
            "grpcapi>cg",
            "proto response",
            (R + 138, 586),
            "start",
            "data",
        ),
    ]
    containers = [
        (
            (L - 20, 146, C + w + 20 - (L - 20), 272),
            "Generated: gen/, rebuilt on every run",
        ),
        ((L - 20, 446, R + w + 20 - (L - 20), 122), "Hand-written runtime: core/"),
        ((L - 20, 596, R + w + 20 - (L - 20), 122), "Kentik, outside the SDK"),
    ]
    body = (
        [dk.container(box, label) for box, label in containers]
        + [
            dk.seg(sid, d, [key], p, label, at, anchor=anchor, kind=kind)
            for sid, d, key, label, at, anchor, kind in wires
        ]
        + [
            dk.node(pid, (x, top[pid], w, h), fam, kind, lines, label=title)
            for pid, (x, _, fam, kind, lines, title, *_) in parts.items()
        ]
    )
    markup = dk.svg(
        "overview-svg",
        (R + w + 60, 740),
        "SDK overview: your code calls a generated service wrapper. On REST, the wrapper calls a "
        "generated REST function and request_json(), which calls the Kentik REST API. On gRPC, it "
        "calls call_grpc(), which calls the Kentik gRPC API. Each answer comes back as a Pydantic model.",
        "".join(body),
        p,
    )
    rest_path = [
        "code>wrap",
        "wrap>rest",
        "rest>rj",
        "rj>restapi",
        "restapi>rj",
        "rj>rest",
        "rest>wrap",
        "wrap>code",
    ]
    grpc_path = [
        "code>wrap",
        "wrap>cg",
        "cg>grpcapi",
        "grpcapi>cg",
        "cg>wrap",
        "wrap>code",
    ]
    data = {
        "select": "wrap",
        "parts": {
            pid: {"title": title, "role": role, "facts": facts, "stops": stops}
            for pid, (*_, title, role, facts, stops) in parts.items()
        },
        "paths": {
            "rest": {
                "label": "REST call",
                "family": "blue",
                "title": "A call on a REST client",
                "text": "The wrapper calls the REST function, which sends the request with request_json(). "
                "V5 services always take this path.",
                "links": rest_path,
            },
            "grpc": {
                "label": "gRPC call",
                "family": "violet",
                "title": "A call on a gRPC client",
                "text": "The wrapper builds the proto request and sends it with call_grpc(), then parses the "
                "answer into the same model as REST.",
                "links": grpc_path,
            },
            "setup": {
                "label": "Client setup",
                "family": "orange",
                "title": "Building the client",
                "text": "KentikAPI builds one transport and gives it to every wrapper that it mounts.",
                "links": ["code>client", "client>wrap"],
            },
        },
    }
    return fragment(
        markup,
        data,
        "Start at your code at the top. Each hop is a call going down and its answer coming back up. "
        "Select a part to see what it needs and what stops without it.",
    )


def _call_path_diagram() -> list[str]:
    """The overview: one REST row and one gRPC row from the caller to the Kentik API."""
    services, operations = _operation_counts()

    return [
        "```mermaid",
        mermaid_init(),
        "sequenceDiagram",
        "    actor C as Your code",
        (
            '    participant W@{ "type": "boundary" } as Service wrapper<br/>'
            f"({services} services, {operations} operations)"
        ),
        "    box transparent REST transport",
        '    participant R@{ "type": "control" } as REST function<br/>gen/{service}/services/',
        '    participant RJ@{ "type": "control" } as request_json()',
        "    participant RA as Kentik REST API",
        "    end",
        "    box transparent gRPC transport",
        '    participant CG@{ "type": "control" } as call_grpc()',
        "    participant GA as Kentik gRPC API",
        "    end",
        "",
        "    C->>+W: client.{service}.{method}(arguments)",
        "    alt REST transport",
        "        W->>+R: arguments",
        f"        rect {_SHARED_RUNTIME_BAND}",
        "        Note over RJ,RA: Shared runtime:<br/>every REST endpoint<br/>goes through request_json()",
        "        R->>+RJ: method, path, body, APIConfig",
        "        RJ->>+RA: HTTPS request with auth headers",
        "        RA-->>-RJ: JSON response",
        "        RJ-->>-R: JSON dict + quota",
        "        end",
        "        R-->>-W: Pydantic model",
        "    else gRPC transport",
        f"        rect {_SHARED_RUNTIME_BAND}",
        "        Note over CG,GA: Shared runtime:<br/>every gRPC endpoint<br/>goes through call_grpc()",
        "        W->>+CG: stub method + proto request",
        "        CG->>+GA: gRPC call over TLS",
        "        GA-->>-CG: proto response",
        "        CG-->>-W: proto response + quota",
        "        end",
        "        W->>W: parse_grpc_response()",
        "    end",
        "    W-->>-C: Pydantic model",
        "    Note over C,GA: On a failure, request_json() or call_grpc() raises a KentikError subclass.",
        "```",
    ]


def _dependency_explorer(edge_counts: dict[tuple[str, str], int]) -> list[str]:
    """The Module Dependencies explorer: from KentikAPI at the top down to the shared foundation."""
    part_of = {group: part for part, groups in _PART_GROUPS.items() for group in groups}
    imports: dict[str, int] = {}
    for (importer, imported), count in edge_counts.items():
        user, used = part_of.get(importer), part_of.get(imported)
        if user and used and user != used:
            key = f"{user}>{used}"
            imports[key] = imports.get(key, 0) + count

    drawn = {key for _, _, keys, *_ in _WIRES for key in keys}
    if missing := sorted(drawn - imports.keys()):
        raise ValueError(
            f"the dependency explorer draws imports that do not exist: {missing}"
        )
    if left_out := sorted(imports.keys() - drawn - _UNDRAWN):
        print(
            f"    \u26a0\ufe0f  The dependency explorer does not draw: {', '.join(left_out)}"
        )

    def counted(keys: list[str], index: int) -> list[str]:
        return [
            f"{_PARTS[key.split('>')[index]][5]} ({imports[key]})"
            for key in sorted(keys)
        ]

    parts = {}
    for pid, (*_, title, role, stops) in _PARTS.items():
        sources = ", ".join(_GROUP_CONFIG[g][1] for g in _PART_GROUPS[pid])
        facts = [f"Source: {sources}"]
        if uses := counted([k for k in imports if k.startswith(f"{pid}>")], 1):
            facts.append("Imports " + ", ".join(uses))
        if users := counted([k for k in imports if k.endswith(f">{pid}")], 0):
            facts.append("Imported by " + ", ".join(users))
        parts[pid] = {"title": title, "role": role, "facts": facts, "stops": stops}

    prefix = "deps"
    wires = [
        dk.seg(sid, d, keys, prefix, label, at, anchor=anchor, arrow=arrow)
        for sid, d, keys, label, at, anchor, arrow in _WIRES
    ]
    boxes = [
        dk.node(pid, (_COLS[col], _ROWS[row], _W, _H), fam, kind, lines, label=title)
        for pid, (col, row, fam, kind, lines, title, _, _) in _PARTS.items()
    ]
    markup = dk.svg(
        "deps-svg",
        (900, 690),
        "Module dependencies: KentikAPI at the top imports the service wrappers and the transports. "
        "They import the runtimes, the models and the proto stubs, down to the shared foundation.",
        # The right channel of the transport wire makes the grid off center by 20 px.
        '<g transform="translate(20,0)">' + "".join(wires + boxes) + "</g>",
        prefix,
    )
    data = {
        "select": "client",
        "parts": parts,
        "links": {key: f"{imports[key]} import statements" for key in sorted(drawn)},
        "paths": _PATHS,
        "words": {"from": "Used by", "to": "Uses"},
    }
    return fragment(
        markup,
        data,
        "Start at KentikAPI at the top. Each arrow points from a part to a part that it imports. Select a "
        "part: moving lines show what it uses, and bold lines show what uses it. Every part also imports "
        "the shared foundation, but the diagram draws that only for the runtimes and the transports.",
        legend=("what uses the selected part", "what the selected part uses"),
    )


def _module_group(module_name: str, source_file: Path | None = None) -> str | None:
    if module_name == "kentik_api.client":
        return "Client API"
    if module_name == "kentik_api.client_mixin":
        return "Client Mixin"
    if module_name.startswith("kentik_api.auth"):
        return "Auth Credentials"
    if module_name.startswith("kentik_api.core.api_config"):
        return "API Config"
    if module_name.startswith("kentik_api.core.rest_runtime"):
        return "REST Runtime"
    if module_name.startswith("kentik_api.core.grpc_runtime"):
        return "gRPC Runtime"
    if module_name.startswith("kentik_api.core.rate_limit"):
        return "Rate Limit"
    if module_name.startswith("kentik_api.errors"):
        return "Error Types"
    if module_name.startswith("kentik_api.transports.base"):
        return "Transport Base"
    if module_name.startswith("kentik_api.transports.rest_client"):
        return "REST Transport"
    if module_name.startswith("kentik_api.transports.grpc_client"):
        return "gRPC Transport"

    if module_name.startswith("kentik_api.gen."):
        if ".pb." in module_name:
            return "Generated Proto Stubs"
        if ".error" in module_name:
            return "Generated Error Classes"
        if ".services." in module_name:
            if source_file is not None and source_file.name[:1].islower():
                return "Generated Service Wrappers"
            tail = module_name.rsplit(".", maxsplit=1)[-1]
            if tail and tail[0].islower():
                return "Generated Service Wrappers"
            return "Generated REST Services"
        if ".models" in module_name:
            return "Generated Models"

    return None


def _generate_runtime_architecture_docs(
    rest_only: frozenset[str] = frozenset(),
) -> None:
    """Generates a high-level runtime architecture page with an inline dependency graph."""
    package_root = PROJECT_ROOT / "src" / "kentik_api"
    docs_root = PROJECT_ROOT / "docs" / "sphinx"

    scan_paths: list[Path] = []
    scan_paths.extend([package_root / "client.py", package_root / "client_mixin.py"])
    for rel in ("auth", "core", "errors", "transports"):
        root = package_root / rel
        if root.exists():
            scan_paths.extend(sorted(root.rglob("*.py")))

    gen_root = package_root / "gen"
    if gen_root.exists():
        for service_dir in sorted([p for p in gen_root.iterdir() if p.is_dir()]):
            for folder in ("services", "service"):
                sf = service_dir / folder
                if sf.exists():
                    scan_paths.extend(sorted(sf.glob("*.py")))
            err_file = service_dir / "error" / "__init__.py"
            if err_file.exists():
                scan_paths.append(err_file)

    edge_counts: dict[tuple[str, str], int] = {}
    nodes: set[str] = set()

    for py_file in scan_paths:
        if not py_file.exists() or (
            py_file.name == "__init__.py" and py_file.parent.name != "error"
        ):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except OSError:
            continue

        current_module = _module_name_from_path(py_file, package_root)
        src_group = _module_group(current_module, source_file=py_file)
        if src_group is None:
            continue
        nodes.add(src_group)

        for node in ast.walk(tree):
            target_modules: list[str] = []
            if isinstance(node, ast.Import):
                target_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = _resolve_import_from(current_module, node.level, node.module)
                target_modules.append(base)
                target_modules.extend(f"{base}.{alias.name}" for alias in node.names)

            dst_groups = {
                _module_group(target_module)
                for target_module in target_modules
                if target_module.startswith("kentik_api")
            }
            for dst_group in dst_groups:
                if dst_group is None or dst_group == src_group:
                    continue
                nodes.add(dst_group)
                key = (src_group, dst_group)
                edge_counts[key] = edge_counts.get(key, 0) + 1

    imports_of: dict[str, list[str]] = {}
    for (src, dst), count in sorted(edge_counts.items()):
        imports_of.setdefault(src, []).append(f"{dst} ({count})")

    group_rows = [
        f"| {label} | {_LAYER_NAMES[layer]} | `{path}` | "
        f"{', '.join(imports_of.get(label, [])) or 'nothing in the SDK'} | "
        f"{_GROUP_ROLES.get(label, '')} |"
        for label, (layer, path) in _GROUP_CONFIG.items()
        if label in nodes
    ]

    architecture_md = [
        "---",
        "html_theme.sidebar_secondary.remove: true",
        "---",
        "",
        "<!-- AUTO-GENERATED: scripts/generation/docs_rendering.py, _generate_runtime_architecture_docs() -->",
        f"<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->",
        "",
        "# SDK Runtime Architecture",
        "",
        "This page shows how a call moves through the SDK, and how the hand-written",
        "runtime modules and the generated services depend on each other.",
        "",
        "## Overview",
        "",
        "Your code calls one generated wrapper per service. The transport of the client",
        "selects the path below the wrapper: REST through `request_json()`, or gRPC",
        "through `call_grpc()`. Each path ends at a Kentik API.",
        "",
        *_system_overview_explorer(),
        "",
        "## Call Path",
        "",
        "Each method call on `client.<service>` takes one of two paths. The transport",
        "that the client uses selects the path. Both paths return the same Pydantic",
        "models and raise the same exception types.",
        "",
        *_call_path_diagram(),
        "",
        "1. `kentik_api.client.KentikAPI` reads the credentials and selects the transport.",
        "2. `kentik_api.client_mixin.KentikClientMixin` mounts one generated service",
        "   wrapper per service.",
        "3. On a REST transport, a wrapper calls the generated REST function in",
        "   `kentik_api.gen.<service>.services`. That function calls `request_json()`",
        "   in `kentik_api.core.rest_runtime`, with the shared `APIConfig`.",
        "4. On a gRPC transport, a wrapper calls `call_grpc()` in",
        "   `kentik_api.core.grpc_runtime`, with the compiled proto stubs in",
        "   `kentik_api.gen.<service>.pb`.",
        "5. Both runtimes turn each failure into a `kentik_api.errors` type, or into",
        "   the error class that the service generates for that operation.",
        "",
        "## Module Dependencies",
        "",
        "The SDK splits into the parts below. Select one to see what it imports and what",
        "imports it. The generator reads the imports from the source on every run.",
        "",
        *_dependency_explorer(edge_counts),
        "",
        "The table lists each module group, and the groups that it imports, with the",
        "number of import statements.",
        "",
        "| Group | Layer | Source | Imports from | Role |",
        "| --- | --- | --- | --- | --- |",
        *group_rows,
        "",
        *_services_without_wrappers_section(),
        *_rest_only_services_section(rest_only),
    ]
    write_text_lf(docs_root / "sdk_runtime_architecture.md", "\n".join(architecture_md))

    index_path = docs_root / "index.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        if "sdk_runtime_architecture" not in index_text:
            marker = "local_generation_workflow\n"
            if marker in index_text:
                index_text = index_text.replace(
                    marker, marker + "sdk_runtime_architecture\n", 1
                )
            else:
                index_text += "\nsdk_runtime_architecture\n"
            write_text_lf(index_path, index_text)


def _grpc_stub_method_name(wrapper_file: Path, method_name: str) -> str | None:
    """Reads the real gRPC stub method a wrapper method calls, e.g. "ListASGroups".

    Parsed off the generated `call_grpc(self._grpc_stub_N.<Name>, _req)` call
    rather than re-derived from the snake_case method name: re-deriving loses
    acronym casing (`list_as_groups` -> `ListAsGroups`, not `ListASGroups`).
    """
    try:
        tree = ast.parse(
            wrapper_file.read_text(encoding="utf-8"), filename=str(wrapper_file)
        )
    except OSError:
        return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != method_name:
            continue
        for sub in ast.walk(node):
            if (
                isinstance(sub, ast.Call)
                and isinstance(sub.func, ast.Name)
                and sub.func.id == "call_grpc"
                and sub.args
                and isinstance(sub.args[0], ast.Attribute)
            ):
                return sub.args[0].attr
    return None


def _strip_optional(type_str: str) -> str:
    optional_match = re.match(r"^Optional\[(.+)\]$", type_str)
    return optional_match.group(1) if optional_match else type_str


def _model_has_only_optional_fields(model_file: Path) -> bool:
    """True if every field on the model class has a Field(..., default=...).

    Lets _discover_example_ops() pick a request model that RequestClass()
    alone can construct, so the generated example snippet actually runs.
    """
    try:
        tree = ast.parse(
            model_file.read_text(encoding="utf-8"), filename=str(model_file)
        )
    except OSError:
        return False

    model_class = next(
        (node for node in tree.body if isinstance(node, ast.ClassDef)), None
    )
    if model_class is None:
        return False

    for node in model_class.body:
        if not isinstance(node, ast.AnnAssign):
            continue
        if not isinstance(node.value, ast.Call):
            return False  # a field with no Field(...) call has no default
        if not any(kw.arg == "default" for kw in node.value.keywords):
            return False

    return True


def _discover_example_ops(
    max_list_ops: int = 3,
) -> tuple[list[dict[str, str]], dict[str, str] | None]:
    """Scans generated *ServiceWrapper files to find representative operations.

    Returns (list_ops, body_op).
    list_ops: up to max_list_ops `list` or list_* operations, each {service, method, response_class}.
    body_op: first operation with a data: parameter, {service, method, request_class}.

    Both are chosen to be directly callable with no arguments, so the
    generated example snippets actually run: list_ops only includes `list` and list_*
    methods with zero required parameters, and body_op only includes a
    data-param operation whose request model has zero required fields
    (RequestClass() alone constructs successfully).
    """
    list_ops: list[dict[str, str]] = []
    body_op: dict[str, str] | None = None

    if not SDK_OUTPUT_DIR.exists():
        return list_ops, body_op

    for service_dir in iter_service_dirs():
        service_name = service_dir.name
        services_folder = service_dir / "services"
        if not services_folder.exists():
            continue

        for wrapper_file in sorted(services_folder.glob("*.py")):
            if wrapper_file.name == "__init__.py":
                continue

            for method in parse_wrapper_methods(wrapper_file):
                if (
                    len(list_ops) < max_list_ops
                    and re.match(r"list(_|$)", method.name.lower())
                    and method.return_type
                    and all(not is_required for _, _, is_required in method.params)
                ):
                    raw = _strip_optional(method.return_type)
                    response_class = raw.rsplit(".", 1)[-1]
                    if response_class:
                        list_ops.append(
                            {
                                "service": service_name,
                                "method": method.name,
                                "response_class": response_class,
                                "wrapper_file": str(wrapper_file),
                            }
                        )

                if body_op is None and method.has_data_param:
                    for param_name, annotation, _ in method.params:
                        if param_name == "data" and annotation:
                            raw = _strip_optional(annotation)
                            request_class = raw.rsplit(".", 1)[-1]
                            model_file = service_dir / "models" / f"{request_class}.py"
                            if model_file.exists() and _model_has_only_optional_fields(
                                model_file
                            ):
                                body_op = {
                                    "service": service_name,
                                    "method": method.name,
                                    "request_class": request_class,
                                }
                            break

        if len(list_ops) >= max_list_ops and body_op is not None:
            break

    return list_ops, body_op


def _replace_marker(text: str, marker: str, new_content: str) -> str:
    """Replaces content inside <!-- kentik-gen:MARKER --> / <!-- /kentik-gen:MARKER --> tags."""
    pattern = re.compile(
        r"<!-- kentik-gen:" + re.escape(marker) + r" -->"
        r".*?"
        r"<!-- /kentik-gen:" + re.escape(marker) + r" -->",
        re.DOTALL,
    )
    replacement = (
        f"<!-- kentik-gen:{marker} -->" + new_content + f"<!-- /kentik-gen:{marker} -->"
    )
    return pattern.sub(replacement, text)


def _transport_paths_explorer() -> list[str]:
    """The REST vs gRPC guide's explorer: both clients reach the same gRPC services."""
    p = "tp"
    # part: (box, family, kind, lines, title, role, facts, if it stops)
    parts = {
        "code": (
            (450, 30),
            "green",
            "src",
            ["Your code", "same methods"],
            "Your code",
            "Calls the same service methods on either client.",
            ["Both clients return the same Pydantic models"],
            "Nothing is sent.",
        ),
        "restc": (
            (160, 170),
            "blue",
            "proc",
            ['protocol="rest"', "HTTPS + JSON"],
            'KentikAPI(protocol="rest")',
            "Sends each call as an HTTPS request with a JSON body.",
            ["HTTP/1.1", "Every operation, V5 included"],
            "Expected: REST calls stop. A gRPC client keeps working.",
        ),
        "grpcc": (
            (740, 170),
            "violet",
            "proc",
            ['protocol="grpc"', "HTTP/2 + protobuf"],
            'KentikAPI(protocol="grpc")',
            "Sends each call as a gRPC call with a protobuf body.",
            ["HTTP/2", "Every V6 operation. V5 calls go over REST"],
            "Expected: gRPC calls stop. A REST client keeps working.",
        ),
        "envoy": (
            (160, 310),
            "blue",
            "proc",
            ["Envoy transcoder", "JSON to gRPC and back"],
            "Envoy transcoder",
            "Converts each REST request into a gRPC call, and the answer back into JSON.",
            [
                "Answers with the header server: envoy",
                "Copies the gRPC status into grpc-status",
            ],
            "Expected: REST calls fail. gRPC calls keep working.",
        ),
        "svc": (
            (450, 450),
            "neutral",
            "hub",
            ["Kentik gRPC services", "one quota per endpoint"],
            "Kentik gRPC services",
            "The services behind both transports.",
            [
                "60 requests per 60 seconds for each endpoint",
                "REST and gRPC take from the same quota",
            ],
            "Expected: both transports fail.",
        ),
    }
    # wire id: (path, link, label, label position, anchor, kind)
    wires = [
        (
            "code_rest",
            "M450,56 H230 V170",
            "code>restc",
            "method call",
            (340, 48),
            "middle",
            "call",
        ),
        (
            "rest_code",
            "M290,170 V86 H450",
            "restc>code",
            "Pydantic model",
            (298, 130),
            "start",
            "data",
        ),
        (
            "code_grpc",
            "M650,56 H870 V170",
            "code>grpcc",
            "method call",
            (760, 48),
            "middle",
            "call",
        ),
        (
            "grpc_code",
            "M810,170 V86 H650",
            "grpcc>code",
            "Pydantic model",
            (802, 130),
            "end",
            "data",
        ),
        (
            "rest_envoy",
            "M230,242 V310",
            "restc>envoy",
            "HTTPS + JSON",
            (222, 280),
            "end",
            "call",
        ),
        (
            "envoy_rest",
            "M290,310 V242",
            "envoy>restc",
            "JSON",
            (298, 280),
            "start",
            "data",
        ),
        (
            "envoy_svc",
            "M290,382 V476 H450",
            "envoy>svc",
            "gRPC call",
            (361, 468),
            "middle",
            "call",
        ),
        (
            "svc_envoy",
            "M450,506 H230 V382",
            "svc>envoy",
            "gRPC response",
            (340, 524),
            "middle",
            "data",
        ),
        (
            "grpc_svc",
            "M810,242 V476 H650",
            "grpcc>svc",
            "gRPC call",
            (802, 420),
            "end",
            "call",
        ),
        (
            "svc_grpc",
            "M650,506 H870 V242",
            "svc>grpcc",
            "gRPC response",
            (878, 420),
            "start",
            "data",
        ),
    ]
    segs = [
        dk.seg(sid, d, [key], p, label, at, anchor=anchor, kind=kind)
        for sid, d, key, label, at, anchor, kind in wires
    ]
    boxes = [
        dk.node(pid, (x, y, 200, 72), fam, kind, lines, label=title)
        for pid, ((x, y), fam, kind, lines, title, *_) in parts.items()
    ]
    markup = dk.svg(
        "transports-svg",
        (1100, 560),
        "Both clients reach the same Kentik gRPC services: REST through the Envoy transcoder, gRPC directly.",
        "".join(segs + boxes),
        p,
    )
    data = {
        "select": "svc",
        "parts": {
            pid: {"title": title, "role": role, "facts": facts, "stops": stops}
            for pid, (*_, title, role, facts, stops) in parts.items()
        },
        "paths": {
            "rest": {
                "label": "REST",
                "family": "blue",
                "title": "A REST call",
                "text": "Envoy converts the request into a gRPC call and the answer back into JSON.",
                "links": [
                    "code>restc",
                    "restc>envoy",
                    "envoy>svc",
                    "svc>envoy",
                    "envoy>restc",
                    "restc>code",
                ],
            },
            "grpc": {
                "label": "gRPC",
                "family": "violet",
                "title": "A gRPC call",
                "text": "The gRPC client calls the services directly.",
                "links": ["code>grpcc", "grpcc>svc", "svc>grpcc", "grpcc>code"],
            },
        },
    }
    return fragment(
        markup,
        data,
        "Select a part. Each hop is a call going down and its answer coming back up. "
        "Both paths end at the same services, so both take from the same quota.",
    )


def _update_guide_snippets() -> None:
    """Injects current generated operation names and counts into docs/sphinx/guides/ marker blocks."""
    if not SDK_OUTPUT_DIR.exists():
        return

    service_count = len(iter_service_dirs())

    list_ops, body_op = _discover_example_ops(max_list_ops=3)
    if not list_ops:
        print("    ⚠️  No list operations found; skipping guide snippet updates.")
        return

    primary = list_ops[0]
    stub_method = (
        _grpc_stub_method_name(Path(primary["wrapper_file"]), primary["method"])
        or primary["method"]
    )
    request_proto = primary["response_class"].replace("Response", "Request")

    gen_md = _GUIDES_DIR / "generation.md"
    if gen_md.exists():
        text = gen_md.read_text(encoding="utf-8")
        text = _replace_marker(text, "service-count", str(service_count))
        write_text_lf(gen_md, text)

    transports_md = _GUIDES_DIR / "rest-vs-grpc.md"
    if transports_md.exists():
        text = transports_md.read_text(encoding="utf-8")
        explorer = "\n".join(_transport_paths_explorer())
        text = _replace_marker(text, "transport-paths-explorer", f"\n{explorer}\n")
        write_text_lf(transports_md, text)

    sphinx_readme = PROJECT_ROOT / "docs" / "sphinx" / "README.md"
    if sphinx_readme.exists():
        text = sphinx_readme.read_text(encoding="utf-8")
        text = _replace_marker(text, "service-count", str(service_count))
        write_text_lf(sphinx_readme, text)

    qs_md = _GUIDES_DIR / "quickstart.md"
    if qs_md.exists():
        text = qs_md.read_text(encoding="utf-8")
        text = _replace_marker(
            text,
            "first-call-example",
            f"""
```python
from kentik_api.client import KentikAPI

client = KentikAPI(protocol="rest")
response = client.{primary["service"]}.{primary["method"]}()
print(response)  # {primary["response_class"]}
```
""",
        )
        text = _replace_marker(
            text,
            "grpc-call-example",
            f"""
```python
client = KentikAPI(protocol="grpc")
response = client.{primary["service"]}.{primary["method"]}()  # same API, same response models
```
""",
        )
        write_text_lf(qs_md, text)

    rest_md = _GUIDES_DIR / "rest.md"
    if rest_md.exists():
        text = rest_md.read_text(encoding="utf-8")
        list_lines = "\n".join(
            f"response = client.{op['service']}.{op['method']}()" for op in list_ops
        )
        text = _replace_marker(
            text,
            "list-methods-example",
            f"""
```python
{list_lines}
```
""",
        )
        if body_op:
            text = _replace_marker(
                text,
                "request-body-example",
                f"""
```python
from kentik_api.gen.{body_op["service"]}.models import {body_op["request_class"]}

response = client.{body_op["service"]}.{body_op["method"]}(data={body_op["request_class"]}())
```
""",
            )
        write_text_lf(rest_md, text)

    grpc_md = _GUIDES_DIR / "grpc.md"
    if grpc_md.exists():
        text = grpc_md.read_text(encoding="utf-8")
        text = _replace_marker(
            text,
            "grpc-usage-example",
            f"""
```python
from kentik_api.client import KentikAPI

client = KentikAPI(protocol="grpc")
response = client.{primary["service"]}.{primary["method"]}()
print(response)  # {primary["response_class"]}
```
""",
        )
        text = _replace_marker(
            text,
            "rest-callflow-diagram",
            f"""
```mermaid
{mermaid_init()}
sequenceDiagram
    actor C as Caller
    participant W@{{ "type": "boundary" }} as ServiceWrapper
    participant RJ@{{ "type": "control" }} as request_json()
    participant API as Kentik REST API

    C->>+W: {primary["method"]}()
    W->>+RJ: api_config, method, path, params
    RJ->>+API: HTTP request (HTTPS)
    alt success
        API-->>RJ: JSON response
        RJ-->>W: parsed dict
        W-->>C: {primary["response_class"]} (Pydantic)
    else 401
        API-->>RJ: error JSON
        RJ-->>C: raise AuthenticationError
    else other error status
        API-->>RJ: error JSON
        RJ-->>C: raise the operation's HTTPException subclass
    else no response (unreachable or timed out)
        RJ-->>C: raise TransportError
    end
    deactivate API
    deactivate RJ
    deactivate W
```
""",
        )
        text = _replace_marker(
            text,
            "grpc-callflow-diagram",
            f"""
```mermaid
{mermaid_init()}
sequenceDiagram
    actor C as Caller
    participant W@{{ "type": "boundary" }} as ServiceWrapper
    participant CG@{{ "type": "control" }} as call_grpc()
    participant S@{{ "type": "control" }} as gRPC stub
    participant API as Kentik gRPC API

    C->>+W: {primary["method"]}()
    W->>W: build {request_proto} proto<br/>(ParseDict for operations with a body)
    W->>+CG: stub method + proto request
    CG->>+S: {stub_method} (gRPC/TLS, deadline set by the channel)
    S->>+API: serialized proto request
    alt success
        API-->>S: serialized proto response
        S-->>CG: {primary["response_class"]} proto
        CG-->>W: proto response and quota
        W-->>C: {primary["response_class"]} (Pydantic)<br/>via parse_grpc_response(), the same check as REST
    else gRPC error, deadline, or unreachable
        S-->>CG: raise RpcError
        CG-->>C: map_grpc_error(): AuthenticationError,<br/>the operation's HTTPException subclass, or TransportError
    end
    deactivate API
    deactivate S
    deactivate CG
    deactivate W
```
""",
        )
        write_text_lf(grpc_md, text)

    body_label = f"{body_op['service']}.{body_op['method']}" if body_op else "none"
    print(
        f"    ✅ Guide snippets updated "
        f"({service_count} services, list: {primary['service']}.{primary['method']}, "
        f"body: {body_label})."
    )


def generate(rest_only: frozenset[str] = frozenset()) -> None:
    """Generates the runtime architecture docs, the gen/ root README, and per-service READMEs."""
    _generate_runtime_architecture_docs(rest_only)
    _generate_gen_root_readme()
    _generate_service_readmes(rest_only)
    _update_guide_snippets()
    write_static_assets(PROJECT_ROOT / "docs" / "sphinx" / "_static")
