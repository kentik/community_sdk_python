<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../../pyproject.toml). Edit directly. -->

# Credentials (`kentik_api.auth`)

This module is hand-written. [`uv run poe generate`](../../../pyproject.toml) does not touch it.

This module is the one definition of Kentik's auth scheme: the
`X-CH-Auth-Email` and `X-CH-Auth-API-Token` keys. REST sends them as
headers and gRPC as call metadata (lowercased, as gRPC requires). No other
part of the SDK spells those names.

## `KentikCredentials`

```python
from kentik_api.auth.credentials import KentikCredentials

creds = KentikCredentials(email="you@example.com", api_token="...")
```

| Name | Returns | Used by |
| --- | --- | --- |
| `auth_headers(email, api_token)` | A `dict` with `X-CH-Auth-Email` and `X-CH-Auth-API-Token`. | [`request_json()`](../core/rest_runtime.py), on every REST call |
| `KentikCredentials.get_grpc_plugin()` | A `grpc.AuthMetadataPlugin` that sends the same two keys, lowercased, as call metadata. | [`GrpcTransport`](../transports/grpc_client.py) |

## Shape

One credential pair becomes the two transport-specific auth shapes:

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "elk", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
flowchart TD
  pair("email + api_token<br/>resolved by KentikAPI()"):::orangeSrc
  cfg("APIConfig<br/>auth_email, auth_token"):::hub
  rest("RestTransport"):::blue
  rj("request_json()<br/>calls auth_headers()"):::blue
  hdrs("HTTP headers<br/>X-CH-Auth-Email<br/>X-CH-Auth-API-Token"):::blue
  grpcT("GrpcTransport"):::violet
  plugin("grpc.AuthMetadataPlugin<br/>KentikCredentials.get_grpc_plugin()"):::violet
  meta("Call metadata<br/>x-ch-auth-email<br/>x-ch-auth-api-token"):::violet

  pair --> cfg
  cfg -->|"api_config"| rest
  rest -->|"api_config"| rj
  rj -->|"auth_headers() dict"| hdrs
  cfg -->|"auth_email, auth_token"| grpcT
  grpcT -->|"KentikCredentials"| plugin
  plugin -->|"lowercased keys"| meta

  click cfg "../core/api_config.py"
  click rest "../transports/rest_client.py"
  click rj "../core/rest_runtime.py"
  click grpcT "../transports/grpc_client.py"
  click plugin "credentials.py"

  classDef orangeSrc fill:#ffd8a8,stroke:#e8590c,color:#d9480f
  classDef blue fill:#e7f5ff,stroke:#1971c2,color:#1864ab
  classDef violet fill:#f3f0ff,stroke:#7048e8,color:#5f3dc4
  classDef hub fill:#f8f9fa,stroke:#495057,color:#212529
  classDef orangeSrc,blue,violet,hub stroke-width:2px,rx:10px
  linkStyle default stroke-width:2px,stroke-linecap:round,stroke-linejoin:round
```

## Where the SDK reads credentials

`KentikCredentials` only holds and formats the values that it receives.
[`KentikAPI`](../client.py), the SDK's public entrypoint, resolves them:
explicit constructor arguments first, then the `KENTIK_EMAIL` /
`KENTIK_API_TOKEN` environment variables, then the `env_file` argument
(`.env` by default, `None` to skip). `KentikAPI` reads the file into memory, never
into `os.environ`. An explicit argument that is empty or only whitespace
raises `ConfigurationError`. The SDK does not fall back to the environment for
it. `KentikCredentials` is read-only. See
[Authentication](../../../docs/sphinx/authentication.md) for the full rules.
