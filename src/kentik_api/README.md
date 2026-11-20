<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../pyproject.toml). Edit directly. -->

# `kentik_api` Package

The top-level package for the Kentik Community Python SDK. See the
repository root [README.md](../../README.md) for installation and
usage, and [AGENTS.md](../../AGENTS.md) for the full
hand-written-vs-generated architecture.

## Layout

| Path | Role |
| --- | --- |
| [`client.py`](client.py) | Hand-written. `KentikAPI`, the SDK's entrypoint: loads credentials, picks a transport, mounts every generated service. |
| [`client_mixin.py`](client_mixin.py) | Generated. Mounts every service wrapper onto `KentikAPI` as a typed attribute (`client.device`, `client.user`, and so on). |
| [`auth/`](auth/README.md) | Hand-written. See [auth/README.md](auth/README.md). |
| [`core/`](core/README.md) | Hand-written. The shared REST and gRPC runtimes every generated call routes through. See [core/README.md](core/README.md). |
| [`errors/`](errors/README.md) | Hand-written. The base exception hierarchy every generated error class builds on. See [errors/README.md](errors/README.md). |
| [`transports/`](transports/README.md) | Hand-written. REST/gRPC transport selection. See [transports/README.md](transports/README.md). |
| [`gen/`](gen/README.md) | Fully generated, one directory per Kentik API service. See [gen/README.md](gen/README.md). |

## Request flow

The diagram below shows what connects to what for one API call, from
`KentikAPI()` to the Kentik API or a raised error. Each call returns a
Pydantic model up the same path. Select a box to open its source.

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "dagre", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
flowchart TD
  kapi("KentikAPI()<br/>credentials: args, env vars, .env<br/>picks REST or gRPC"):::orangeSrc
  cfg("APIConfig<br/>host, credentials, timeouts"):::orange
  wrap("Service wrapper<br/>client.{service}<br/><small>mounted by client_mixin.py</small>"):::green
  rj("request_json()<br/>core/rest_runtime.py"):::blue
  cg("call_grpc()<br/>core/grpc_runtime.py"):::violet
  restApi("Kentik REST API"):::blueSrc
  grpcApi("Kentik gRPC API"):::violetSrc
  err("Raised errors<br/>KentikError subclasses<br/>gen/{service}/error/ classes"):::red

  kapi -->|"builds"| cfg
  cfg -->|"one transport"| wrap
  wrap -->|"REST client"| rj
  wrap -->|"gRPC client"| cg
  rj -->|"HTTPS + auth headers"| restApi
  cg -->|"gRPC over TLS"| grpcApi
  rj -->|"failure"| err
  cg -->|"failure"| err

  click kapi "client.py"
  click cfg "core/api_config.py"
  click wrap "gen/README.md"
  click rj "core/rest_runtime.py"
  click cg "core/grpc_runtime.py"
  click err "errors/README.md"

  classDef orangeSrc fill:#ffd8a8,stroke:#e8590c,color:#d9480f
  classDef orange fill:#fff4e6,stroke:#e8590c,color:#d9480f
  classDef green fill:#ebfbee,stroke:#2f9e44,color:#2b8a3e
  classDef blueSrc fill:#a5d8ff,stroke:#1971c2,color:#1864ab
  classDef blue fill:#e7f5ff,stroke:#1971c2,color:#1864ab
  classDef violetSrc fill:#d0bfff,stroke:#7048e8,color:#5f3dc4
  classDef violet fill:#f3f0ff,stroke:#7048e8,color:#5f3dc4
  classDef red fill:#fff5f5,stroke:#e03131,color:#c92a2a
  classDef orangeSrc,orange,green,blueSrc,blue stroke-width:2px,rx:10px
  classDef violetSrc,violet,red stroke-width:2px,rx:10px
  linkStyle default stroke-width:2px,stroke-linecap:round,stroke-linejoin:round
```

Every generated REST operation, in every service, calls
[`core/rest_runtime.py`](core/rest_runtime.py) the same way, and every gRPC
operation calls [`core/grpc_runtime.py`](core/grpc_runtime.py) the same way. No
service wrapper implements its own HTTP, auth, or error-parsing logic.

## Using the client

```python
from kentik_api.client import KentikAPI

# KENTIK_EMAIL/KENTIK_API_TOKEN from the environment or .env
client = KentikAPI(protocol="rest")
devices = client.device.list()
```

`KentikAPI` never implements per-service logic itself. It wires
together the hand-written pieces above with whatever [`gen/`](gen/README.md) produces,
so extending SDK behavior always means changing one of those pieces,
never `client.py` itself.
