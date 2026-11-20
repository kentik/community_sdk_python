# Contract: the `client.v5` service

**Feature**: [../spec.md](../spec.md) | **Models**: [../data-model.md](../data-model.md)

`client.v5` is a generated `V5ServiceWrapper`. It is mounted on every
`KentikAPI`, for both `protocol="rest"` and `protocol="grpc"`, and it always
sends its calls over REST to the V5 base URL (see
[client-config.md](client-config.md)).

## Operations

| Method | HTTP | Request | Returns | Success status |
| --- | --- | --- | --- | --- |
| `top_x_data(*, data, api_config_override=None)` | `POST /query/topXdata` | `QueryRequest` | `TopXDataResponse` | 200 |
| `top_x_chart(*, data, api_config_override=None)` | `POST /query/topXchart` | `ChartRequest` | `ChartResponse` | 200 |
| `query_url(*, data, api_config_override=None)` | `POST /query/url` | `QueryRequest` | `str` | 200 |
| `batch_tags(*, data, api_config_override=None)` | `POST /batch/tags` | `BatchPart` | `BatchResponse` | 202 |
| `batch_populators(*, dimensionName, data, api_config_override=None)` | `POST /batch/customdimensions/{dimensionName}/populators` | `BatchPart` | `BatchResponse` | 202 |
| `batch_status(*, guid, api_config_override=None)` | `GET /batch/{guid}/status` | none | `BatchStatus` | 200 |

The paths are relative to the V5 base URL. The method names are recorded in
`public_names.json` on the first generation run (research R13).

## Errors

Each operation raises the same types as every other 2.x operation:

- `ConfigurationError`: credentials are missing, before anything is sent.
- `AuthenticationError`: status 401.
- `TransportError`: no response, including a timeout. This is the expected
  failure of `top_x_chart` until Kentik fixes the endpoint.
- The generated `HTTPException` subclass of the operation (for example
  `TopXDataError`) for every other non-success status. The `message` holds
  the API's `error` text, for example `The device_name is required`.
- `HTTPException` with status 502 when a success body does not match the
  model.

`exc.rate_limit` and the result's quota hold no values, because V5 sends no
rate limit headers.

## Documented declared statuses

The description file declares, for each operation, the success status above
and `400`, `401`, `403`, `404`, `429`, and `500`. The mocked suites assert the
SDK behavior for every declared status (Principle IV).

## Guarantees

- No retry. A 429 raises at once.
- `batch_tags` and `batch_populators` are sent once. The SDK never resends a
  batch part (FR-014).
- A gRPC client sends these calls over REST. No call raises
  `NotImplementedError`.
- Unknown string values in a response are kept as they are (FR-010).
- Extra keys in a result row are kept (FR-003).
