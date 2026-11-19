<!-- HAND-WRITTEN: not modified by [`uv run poe generate`](pyproject.toml). Edit directly. -->

# Changelog

This file lists the changes a caller of the SDK can see. The generated API
surface (services, operations, model fields, and enum values) has its own
record in [`api_surface.json`](api_surface.json). To list surface changes
between two releases, run
[`scripts/release_notes.py`](scripts/release_notes.py):

```bash
uv run poe release-notes
```

Each release appends that list to its GitHub release notes. A pull request
whose surface change can break a caller (a removed or retyped field, for
example) fails `uv run poe check-changelog` until this file names the change.

`uv run poe generate` does not edit this file. When a regeneration ends with
`⚠️ API SURFACE CHANGED`, add an entry here for each listed change before you
commit. See "Update the release notes after every regeneration" in
[the generation guide](docs/sphinx/guides/generation.md).

## Unreleased

This is the first release of the SDK for Kentik's V6 API, and it replaces
kentik-api 1.x completely. If you come from 1.x, read
[Migrating from 1.x](docs/sphinx/guides/migrating-from-1x.md) instead of the
tables below, which compare against earlier development builds of this SDK.

### Runtime fixes

- `TransportError.may_have_reached_server` is false for REST connection and
  pool failures that occur before the request is sent. It is true for other
  transport failures, including gRPC failures. True means the server may have
  received the request, not that it processed it.
- `DFCache.get()` includes the last stored row when its timestamp matches the requested start.
- Dependency requirement narrowed, `grpcio>=1.85.0` to `grpcio>=1.85.3`.
  The generated gRPC code requires the runtime that matches `grpcio-tools` 1.85.3.
  The locked `certifi` and `setuptools` versions
  also change to fix known advisories.
- Over REST, `client.as_group.update()` and `client.site.update_market()`
  now work. Kentik's REST API ignores the documented camelCase body key
  (`asGroup`, `siteMarket`) on these calls, so the SDK sends the proto name
  (`as_group`, `site_market`) instead. `client.flow_tag.update()` and
  `client.alerting.auto_ack_replace()` have the same request layout and send
  the proto name too. The auto-ack call accepts both names. Flow tag writes
  currently fail upstream for another reason. The public signatures do not
  change. The SDK removes this workaround when Kentik fixes the API.
- Over gRPC, `alerting`, `audit`, `custom_application`, `custom_dimension`,
  `plan`, and `saved_filter` now work. Kentik's gRPC server fails every call
  to these services that carries a deadline, and the SDK always sets one. For
  these services only, the SDK sends no deadline and ends the call itself
  when the deadline passes, with the same `TransportError`. The public
  signatures do not change. The SDK removes this workaround when Kentik fixes
  the API.
- `APIConfig` owns its timeout values. Changing a supplied or returned
  `httpx.Timeout` no longer changes active settings. The public type and
  signatures stay unchanged. Use `with_timeout()` for timeout changes.
- `wait_for_batch()` applies one cooperative deadline to status requests
  and sleeps, preserves tighter client limits, and rejects late completion.
  It raises `ValueError` for non-positive or non-finite timeout and interval
  values. A request timeout observed at or after expiry becomes
  `BatchWaitTimeout` with the original error cause. Earlier observed
  timeouts and all non-timeout errors propagate unchanged. This is not a
  hard wall-clock cancellation guarantee.
- Fully buffered REST error responses retain their normal HTTP or JSON
  error instead of becoming deadline timeouts. Successful responses still
  respect the deadline, and unfinished response streams remain bounded.
- `DFCache.fetch_latest()` returns `None` without querying or changing
  files when the newest cached time equals or exceeds the current minute.
  Repeated same-minute refreshes no longer raise an invalid-range error.

### Upstream API changes

The SDK now uses schema commit `9f58fdd`. Kentik replaced two API versions,
so these changes can break a caller:

- **`credential`** moves from `v202407alpha1` to `v20261020alpha1`.
  `client.credential.list_group()` and `get_group()` keep their names but now
  call `/credential/v20261020alpha1/groups`. The old paths
  `/credential/v202407alpha1/group` and `/credential/v202407alpha1/group/{id}`
  are gone, and `get_group()` takes `name` instead of `id`.
  `ListCredentialGroupResponse` (the schema's `ListCredentialGroupsResponse`)
  has no `ListCredentialGroupResponse.invalidCount`.
  `CredentialGroup.version` is optional. `CredentialGroup.createdBy`,
  `credentials`, and `type` now use `CreatedBy`, `Credential`, and
  `CredentialType`. The models `LandingType`, `PermissionEntry`, `Role`,
  `Secret`, `SecretType`, and `User` are removed. New methods: `list`, `get`,
  `delete`, `assign_consumer`, `create_group`, `update_group`,
  `delete_group`, and `list_overviews`.
- **`alerting` suppressions** move from `v202505` to `v202611`. The client
  methods keep their names, but the old paths `/v202505/suppressions`,
  `/v202505/suppressions/list`, and `/v202505/suppressions/{id}` are gone.
  `Suppression.source` becomes `sources`, and `Suppression.strict` and
  `Suppression.userId` are removed. `Suppression.startTimeAt` is optional.
  `SuppressionFilters.sources` now holds `v202505Source`, which has the same
  fields as `Source`. `Suppression` gains `contextFilter`, `startTimeCode`,
  and `endTimeCode`.
- **Added:** `client.synthetics.bulk_update_tests()` and
  `get_bulk_update_tests_status()`, new `dictionary` and `kagent` fields, and
  the `kagent` installer types `INSTALLER_TYPE_DEB` and `INSTALLER_TYPE_RPM`.
  `kagent` `InstallConfig` gains `bundleSource`, which uses the new
  `BundleSource` enum.

### Breaking changes

Each change below can stop an existing `except` clause or call from working.

| Before | After | What to change |
| --- | --- | --- |
| `KentikAPI(...)` raised `ValueError` for missing credentials, an unknown region, or an unknown protocol | It raises `ConfigurationError` | Catch `ConfigurationError` or `KentikError` |
| A REST 401 raised the operation's generated `HTTPException` subclass | It raises `AuthenticationError`, as gRPC does | Catch `AuthenticationError` |
| gRPC `CANCELLED`, `DEADLINE_EXCEEDED`, and `UNAVAILABLE` raised `HTTPException` with status 500 or 503 | They raise `TransportError`, as REST does for the same failures | Catch `TransportError` |
| A gRPC status code with no mapping raised `HTTPException(500)` | Every code has an explicit mapping; an unrecognized code raises `TransportError` | See the table in [the error handling guide](docs/sphinx/guides/error_handling.md) |
| A gRPC call had no deadline and could block forever | Every gRPC call has a deadline, 60 seconds by default | Set `timeout` or `grpc_deadline` for longer calls |
| `call_grpc()` wrapped any exception from the stub in `TransportError` | Only a gRPC error is converted; other exceptions propagate unchanged | Catch the original exception type |
| `call_grpc()` returned the response | It returns `(response, rate_limit)` | Unpack the tuple |
| `KentikCredentials.get_rest_headers()` existed | It is removed | Use `kentik_api.auth.credentials.auth_headers(email, api_token)` |
| `RestTransport(credentials, base_url=..., api_config=None)` and `GrpcTransport(credentials, target, api_config=None, options)` built their own `APIConfig` when none was given, with a default host and timeout that could differ from the client's | Each takes one `APIConfig`, the single source of host, credentials, and timeouts: `RestTransport(api_config)`, `GrpcTransport(api_config, target, options)`. `GrpcTransport` raises `ConfigurationError` when the config has no credentials | Build an `APIConfig(base_path=..., auth_email=..., auth_token=...)` and pass it, or use `KentikAPI`, which builds it for you |
| An `APIConfig` with no credentials failed inside httpx with `TypeError` | It raises `ConfigurationError` before the SDK sends a request | Give the config `auth_email` and `auth_token` |
| `KentikAPI(...)` loaded every key of the nearest `.env` into `os.environ`, even when you passed credentials | It reads only `KENTIK_EMAIL` and `KENTIK_API_TOKEN`, into memory, and only when an argument or environment variable is missing | Load other `.env` keys yourself, for example with `dotenv.load_dotenv()` |
| `kmeta` `ServiceNowConfig.credentialVaultId` held a credential vault entry ID | Upstream renamed it `credentialVaultName`; it holds the entry's name and always resolves to the entry's latest version | Read and send `credentialVaultName` |
| Client method names depended on module and route order, and many repeated the Service name (`client.audit.get_audit_event`) | Names no longer depend on order and drop the Service word when two or more words remain. See [Renamed client methods](#renamed-client-methods) | Use the new names in the table below |
| 55 model names held a schema version (`labelv202210Label`), so a version bump renamed them | The version and its package prefix are gone (`Label`). See [Renamed models](#renamed-models) | Use the new names in the table below |
| Error classes were named after the upstream operationId, and operations that share one (`alerting` has eight `List` operations) shared one class | Each operation has its own class, named after its client method: `client.label.list` raises `ListError`. See [Renamed error classes](#renamed-error-classes) | Catch the new names in the table below |
| Each error package exported `ERROR_BY_OPERATION`, keyed by operationId | It exports `ERROR_BY_METHOD`, keyed by client method name | Look up `ERROR_BY_METHOD["list"]` |
| The SDK accepted `pydantic>=2.12.5` | It needs `pydantic>=2.14.0`, for thread-safe model rebuilds and constant-time secret comparison | Upgrade Pydantic to 2.14.0 or later |
| The SDK accepted `python-dotenv>=1.2.1` | It needs `python-dotenv>=1.2.4`. Earlier versions drop the first variable after a byte order mark, and read `KEY= # comment` as the comment text | Upgrade python-dotenv to 1.2.4 or later |

#### Renamed client methods

A name that several modules of one Service declare carries the module prefix
in every module, so a client method name never moves to another operation. A
second HTTP route of one operation is named by its extra path parameters, not
by a number. A name drops the Service word, because `client.<service>`
already says it: `client.site.create`, not `client.site.create_site`. See
[Shorter client methods](#shorter-client-methods). A protoc default operationId
(`RouteService_List`) loses its module prefix, so no name holds a double
underscore; if one word is left, the module noun stays
(`client.ktbgp.route_list`).

| Service | Before | After |
| --- | --- | --- |
| `alerting` | `list`, `get`, `create`, `delete`, `replace` (AlertAutoAckService) | `auto_ack_list`, `auto_ack_get`, `auto_ack_create`, `auto_ack_delete`, `auto_ack_replace` |
| `alerting` | `alert_silence_notifications_list`, `alert_silence_notifications_get`, `alert_silence_notifications_create`, `alert_silence_notifications_delete`, `alert_silence_notifications_replace` | `silence_notifications_list`, `silence_notifications_get`, `silence_notifications_create`, `silence_notifications_delete`, `silence_notifications_replace` |
| `audit` | `list_audit_events`, `get_audit_event`, `get_audit_event_2` | `list_events`, `get_event`, `get_event_by_ctime` |
| `cost` | `list_cost_providers`, `list_cost_provider_summaries`, `get_cost_provider_summary` | `list_providers`, `list_provider_summaries`, `get_provider_summary` |
| `credential` | `list_credential_group`, `get_credential_group` | `list_group`, `get_group` |
| `custom_dimension` | `get_custom_dimension_info` | `get_info` |
| `device` | `update_device_labels` | `update_labels` |
| `journeys` | `get_journeys_nlq` | `get_nlq` |
| `kagent` | `capability_admin_service__list_capabilities`, `capability_admin_service__get_capability`, `capability_admin_service__create_capability`, `capability_admin_service__update_capability`, `capability_admin_service__delete_capability` | `list_capabilities`, `get_capability`, `create_capability`, `update_capability`, `delete_capability` |
| `kagent` | `capability_release_service__get_capability_release`, `capability_release_service__get_capability_latest_releases`, `capability_release_service__get_capability_supported_distros` | `get_capability_release`, `get_capability_latest_releases`, `get_capability_supported_distros` |
| `ktbgp` | `route_service__list`, `route_service__announce`, `route_service__withdraw` | `route_list`, `route_announce`, `route_withdraw` |
| `nms` | `metrics_schema_service__get_metrics_schema` | `get_metrics_schema` |
| `pathfinder` | `create_pathfinder_report` | `create_report` |
| `site` | `list_site_markets`, `get_site_market`, `create_site_market`, `update_site_market`, `delete_site_market` | `list_markets`, `get_market`, `create_market`, `update_market`, `delete_market` |

[`api_surface.json`](api_surface.json) now records the client method for each operation, so
`uv run poe check-changelog` flags a renamed method as a breaking change. It also
records the gRPC method each operation calls, so an operation that stops
working over gRPC is a breaking change too.

#### Renamed models

Each model module is renamed too: import from
`kentik_api.gen.<service>.models`, for example
`from kentik_api.gen.label.models import Label`.
`v202505AlertAcknowledgement` in `alerting` keeps its name, because
`AlertAcknowledgement` is a different model.

| Service | Before | After |
| --- | --- | --- |
| `alerting` | `typesv202506PaginationConfig`, `typesv202506PaginationInfo`, `typesv202506SortingConfig` | `PaginationConfig`, `PaginationInfo`, `SortingConfig` |
| `alerting` | `v202303AttributeFilter`, `v202303AttributeFilterStringArray`, `v202303KeyValue`, `v202303KeyValueFilter`, `v202303MultiAttributeFilter`, `v202303Severity`, `v202303SimpleAttributeFilter`, `v202303SimpleAttributeFilterStringArray`, `v202303TimeRange` | `AttributeFilter`, `AttributeFilterStringArray`, `KeyValue`, `KeyValueFilter`, `MultiAttributeFilter`, `Severity`, `SimpleAttributeFilter`, `SimpleAttributeFilterStringArray`, `TimeRange` |
| `alerting` | `v202501BitwiseOp`, `v202501FlowspecMatch`, `v202501Fragment`, `v202501FragmentFormula`, `v202501FragmentPredicate`, `v202501FragmentPredicateGroup`, `v202501NumericFormula`, `v202501NumericOp`, `v202501NumericPredicate`, `v202501NumericPredicateGroup`, `v202501TCPFlag`, `v202501TCPFlagsFormula`, `v202501TCPFlagsPredicate`, `v202501TCPFlagsPredicateGroup` | `BitwiseOp`, `FlowspecMatch`, `Fragment`, `FragmentFormula`, `FragmentPredicate`, `FragmentPredicateGroup`, `NumericFormula`, `NumericOp`, `NumericPredicate`, `NumericPredicateGroup`, `TCPFlag`, `TCPFlagsFormula`, `TCPFlagsPredicate`, `TCPFlagsPredicateGroup` |
| `alerting` | `v202506MitigationTarget` | `MitigationTarget` |
| `bgp_monitoring` | `v202303Afi`, `v202303RpkiStatus`, `v202303Safi`, `v202303UserInfo`, `v202303VantagePoint` | `Afi`, `RpkiStatus`, `Safi`, `UserInfo`, `VantagePoint` |
| `cost` | `costv202308Status` | `Status` |
| `credential` | `v202211LandingType`, `v202211PermissionEntry`, `v202211Role`, `v202211User`, `v202312alpha1Secret`, `v202312alpha1SecretType` | `LandingType`, `PermissionEntry`, `Role`, `User`, `Secret`, `SecretType` |
| `device` | `devicev202504beta2Label` | `Label` |
| `kagent` | `kagentv202401AgentConfig` | `AgentConfig` |
| `ktbgp` | `ktbgpv202501Withdraw` | `Withdraw` |
| `label` | `labelv202210Label` | `Label` |
| `mkp` | `v202211LandingType`, `v202211PermissionEntry`, `v202211Role`, `v202211User` | `LandingType`, `PermissionEntry`, `Role`, `User` |
| `rbux` | `v202501alpha1FilterField`, `v202501alpha1FilterOperator`, `v202501alpha1SavedFilterFilter`, `v202501alpha1SavedFilterFilterGroup`, `v202501alpha1SavedFilterFilterId`, `v202501alpha1SavedFilterFilters` | `FilterField`, `FilterOperator`, `SavedFilterFilter`, `SavedFilterFilterGroup`, `SavedFilterFilterId`, `SavedFilterFilters` |
| `synthetics` | `syntheticsv202309Location`, `v202303UserInfo` | `Location`, `UserInfo` |

These fields keep their names, but their type is now the renamed model:

- `alerting`: `Alert.highestSeverity`, `Alert.severity`, `AlertAutoAck.key`,
  `AlertAutoAckFilters.createdAt`, `AlertAutoAckFilters.endTimeAt`,
  `AlertAutoAckFilters.keys`, `AlertAutoAckFilters.modifiedAt`,
  `AlertAutoAckFilters.startTimeAt`,
  `AlertAutoAckServiceListRequest.pagination`,
  `AlertAutoAckServiceListRequest.sorting`,
  `AlertAutoAckServiceListResponse.pagination`, `AlertFilters.activeAt`,
  `AlertFilters.endedAt`, `AlertFilters.highestSeverities`,
  `AlertFilters.keys`, `AlertFilters.recentSeverities`,
  `AlertFilters.severities`, `AlertFilters.startedAt`, `AlertPhase.severity`,
  `AlertServiceListRequest.pagination`, `AlertServiceListRequest.sorting`,
  `AlertServiceListResponse.pagination`,
  `AlertSilenceNotificationFilters.createdAt`,
  `AlertSilenceNotificationFilters.endTimeAt`,
  `AlertSilenceNotificationFilters.keys`,
  `AlertSilenceNotificationFilters.modifiedAt`,
  `AlertSilenceNotificationFilters.startTimeAt`,
  `AlertSilenceNotificationsDefinition.key`,
  `AlertSilenceNotificationsServiceListRequest.pagination`,
  `AlertSilenceNotificationsServiceListRequest.sorting`,
  `AlertSilenceNotificationsServiceListResponse.pagination`,
  `Mitigation.target`, `MitigationFilters.createdAt`,
  `MitigationMethodsFilters.createdAt`, `MitigationMethodsFilters.modifiedAt`,
  `MitigationMethodsServiceListResponse.pagination`,
  `MitigationPlatformsFilters.createdAt`,
  `MitigationPlatformsFilters.modifiedAt`,
  `MitigationPlatformsServiceListResponse.pagination`,
  `MitigationsServiceListResponse.pagination`,
  `NmsContextActivationInfo.severity`, `PolicyListFilters.createdAt`,
  `PolicyListFilters.modifiedAt`, `PolicyPolicyLevel.severity`,
  `PolicyServiceListRequest.pagination`, `PolicyServiceListRequest.sorting`,
  `PolicyServiceListResponse.pagination`, `Suppression.keyFilter`,
  `Suppression.severities`, `SuppressionFilters.createdAt`,
  `SuppressionFilters.endTimeAt`, `SuppressionFilters.modifiedAt`,
  `SuppressionFilters.startTimeAt`, `SuppressionServiceListRequest.pagination`,
  `SuppressionServiceListRequest.sorting`,
  `SuppressionServiceListResponse.pagination`
- `bgp_monitoring`: `BgpMonitor.createdBy`, `BgpMonitor.lastUpdatedBy`,
  `Nlri.afi`, `Nlri.safi`, `RouteInfo.rpkiStatus`, `RouteInfo.vantagePoint`
- `cost`: `CostProviderSummary.status`
- `credential`: `CredentialGroup.createdBy`, `CredentialGroup.credentials`,
  `CredentialGroup.type`
- `device`: `DeviceDetailed.labels`
- `kagent`: `Agent.config`, `AgentServiceUpdateAgentBody.config`
- `ktbgp`: `RouteServiceWithdrawRequest.withdraw`
- `label`: `CreateLabelRequest.label`, `CreateLabelResponse.label`,
  `ListLabelsResponse.labels`, `UpdateLabelResponse.label`
- `mkp`: `Tenant.users`
- `rbux`: `ScopeConfig.filters`
- `synthetics`: `NetNode.location`, `Test.createdBy`, `Test.lastUpdatedBy`

#### Renamed error classes

An error class is now named after its client method, so it keeps its name
when upstream changes the operationId. Each response class follows its
operation class: `ListLabelsUnexpectedError` extends `ListLabelsError`. A
name that would match a Python builtin exception gets the Service name in
front. Acronyms are no longer all capitals, because method names are lowercase
(`ListASGroupsError` is now `ListAsGroupsError`).

In `alerting`, `CreateError`, `DeleteError`, `GetError`, `ListError`, and
`ReplaceError` are split into one class per method. Each class name is the
method name in PascalCase with `Error` added: `list` raises `ListError`,
`auto_ack_get` raises `AutoAckGetError`, and
`suppression_delete` raises `SuppressionDeleteError`.

| Service | Before | After |
| --- | --- | --- |
| `as_group` | `ListASGroupsError`, `GetASGroupError`, `CreateASGroupError`, `UpdateASGroupError`, `DeleteASGroupError` | `ListAsGroupsError`, `GetAsGroupError`, `CreateAsGroupError`, `UpdateAsGroupError`, `DeleteAsGroupError` |
| `audit` | `ListAuditEventsError`, `GetAuditEventError` (both routes) | `ListEventsError`, `GetEventError`, `GetEventByCtimeError` |
| `cost` | `ListCostProvidersError`, `ListCostProviderSummariesError`, `GetCostProviderSummaryError` | `ListProvidersError`, `ListProviderSummariesError`, `GetProviderSummaryError` |
| `credential` | `ListCredentialGroupError`, `GetCredentialGroupError` | `ListGroupError`, `GetGroupError` |
| `custom_dimension` | `GetCustomDimensionInfoError` | `GetInfoError` |
| `device` | `UpdateDeviceLabelsError` | `UpdateLabelsError` |
| `journeys` | `GetJourneysNlqError` | `GetNlqError` |
| `kagent` | `CapabilityAdminService_ListCapabilitiesError`, `CapabilityAdminService_GetCapabilityError`, `CapabilityAdminService_CreateCapabilityError`, `CapabilityAdminService_UpdateCapabilityError`, `CapabilityAdminService_DeleteCapabilityError` | `ListCapabilitiesError`, `GetCapabilityError`, `CreateCapabilityError`, `UpdateCapabilityError`, `DeleteCapabilityError` |
| `kagent` | `CapabilityReleaseService_GetCapabilityReleaseError`, `CapabilityReleaseService_GetCapabilityLatestReleasesError`, `CapabilityReleaseService_GetCapabilitySupportedDistrosError` | `GetCapabilityReleaseError`, `GetCapabilityLatestReleasesError`, `GetCapabilitySupportedDistrosError` |
| `kmi` | `GetASNInsightsError`, `GetASNDetailsError` | `GetAsnInsightsError`, `GetAsnDetailsError` |
| `ktbgp` | `RouteService_ListError`, `RouteService_AnnounceError`, `RouteService_WithdrawError` | `RouteListError`, `RouteAnnounceError`, `RouteWithdrawError` |
| `nms` | `MetricsSchemaService_GetMetricsSchemaError` | `GetMetricsSchemaError` |
| `pathfinder` | `CreatePathfinderReportError` | `CreateReportError` |
| `site` | `ListSiteMarketsError`, `GetSiteMarketError`, `CreateSiteMarketError`, `UpdateSiteMarketError`, `DeleteSiteMarketError` | `ListMarketsError`, `GetMarketError`, `CreateMarketError`, `UpdateMarketError`, `DeleteMarketError` |

#### Shorter client methods

A client method drops the Service word even when one word is left:
`client.site.create()`, `client.user.list()`. A method for another object
keeps its noun (`client.site.create_market()`). The device bulk calls end in
`_bulk`. When two names would become one, both keep the long name. The error
classes follow: `client.site.create` raises `CreateError`, in
`kentik_api.gen.site.error`.

| Service | Before | After |
| --- | --- | --- |
| `alerting` | `alert_get`, `alert_list` | `get`, `list` |
| `as_group` | `create_as_group`, `delete_as_group`, `get_as_group`, `list_as_groups`, `update_as_group` | `create`, `delete`, `get`, `list`, `update` |
| `capacity_plan` | `get_capacity_plan`, `list_capacity_plans` | `get`, `list` |
| `cloud_export` | `create_cloud_export`, `delete_cloud_export`, `get_cloud_export`, `list_cloud_exports`, `update_cloud_export` | `create`, `delete`, `get`, `list`, `update` |
| `custom_application` | `create_custom_application`, `delete_custom_application`, `get_custom_application`, `list_custom_applications`, `update_custom_application` | `create`, `delete`, `get`, `list`, `update` |
| `custom_dimension` | `create_custom_dimension`, `delete_custom_dimension`, `list_custom_dimensions`, `update_custom_dimension` | `create`, `delete`, `list`, `update` |
| `device` | `create_device`, `create_devices`, `delete_device`, `delete_devices`, `get_device`, `get_device_by_name`, `list_devices`, `update_device`, `update_devices` | `create`, `create_bulk`, `delete`, `delete_bulk`, `get`, `get_by_name`, `list`, `update`, `update_bulk` |
| `dictionary` | `get_dictionary` | `get` |
| `flow_tag` | `create_flow_tag`, `delete_flow_tag`, `get_flow_tag`, `search_flow_tag`, `update_flow_tag` | `create`, `delete`, `get`, `search`, `update` |
| `interface` | `interface_create`, `interface_delete`, `interface_get`, `interface_update`, `list_interface` | `create`, `delete`, `get`, `update`, `list` |
| `label` | `create_label`, `delete_label`, `list_labels`, `update_label` | `create`, `delete`, `list`, `update` |
| `network_class` | `network_class_get`, `network_class_update` | `get`, `update` |
| `notification_channel` | `get_notification_channel`, `list_notification_channels`, `search_notification_channels` | `get`, `list`, `search` |
| `plan` | `list_plans` | `list` |
| `saved_filter` | `create_saved_filter`, `delete_saved_filter`, `get_saved_filter`, `list_saved_filters`, `list_saved_filters_all`, `update_saved_filter` | `create`, `delete`, `get`, `list`, `list_all`, `update` |
| `site` | `create_site`, `delete_site`, `get_site`, `list_sites`, `update_site` | `create`, `delete`, `get`, `list`, `update` |
| `user` | `create_user`, `delete_user`, `get_user`, `list_users`, `update_user` | `create`, `delete`, `get`, `list`, `update` |

| Service | Error classes before | After |
| --- | --- | --- |
| `alerting` | `AlertGetError`, `AlertListError` | `GetError`, `ListError` |
| `as_group` | `CreateAsGroupError`, `DeleteAsGroupError`, `GetAsGroupError`, `ListAsGroupsError`, `UpdateAsGroupError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `UpdateError` |
| `capacity_plan` | `GetCapacityPlanError`, `ListCapacityPlansError` | `GetError`, `ListError` |
| `cloud_export` | `CreateCloudExportError`, `DeleteCloudExportError`, `GetCloudExportError`, `ListCloudExportsError`, `UpdateCloudExportError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `UpdateError` |
| `custom_application` | `CreateCustomApplicationError`, `DeleteCustomApplicationError`, `GetCustomApplicationError`, `ListCustomApplicationsError`, `UpdateCustomApplicationError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `UpdateError` |
| `custom_dimension` | `CreateCustomDimensionError`, `DeleteCustomDimensionError`, `ListCustomDimensionsError`, `UpdateCustomDimensionError` | `CreateError`, `DeleteError`, `ListError`, `UpdateError` |
| `device` | `CreateDeviceError`, `CreateDevicesError`, `DeleteDeviceError`, `DeleteDevicesError`, `GetDeviceError`, `GetDeviceByNameError`, `ListDevicesError`, `UpdateDeviceError`, `UpdateDevicesError` | `CreateError`, `CreateBulkError`, `DeleteError`, `DeleteBulkError`, `GetError`, `GetByNameError`, `ListError`, `UpdateError`, `UpdateBulkError` |
| `dictionary` | `GetDictionaryError` | `GetError` |
| `flow_tag` | `CreateFlowTagError`, `DeleteFlowTagError`, `GetFlowTagError`, `SearchFlowTagError`, `UpdateFlowTagError` | `CreateError`, `DeleteError`, `GetError`, `SearchError`, `UpdateError` |
| `interface` | `InterfaceCreateError`, `InterfaceDeleteError`, `InterfaceGetError`, `InterfaceUpdateError`, `ListInterfaceError` | `CreateError`, `DeleteError`, `GetError`, `UpdateError`, `ListError` |
| `label` | `CreateLabelError`, `DeleteLabelError`, `ListLabelsError`, `UpdateLabelError` | `CreateError`, `DeleteError`, `ListError`, `UpdateError` |
| `network_class` | `NetworkClassGetError`, `NetworkClassUpdateError` | `GetError`, `UpdateError` |
| `notification_channel` | `GetNotificationChannelError`, `ListNotificationChannelsError`, `SearchNotificationChannelsError` | `GetError`, `ListError`, `SearchError` |
| `plan` | `ListPlansError` | `ListError` |
| `saved_filter` | `CreateSavedFilterError`, `DeleteSavedFilterError`, `GetSavedFilterError`, `ListSavedFiltersError`, `ListSavedFiltersAllError`, `UpdateSavedFilterError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `ListAllError`, `UpdateError` |
| `site` | `CreateSiteError`, `DeleteSiteError`, `GetSiteError`, `ListSitesError`, `UpdateSiteError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `UpdateError` |
| `user` | `CreateUserError`, `DeleteUserError`, `GetUserError`, `ListUsersError`, `UpdateUserError` | `CreateError`, `DeleteError`, `GetError`, `ListError`, `UpdateError` |

### Added

- **`v5` service.** `client.v5` brings back the V5 query calls that have no
  V6 equivalent: `top_x_data`, `top_x_chart`, and `query_url`. They are
  generated from a hand-maintained description in [`schema/openapi/`](schema/openapi/) and
  always go over REST to the V5 host (`https://api.kentik.com/api/v5`, or
  `https://api.kentik.eu/api/v5` for `region="eu"`), also on a client created
  with `protocol="grpc"`. A query model keeps every field it gets, so query
  JSON from 1.x or from Data Explorer works unchanged. `top_x_chart` is not
  verified: the endpoint gave no response in a live check.
  `kentik_api.v5_tools.decode_chart()` turns its result into image bytes. The
  V5 SQL endpoint is retired, so there is no SQL call. A V5 error's text
  (for example `The device_name is required`) ends the exception message, and
  V5 calls report no quota, because V5 sends no rate limit headers.
- **V5 batch calls.** `client.v5.batch_tags`, `batch_populators`, and
  `batch_status` bring back bulk flow tag and populator updates.
  `kentik_api.v5_tools.split_batch()` packs a large set into parts of at most
  4 MB, `send_batch()` sends them with the batch guid and never resends a
  part, and `wait_for_batch()` polls the status with a time limit.
- **`analytics` extra.** `pip install "kentik-api[analytics]"` brings back
  the 1.x `kentik_api.analytics` package on top of `client.v5.top_x_data`:
  `DataQueryDefinition`, `DFCache`, and `flatness_analysis`, with the same
  names and output. SQL definitions and the `@fixup:` column type are gone:
  the SQL endpoint is retired, and `@fixup:` ran Python code from the
  definition file. Definition files load with `yaml.safe_load`. `DFCache`
  writes file names with `_` in place of `:`, because Windows does not allow
  `:` in a file name. It still reads the 1.x names.
- **`kentik_api.devices.DeviceLookup`.** Replaces 1.x `DeviceCache`: devices
  and interfaces by ID or name, link names, and link speeds, from the V6
  `device` and `interface` services. It saves and loads JSON, not pickle.
- **`v5_base_url` argument and `v5_api_config` property.** `KentikAPI` takes
  a custom V5 host (it must use https). `client.v5_api_config` is the base
  for a per-call override of a `client.v5` call.
- **Stable public names.** [`public_names.json`](public_names.json) sets the name of every Service,
  client method, and model, and each method's error classes follow its name. A version bump or a new operationId upstream no
  longer renames anything. When upstream moves or renames something,
  generation fails and names the entry to update. See "Keep public names
  stable" in [the generation guide](docs/sphinx/guides/generation.md).
- **`kmeta` service.** `client.kmeta` manages ServiceNow configurations: list,
  get, create, update, and delete. It predates `api_surface.json`, so
  `uv run poe release-notes` does not list it.
- **`nms` service.** `client.nms.get_metrics_schema()`
  returns the NMS metrics schema: each measurement and its fields, on REST
  and gRPC. The response's `schema` field is `schema_` in Python, because
  `schema` is a `BaseModel` attribute.
- **Static agent addresses.** `synthetics` `AgentMetadata` has read-only
  `staticIpv4` and `staticIpv6`, true when the agent's public address does not
  change.
- **`env_file` argument.** `KentikAPI(env_file=path)` reads credentials from
  that file. `env_file=None` turns off file lookup. See
  [Authentication](docs/sphinx/authentication.md) for use with encrypted
  secrets such as sops.
- **Timeouts.** `KentikAPI` and `APIConfig` accept `timeout` (both transports),
  `rest_timeout` (a number or a per-phase `httpx.Timeout`), and
  `grpc_deadline`. A zero or negative value raises `ConfigurationError`.
- **Per-call overrides.** Every service method accepts `api_config_override`.
  `client.api_config.with_timeout(300)` gives a copy with a longer timeout
  that shares the client's connection and credentials. An override replaces
  the client's configuration for that call. On gRPC, only its deadline
  applies.
- **Quota reporting.** `kentik_api.rate_limit_of(result)` returns the quota
  that the call reported. Every SDK exception has a `rate_limit` attribute.
  `client.api_config.rate_limits` holds the latest quota for each endpoint,
  keyed by HTTP method and path template on REST (for example
  `GET /device/v202504beta2/device/{device.id}`) and by gRPC method on gRPC.
  See [the rate limiting guide](docs/sphinx/guides/rate_limiting.md).
- **`HTTPException.grpc_status_code`** holds the gRPC status name verbatim.
- **Connection reuse.** A `KentikAPI` client uses one HTTP connection for all
  its REST calls. `close()` releases it. A call after `close()` raises
  `ConfigurationError`.
- **Connection retries.** The SDK retries a failed connection attempt twice.
  It never retries a request that reached the server. A call through a proxy
  is not retried, because httpcore does not support retries for proxy
  connections.
- **Proxies.** REST calls honor `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY`, and
  `NO_PROXY` (either case). gRPC already honored the lowercase `https_proxy` and
  `no_proxy`. There is no `proxy=` argument.
- **Schema text in docstrings.** Each client method has the operation summary
  and description from the schema as its docstring. Each model field has the
  schema description. `help()`, editors, and the Sphinx pages show this text.

### Fixed

- **A V5 error keeps the server's error text.** A failed `client.v5` call
  raised a message with only the status code, because the generated error
  classes read only a `message` field. The V5 API sends `{"error": ...}`. The
  message now ends with that text, as in "failed with status code: 400: The
  device_name is required".
- **`KentikAPI.close()` always closes the V5 connection.** When closing the
  main transport raised, the V5 connection stayed open.
- **A 502 for a response that fails its model keeps the call's quota.** On
  REST and gRPC, `exc.rate_limit` was `None` for this error only.
- **`DeviceLookup` fixes.** `count` now counts every device, as iteration
  does; it skipped a second device with a duplicate name. A link without `:`
  raises a `ValueError` that names the expected form, instead of a tuple
  unpacking error. A missing device or interface logs a warning, not a
  critical message.
- **`DFCache` refuses input it cannot handle.** A `step` of zero or less,
  which looped forever, raises `ValueError`. A naive `datetime`, which failed
  later with a `TypeError` against the cached times, raises `ValueError`. A
  cache file name without a UTC offset reads as UTC.
- **A query definition placeholder must be a plain name.** `{start}` and
  `{start:%Y}` work as before. `{start.__class__}` and `{start[0]}` read into
  the values passed in, and now raise `ValueError`.
- **A failed gRPC proto import names its cause.** When a service's proto
  modules failed to import, every gRPC call raised "gRPC proto dependencies
  not installed", even for a descriptor-pool conflict, which needs a different
  fix. The `NotImplementedError` now reads "gRPC proto modules for `<service>`
  service failed to import: `<cause>`" and is chained from the import error.
- **gRPC errors keep the server's error details.** gRPC dropped the
  `google.rpc.Status` that the server sends in a trailer, so a `BadRequest`
  did not say which field it rejected. It is now decoded into
  `exc.details["rpc_status"]`. On REST, `exc.details["rpc_status"]` kept only
  each detail's `@type`, and renamed it `type`. It now holds the full JSON
  body. Both transports give the same dict.
- **gRPC errors report quota from a trailers-only response.** An error with no
  body sends every header as trailing metadata, and the SDK read quota only
  from initial metadata, so a `429` on gRPC could carry no `rate_limit`. Both
  are now read.
- **A space in a REST query value goes out as `%20`.** httpx wrote it as `+`,
  which Envoy's gRPC transcoder does not decode by default, so a value such as
  a journeys `prompt` could reach the service with plus signs. `%20` means a
  space to every server.
- **`APIConfig` and `KentikCredentials` settings are read-only.** The SDK reads
  each setting at a different time: `verify` and `base_path` when the REST
  connection opens, the credentials when the gRPC channel opens, a timeout on
  every call. So a change after construction reached some calls, or none. Each
  assignment now raises `AttributeError`. Use `with_timeout()` for timeouts, or
  build a new `KentikAPI` for anything else.
- **A forked process opens its own REST connection.** After `os.fork()`, for
  example in a multiprocessing worker, the child reused the parent's pooled
  connection, so both processes wrote to one socket. The child now opens a new
  connection on its first REST call. gRPC channels follow gRPC's own fork rules.
- **An empty credential argument raises an error.** `KentikAPI(email="")`
  took the email from the environment or `.env` instead, so a caller whose
  secret lookup returned nothing silently ran as another identity. An `email`
  or `api_token` argument that is empty or only whitespace now raises
  `ConfigurationError`. Omit the argument to read it from the environment.
- **A REST timeout bounds the whole call.** httpx restarts its read timeout on
  every chunk, so a server that kept sending a few bytes held a call with
  `timeout=1.0` open for 11 seconds. A numeric `timeout` or `rest_timeout` is
  now a total deadline: the call raises `TransportError` once the deadline
  passes, at most one read later. A `rest_timeout` given as an `httpx.Timeout`
  keeps httpx's per-phase meaning and sets no total deadline.
- **`Alert.acknowledgement` is the acknowledgement object again.** The
  generator stripped a version prefix, and the enum `v202505AlertAcknowledgement`
  overwrote the object `AlertAcknowledgement`. Any alert with an acknowledgement
  then failed validation. The enum now keeps its prefixed name, and
  `AlertFilters.ackStates` uses `v202505AlertAcknowledgement`. Code that
  imported the enum as `AlertAcknowledgement` must import
  `v202505AlertAcknowledgement`.
- **`oneof` members are optional.** The OpenAPI schema drops the proto `oneof`
  grouping and marks every member as required, so no valid message could pass
  validation. The generator now reads the `oneof` groups from the proto and
  makes their members optional. `ExternalContext.servicenow` and
  `ExternalContext.jiraCloud` are now `Optional`, so alerts with an external
  context parse, and `set_external_context` accepts one context.
  `Nlri.prefix` (`bgp_monitoring`) is now `Optional[str]`.
- **Request bodies send only the fields you set.** REST sent `null` for every
  optional field left unset. On a PATCH, grpc-gateway builds the update mask
  from the body keys, so those nulls cleared the fields. Both transports now
  send exactly the fields set on the model. To clear a field, set it to `None`
  explicitly.
- **Four untyped request bodies are now models.** Their `data` parameter took
  `Dict[str, Any]`, because the schema declares their bodies inline. `data`
  now takes a typed model:
  - `kagent` `upsert_agent_capability`: `AgentCapabilityServiceUpsertAgentCapabilityBody`
  - `kagent` `update_agent`: `AgentServiceUpdateAgentBody`
  - `kagent` `update_capability`:
    `CapabilityAdminServiceUpdateCapabilityBody`
  - `rbux` `update_scope`: `ScopeServiceUpdateScopeBody`
- **A misspelled key or enum value in a gRPC body raises an error.** gRPC
  dropped a body key or enum name the proto does not declare. On a
  full-replace update this blanked the field the caller meant to set, and on a
  PATCH it left the update mask empty, so every field was replaced. gRPC now
  raises `ConfigurationError` that names the bad key before it sends anything.
  Typed request models are not affected: every field they declare exists in
  the proto. Code that passes extra keys in a `Dict[str, Any]` body must remove
  them.
- **A gRPC PATCH updates only the fields you send.** For a PATCH whose body is
  one field, grpc-gateway builds the request's `update_mask` from the keys in
  the REST body. The gRPC call sent an empty mask instead, which updates every
  field and can clear the ones you left out. gRPC now builds the same mask.
  This applies to `client.kagent.update_capability`.
- **A success status with an unusable body raises a 502.** A REST success
  whose body is not JSON raised the operation's error class with the message
  "failed with status code: 200". A JSON `null` body returned an empty model
  that nothing validated. Both now raise `HTTPException` with status 502 and
  a message that names the problem, as a body of the wrong shape already did.
- **A gRPC response that does not match its model raises the same 502 as
  REST.** It raised pydantic's `ValidationError`, outside `KentikError`. One
  cause is an enum value newer than this SDK: the response fails on both
  transports until you upgrade. Catch `HTTPException` (or `KentikError`) for
  it, not `ValidationError`.
- **Responses parse when the server leaves a message field unset.** A proto
  `REQUIRED` field binds the request, not the response, and an unset message
  field is absent from a response. So a policy without a baseline failed
  validation. In models that a response can reach, message fields are now
  `Optional`. Models used only in requests keep them required. Code that reads
  these fields must handle `None`: `FlowPolicySettings.baseline`,
  `FlowPolicySettings.dataset`, `FlowPolicySettings.evaluation`,
  `FlowPolicySettingsDatasetConfig.sources`,
  `FlowPolicySettingsDatasetConfig.filters`,
  `FlowPolicyLevelSettings.activation`, `EventPolicySettings.filters`,
  `EventPolicyLevelSettings.filters` (`alerting`), and
  `GetSecretResponse.secret` (`vault`).
- **A gRPC response over 4 MiB no longer reads as a quota error.** The channel
  now allows 40 MiB, and `KentikAPI(grpc_options=[...])` changes it. A response
  over the limit raises `TransportError`, not `HTTPException` with status 429.
- **`except <Operation>Error` now catches what the operation raises.** Each
  response error class, such as `ListDevicesUnexpectedError`, now extends its
  operation class, `ListDevicesError`, as well as the service class. gRPC now
  raises the same class as REST, with `grpc_status_code` set, where it raised
  the plain `HTTPException` before.
- **gRPC calls reach the right RPC.** In a Service with more than one proto
  service, such as `alerting`, a gRPC call went to whichever service declared
  an RPC of the same name last. For example, deleting an AlertAutoAck called
  `SuppressionService.Delete`. Each call now goes to the RPC that shares its
  REST operation's HTTP rule.
- **`alerting` mitigation operations work on gRPC.** `alerting` has two
  protos named `mitigation.proto`, and the second overwrote the first in
  `pb/`, which lost `MitigationsService`. Its six operations raised
  `NotImplementedError` on gRPC. Proto modules whose names collide inside a
  Service now carry their folder in the name, for example
  `pb/mitigation_public_v202505_pb2.py` and `pb/mitigation_types_v202506_pb2.py`.
  Code that imported `kentik_api.gen.alerting.pb.mitigation_pb2` directly must
  import one of these.
- **gRPC calls send every argument.** Path and query arguments were sent
  under their Python names, which match no proto field, and were dropped.
  For example, `client.device.get_device(deviceid="42")` sent an empty `id`,
  and pagination and filter arguments had no effect. They now set the request
  field that grpc-gateway sets for the same REST call.
- **More operations work on gRPC.** 32 operations that raised
  `NotImplementedError` on gRPC now make the call, because their REST name
  differed from their RPC name.
- **Renamed fields keep their wire name in requests.** A field whose
  Python name differs from its JSON name went out under the Python name.
  For example, a saved filter group's `not_` was sent as `"not_"`, so the
  API ignored the negation, and `protobufAny.type` lost its `@type` key.
  Request bodies now use the JSON names (`not`, `and`, `or`, `in`,
  `from`, `@type`) on REST and gRPC.
- **REST path arguments are encoded.** A path argument went into the URL
  as is, so `client.device.delete_device(deviceid="../../user/7")` sent the
  DELETE to another resource, and a `?` or `#` cut the path short. Each path
  argument is now percent-encoded into its own segment. An empty string, `.`,
  or `..`, which encoding cannot keep in place, raises `ValueError` before the
  SDK sends a request.

### Dependencies

The generated gRPC and protobuf modules refuse to import on older runtimes, so
the declared floors match them:

| Package | Before | After |
| --- | --- | --- |
| `grpcio` | `>=1.78.0` | `>=1.84.0` |
| `protobuf` | not declared | `>=7.35.1,<8` |
| `httpx` | `>=0.28.1` | `>=0.28.1,<1` |
| `python-dotenv` | `>=1.1.1` | `>=1.2.1` |
| `googleapis-common-protos` | `>=1.63.0` | `>=1.73.1` |

### Documentation

- The quickstart, REST, gRPC, error handling, and generation guides are part
  of the published documentation.
- A new [rate limiting guide](docs/sphinx/guides/rate_limiting.md) covers the
  quota headers and the three limits that no header shows.

### Development

This section is for contributors. It does not change the SDK.

- Project tasks run as `uv run poe <task>` on Windows, macOS, and Linux, with
  only uv and Git installed, and Make is no longer used. Each former Make
  target has a poe task with the same name, and each Make variable is now an
  option, for example `uv run poe generate --local` and `--since <ref>`. The
  `services`, `tests`, `install`, `help`, and `local` targets have no task:
  use `generate`, `test`, `uv sync`, bare `uv run poe`, and `--local`.
- CI runs the tests, lint, type check, and the generated-output drift check
  on Windows and macOS as well as Linux.
- [`AGENTS.md`](AGENTS.md) holds the agent instructions. [`CLAUDE.md`](CLAUDE.md) imports it, so it
  also works on a Windows checkout.
