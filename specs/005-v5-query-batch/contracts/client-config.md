# Contract: client configuration for V5

**Feature**: [../spec.md](../spec.md) | **Requirement**: FR-006a

## `KentikAPI` additions

```python
KentikAPI(
    email=None,
    api_token=None,
    protocol="rest",
    region="us",
    *,
    v5_base_url: str | None = None,  # new
    timeout=60.0,
    rest_timeout=None,
    grpc_deadline=None,
    grpc_options=None,
    env_file=".env",
)
```

| Input | V5 base URL |
| --- | --- |
| `region="us"`, no `v5_base_url` | `https://api.kentik.com/api/v5` |
| `region="eu"`, no `v5_base_url` | `https://api.kentik.eu/api/v5` |
| any region, `v5_base_url="https://host/api/v5"` | `https://host/api/v5` |

- `v5_base_url` MUST start with `https://`, or `KentikAPI` raises
  `ConfigurationError`. This keeps credentials off plain HTTP.
- The V5 `APIConfig` uses the same credentials, `timeout`, and
  `rest_timeout` as the V6 `APIConfig`. It owns its own `httpx.Client`.
- `client.v5_api_config` is the V5 `APIConfig`. A per-call override comes
  from it, for example
  `client.v5.top_x_chart(data=..., api_config_override=client.v5_api_config.with_timeout(300))`.
- `client.api_config` stays the V6 `APIConfig`.
- `client.close()` and the context manager close both transports.
- The SDK never builds the V5 URL from the V6 URL.

## Not changed

- The V6 host, the transports of every V6 service, and `protocol` behavior.
- The credential order (Principle VI).
