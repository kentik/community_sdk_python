<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](../../../pyproject.toml). Edit directly. -->

# Migrating from 1.x

Version 2 is a new SDK with the same package name. It shares no code with
[kentik-api 1.x](https://github.com/kentik/community_sdk_python/tree/v1.0.7).
Version 1 wrapped the V5 REST API, which Kentik marks as deprecated, plus two
V6 gRPC services. A generator builds version 2 from Kentik's V6 API schema.
Version 2 covers every V6 service that the schema publishes. Where V6 has no
equivalent of a V5 endpoint (the query and batch APIs), `client.v5` calls the
V5 endpoint itself. See [V5 query and batch calls](v5.md).

There is no compatibility layer. Rewrite each call against the new client.
The table "Every 1.x call in 2.x" below lists the replacement of each call.

## At a glance

| | 1.x | 2.x |
| --- | --- | --- |
| Python | 3.8 and later | 3.12 and later |
| API | V5 REST, plus V6 gRPC for synthetics and cloud export | V6, over REST or gRPC |
| Import | `from kentik_api import KentikAPI` | `from kentik_api.client import KentikAPI` |
| Credentials | `KentikAPI(email, token)`, or a profile in `~/.kentik/` | Arguments, `KENTIK_EMAIL` / `KENTIK_API_TOKEN`, or a `.env` file |
| Region | `api_host="api.kentik.eu"` | `region="eu"` |
| Resources | `client.sites`, `client.devices` | `client.site`, `client.device`, one attribute per service |
| Methods | `get_all()`, `get(id)`, `create(obj)` | `list()`, `get(id=...)`, `create(data=...)`, named after the API operation |
| Arguments | Positional | Keyword only |
| Data types | Hand-written classes such as `Site` | Generated Pydantic models |
| Errors | `KentikAPIError` and subclasses | `KentikError` and subclasses |
| Timeout | `timeout=(10.0, 60.0)` | `timeout=60.0`, or `rest_timeout=httpx.Timeout(...)` |
| Retries | `retry_strategy=Retry(...)` | Failed connection attempts only, twice. No retry after the server responds. |
| Proxy | `proxy="http://..."` | The `https_proxy` and `no_proxy` environment variables, on both transports |

## One call, before and after

1.x:

```python
from kentik_api import KentikAPI, Site

client = KentikAPI(email, token)
created = client.sites.create(Site(site_name="lab", latitude=49, longitude=12))
got = client.sites.get(created.id)
```

2.x:

```python
from kentik_api.client import KentikAPI
from kentik_api.gen.site.models import CreateSiteRequest, Site, SiteType

with KentikAPI(email=email, api_token=token) as client:
    created = client.site.create(
        data=CreateSiteRequest(
            site=Site(title="lab", lat=49, lon=12, type=SiteType.SITE_TYPE_DATA_CENTER)
        )
    )
    got = client.site.get(id=created.site.id)
```

Field names follow the V6 schema, not 1.x. In this example, `site_name` becomes
`title`, and `latitude` becomes `lat`. Each service's reference page lists its
operations and models, for example [site](../services/site.md).

## Credentials

1.x read `KTAPI_AUTH_EMAIL` and `KTAPI_AUTH_TOKEN` in its examples, or a JSON
profile under `~/.kentik/`. 2.x reads neither. See
[Authentication](../authentication.md) for the order in which 2.x looks for
credentials, and for how to keep them encrypted.

## Errors

| 1.x | 2.x |
| --- | --- |
| `KentikAPIError` | `KentikError` |
| `AuthError` | `AuthenticationError` |
| `TimedOutError`, `UnavailabilityError` | `TransportError` |
| `NotFoundError`, `BadRequestError` | `HTTPException`, with `status_code` 404 or 400 |
| `RateLimitExceededError` | `HTTPException` with `status_code` 429. The quota is in `exc.rate_limit`. |

See the [error handling guide](error_handling.md).

A gRPC response larger than 40 MiB raises `TransportError`, not a 429. 1.x
allowed 40 MB, and grpcio alone allows only 4 MiB. To change the limit, pass
`grpc_options=[("grpc.max_receive_message_length", N)]` to `KentikAPI`.

## Every 1.x call in 2.x

2.x adds a V5 call only when V6 has no equivalent, so each 1.x call has one
replacement. Method arguments are keyword only, and models are in
`kentik_api.gen.<service>.models`.

| 1.x call | 2.x call | Notes |
| --- | --- | --- |
| `sites.get_all`, `get`, `create`, `update`, `delete` | `site.list`, `get`, `create`, `update`, `delete` | `site_name` is `title`, `latitude` is `lat`, `longitude` is `lon` |
| `devices.get_all`, `get`, `create`, `update`, `delete` | `device.list`, `get`, `create`, `update`, `delete` | `device_name` is `deviceName`. 2.x adds `create_bulk`, `update_bulk`, `delete_bulk`, and `get_by_name` |
| `devices.apply_labels` | `device.update_labels` | |
| `devices.interfaces.get_all(device_id)` | `interface.list` | Filter on the device ID in the request |
| `devices.interfaces.get`, `create`, `update`, `delete` | `interface.get`, `create`, `update`, `delete` | |
| `device_labels.get_all`, `create`, `update`, `delete` | `label.list`, `create`, `update`, `delete` | |
| `device_labels.get` | `label.list` | No get call. List the labels and filter |
| `users.get_all`, `get`, `create`, `update`, `delete` | `user.list`, `get`, `create`, `update`, `delete` | 2.x adds token and session reset |
| `tags.get_all` | `flow_tag.search` | Page through the search |
| `tags.get`, `create`, `update`, `delete` | `flow_tag.get`, `create`, `update`, `delete` | |
| `saved_filters.get_all`, `get`, `create`, `update`, `delete` | `saved_filter.list`, `get`, `create`, `update`, `delete` | |
| `custom_dimensions.get_all`, `get`, `create`, `update`, `delete` | `custom_dimension.list`, `get_info`, `create`, `update`, `delete` | |
| `custom_dimensions.populators.create`, `update`, `delete` | `custom_dimension.create_populator`, `update_populator`, `delete_populator` | 2.x adds `get_populator` |
| `custom_applications.get_all`, `create`, `update`, `delete` | `custom_application.list`, `create`, `update`, `delete` | 2.x adds `get` |
| `plans.get_all` | `plan.list` | |
| `my_kentik_portal.get_all`, `get`, `create_tenant_user`, `delete_tenant_user` | `mkp.tenant_list`, `tenant_get`, `tenant_user_create`, `tenant_user_delete` | 2.x adds tenant and package management |
| `alerting.create_manual_mitigation` | `alerting.mitigations_create` | The request names a platform ID and a method ID |
| `alerting.get_active_alerts` | `alerting.list` | Filters move into the request body |
| `alerting.get_alerts_history` | `alerting.list` | Set `filters.states` and a `filters.startedAt` range |
| `query.data` | `v5.top_x_data` | A V5 call. See [V5 query and batch calls](v5.md) |
| `query.chart` | `v5.top_x_chart`, then `kentik_api.v5_tools.decode_chart()` | Not verified: the endpoint gave no response in a live check |
| `query.url` | `v5.query_url` | Returns the link as `str` |
| `query.sql` | None | Kentik retired the V5 SQL endpoint on 2025-05-01. Query the same data with `v5.top_x_data` |
| `batch.batch_operation_on_flow_tags` | `v5.batch_tags` | Use `split_batch()` and `send_batch()` for a large set |
| `batch.batch_operation_on_populators(dimension_name, ...)` | `v5.batch_populators(dimensionName=..., data=...)` | |
| `batch.get_status(guid)` | `v5.batch_status(guid=...)` | `wait_for_batch()` polls it |
| `synthetics.*` | `synthetics.*` | `private_only` filtering moves to the caller |
| `cloud_export.get_all`, `get`, `create`, `update`, `delete` | `cloud_export.list`, `get`, `create`, `update`, `delete` | |
| `cloud_export.patch` | `cloud_export.update` | No field mask. Read the export, change it, and write it back |
| `kentik_api.utils.DeviceCache` | `kentik_api.devices.DeviceLookup` | Saves to JSON, not pickle |
| `kentik_api.analytics` | `kentik_api.analytics`, with `pip install "kentik-api[analytics]"` | Top-X definitions only. A SQL definition or an `@fixup:` mapping raises `ValueError` |

### Renamed fields

A V6 field name is usually the 1.x name in camelCase: `device_name` is
`deviceName`, and `created_date` is `createdDate`. The table lists each other
rename, and each 1.x field that V6 does not have. Many V6 models also drop
`company_id`.

| 1.x class | 2.x model | Renamed fields | No V6 field |
| --- | --- | --- | --- |
| `User` | `user.User` | `email` is `userEmail`, `full_name` is `userFullName`, `filters` is `filter` (a JSON string), `created_date` is `cdate`, `updated_date` is `edate` | `username` (`userEmail` is the user name), `email_service`, `email_product`, `saved_filters` |
| `DeviceLabel` | `label.Label` | `created_date` is `cdate`, `updated_date` is `edate` | `devices`, `user_id` |
| `Tag` | `flow_tag.FlowTag` | `flow_tag` is `name`, `addr` is `ip` (an `AddressInfo` object), `created_date` is `cdate`, `updated_date` is `edate` | `user_id`, `addr_count`, `mac_count` |
| `FilterGroups` | `saved_filter.SavedFilterFilterGroup` | `filterGroups` is `nestedFilterGroups`, `connector` is the boolean `any`, `saved_filters` is `savedFilterIds` (IDs, not objects) | `filterString`, `id`, `metric`, `name`, `named`, `autoAdded` |
| `CustomDimension` | `custom_dimension.CustomDimension` | `display_name` is `description` | |
| `Populator` | `custom_dimension.Populator` | | `dimension_id` |
| `Plan` | `plan.Plan` | `device_types` is `deviceTypes` (a list of device subtypes) | |
| `Tenant` | `mkp.Tenant` | | `created_date`, `updated_date` |
| `TenantUser` | `mkp.TenantUser` | `email` is `userEmail`, `fullname` is `userFullName` | `name`, `last_login` |
| `ManualMitigation` | `alerting.MitigationsServiceCreateRequest` | `platformID` is `platformId`, `methodID` is `methodId`, `minutesBeforeAutoStop` is `autoStopTtl` (a string, and the schema gives no unit) | |
| `Device` | `device.DeviceDetailed` | `interfaces` is `allInterfaces` | `snmp_last_updated` |
| `SNMPv3Conf` | `device.DeviceSnmpV3Conf` | `user_name` is `username` | |
| `Interface` | `interface.Interface` | `created_date` is `cdate`, `updated_date` is `edate` | |
| `VRFAttributes` | `interface.InterfaceVrf` | | `device_id` |
| `Site` | `site.Site` | `site_name` is `title`, `latitude` is `lat`, `longitude` is `lon` | |
| `CloudExport` | `cloud_export.CloudExport` | | `ibm`, `bgp` |
| `AwsProperties` | `cloud_export.AwsProperties` | | `multiple_buckets` |

### V5 query field names

`client.v5` models use the V5 wire names, as 1.x sent them. A 1.x
`QueryObject` becomes a `QueryRequest`, and a `QueryArrayItem` becomes a
`QueryItem`. 1.x enums such as `MetricType.bytes` become plain strings such as
`"bytes"`. `metric` and `device_name` take a string or a list. A query model
keeps every field it gets, so query JSON copied from Data Explorer works
unchanged.

### 1.x examples

| 1.x example | 2.x |
| --- | --- |
| `queries_example.py` | [`examples/v5/query.py`](https://github.com/kentik/community_sdk_python/blob/main/examples/v5/query.py) |
| `batch_example.py` | [`examples/v5/batch.py`](https://github.com/kentik/community_sdk_python/blob/main/examples/v5/batch.py) |
| `analytics_example_topx.py` | [`examples/v5/analytics_topx.py`](https://github.com/kentik/community_sdk_python/blob/main/examples/v5/analytics_topx.py) |
| `analytics_example_sql.py` | No port: Kentik retired the SQL endpoint on 2025-05-01. See [`examples/v5/analytics_topx.py`](https://github.com/kentik/community_sdk_python/blob/main/examples/v5/analytics_topx.py) |
| `demos/queries_visualisation_demo.ipynb` | No port |

## Features that 1.x had and 2.x does not

| 1.x feature | In 2.x |
| --- | --- |
| `client.query.sql` (V5 SQL query) | Kentik retired the endpoint on 2025-05-01. |
| `retry_strategy` | Removed. See the [rate limiting guide](rate_limiting.md) for why the SDK does not retry after a response. |
