# Draft Jira issues for the Kentik API team

Six draft issues from the community SDK live tests on 2026-10-21, and three
more from 2026-10-26 (issues 7 to 9). Each one was
re-checked with plain `curl` or `grpcurl`, without the SDK. Account: lab
account. Host: `grpc.api.kentik.com`. Schema: `api-schema-public` `9de9a68`,
which is the same as upstream HEAD `8ec5847` for every service below.

To run any curl or grpcurl step, first run the Step 0 setup from
[`upstream-rest-update-body-merge.md`](../upstream/upstream-rest-update-body-merge.md).
It defines `$BASE`, `AUTH`, and `GRPC`.
Every test object name starts with `sdk-e2e-test-`, and every test object was
deleted after the test.

> [!NOTE]
> This is a historical draft snapshot. Use
> [kentik-api-team-findings.md](../kentik-api-team-findings.md) for current
> status. The 2026-10-27 test showed that `UpdateFlowTag` accepts the
> documented body. The earlier claim that every FlowTag write fails is stale.
> AutoAck body parsing also passed the missing-ID validation control. Its
> later `SyntaxError` is a separate issue.

| # | Summary | Transports | Suggested priority |
| --- | --- | --- | --- |
| 1 | REST update ignores the documented camelCase body for AS groups and site markets | REST | High |
| 2 | gRPC calls that set a deadline fail with `RangeError` on six services | gRPC | High |
| 3 | Every flow tag write returns 500 `StatusCodeError` | REST and gRPC | High |
| 4 | CreateSavedFilter with a filter rule returns 500 `ValidationError` | REST | Medium |
| 5 | Custom application: GET of a missing ID returns 200 with an empty object, and DELETE returns 500 | REST | Low |
| 6 | Missing AS group or site market returns 400 `INVALID_ARGUMENT`, not 404 `NOT_FOUND` | REST and gRPC | Low |
| 7 | GET of a missing ID returns 500 on alerting, audit, and vault | REST and gRPC | Medium |
| 8 | A malformed ID returns 500, not 400 | REST and gRPC | Low |
| 9 | kagent capabilities and kmeta ServiceNow operations are published but return 501 | REST and gRPC | Medium |

---

## 1. REST update ignores the documented camelCase body for AS groups and site markets

- **Type:** Bug
- **Components:** to confirm in CORE. Proto service scopes: `admin.as_group` (`ASGroupService`), `admin.site` (`SiteService`)
- **Labels:** `api-v6`, `rest`, `community-sdk`
- **Attachment:** [body-merge report](../upstream/upstream-rest-update-body-merge.md) (full report with every request and response)

### Description

`PUT /as_group/v202212/as_group/{asGroup.id}` and
`PUT /site/v202509/site_markets/{siteMarket.id}` reject the body that the
published OpenAPI document defines. The body wraps the object in its
camelCase JSON name (`asGroup`, `siteMarket`). The server reads only the
proto name (`as_group`, `site_market`). The same update works over gRPC.

### Steps to reproduce

```bash
curl -X POST "$BASE/as_group/v202212/as_group" "${AUTH[@]}" \
  -d '{"asGroup":{"name":"sdk-e2e-test-x","asn":["36459"]}}'           # 200, note the id
curl -X PUT "$BASE/as_group/v202212/as_group/$ID" "${AUTH[@]}" \
  -d '{"asGroup":{"name":"sdk-e2e-test-x","asn":["36459"]}}'           # 400
curl -X PUT "$BASE/as_group/v202212/as_group/$ID" "${AUTH[@]}" \
  -d '{"as_group":{"name":"sdk-e2e-test-x","asn":["36459"]}}'          # 200
curl -X DELETE "$BASE/as_group/v202212/as_group/$ID" "${AUTH[@]}"
```

For site markets, use `/site/v202509/site_markets` with `siteMarket` and
`site_market`. The documented body returns 500.

### Expected

Both spellings reach the same field, as the
[ProtoJSON format](https://protobuf.dev/programming-guides/json/) requires.
The documented body updates the object.

### Actual

- AS group: `400 At path: request.as_group.name -- Expected a string, but received: undefined`.
- Site market: `500 internal error (name:TypeError type:object)`.
- With both keys in one body, the server keeps `as_group` and drops `asGroup` without an error.

### Scope

Of 101 HTTP rules with a body, 4 have this layout. 2 fail (above).
`FlowTagService.UpdateFlowTag` cannot be tested because of issue 3.
`AlertAutoAckService.Replace` (`admin.alerting`) has the same layout and is
not affected.

### Control: AutoAck reads the camelCase body

Re-checked with curl on 2026-10-21 at 23:35 UTC. The ID `999999999` does not
exist, so these requests cannot change data. The error changes with the
content of the camelCase object, so the server reads that object. Both
spellings give the same result.

```bash
P=/v202505/alerts/ack/auto/999999999
curl -X PATCH "$BASE$P" "${AUTH[@]}" -d '{"autoAck":{}}'
# 400 [invalid_argument] must include non null startTime
curl -X PATCH "$BASE$P" "${AUTH[@]}" -d '{"autoAck":{"startTimeAt":"2030-01-01T00:00:00Z"}}'
# 400 [invalid_argument] invalid alarm auto ack request error: rule_id must not be an empty string
curl -X PATCH "$BASE$P" "${AUTH[@]}" -d '{"auto_ack":{"start_time_at":"2030-01-01T00:00:00Z"}}'
# 400, the same rule_id error
curl -X PATCH "$BASE$P" "${AUTH[@]}" -d '{}'
# 400 must include non null startTime
```

This shows that the camelCase body is parsed and validated. It does not show
that an update is saved, because that needs a real auto-ack rule tied to an
alert policy, which we did not create on a shared account. A GET of the same
missing ID returns `500 Could not process the request` (`dbcmvcnzked0068dhcd0`),
not 404.

### Request IDs

`dbckd2czked00d9jjnq0` (UpdateASGroup 400), `dbckd2wsmfx00gt3td1g`
(UpdateSiteMarket 500), `dbcmvcnzked00d9jjzag`, `dbcmvcxsmfx00d9r3p40`,
`dbcmvcxzked00gt87t0g` (AutoAck control).

---

## 2. gRPC calls that set a deadline fail with `RangeError` on six services

- **Type:** Bug
- **Components:** to confirm in CORE. Proto service scopes: `admin.alerting`, `admin.audit`, `admin.custom_application`, `admin.custom_dimension`, `admin.plan`, `admin.saved_filter`
- **Labels:** `api-v6`, `grpc`, `community-sdk`
- **Related:** possibly related to the earlier report "Alerting: the backend needs `startedAt`, and every gRPC RPC returns 500" (2026-10-13). That report has no Jira key that we know of.

### Description

On six services, every gRPC call fails with
`INTERNAL: internal error (name:RangeError type:object)` when the client sets
a deadline. A deadline is the standard `grpc-timeout` request header. The
same calls work without a deadline. Other services, for example `label`,
work with or without one. Most gRPC clients set a deadline on every call,
and the community SDK always sets one. So for these clients, these services
are unusable over gRPC.

### Steps to reproduce

Each pair below makes the same read-only call. The only difference is
`-max-time`, which makes `grpcurl` send `grpc-timeout`.

```bash
"${GRPC[@]}" -proto kentik/alerting/public/v202505/mitigation_method.proto -d '{}' \
  grpc.api.kentik.com:443 kentik.alerting.public.v202505.MitigationMethodsService/List
# OK: {"pagination":{"totalCount":"2"},"methods":[...]}

"${GRPC[@]}" -max-time 30 -proto kentik/alerting/public/v202505/mitigation_method.proto -d '{}' \
  grpc.api.kentik.com:443 kentik.alerting.public.v202505.MitigationMethodsService/List
# ERROR: Code: Internal  Message: internal error (name:RangeError type:object)

"${GRPC[@]}" -max-time 30 -proto kentik/saved_filter/v202501alpha1/saved_filter.proto -d '{}' \
  grpc.api.kentik.com:443 kentik.saved_filter.v202501alpha1.SavedFilterService/ListSavedFilters
# ERROR: RangeError. Without -max-time: OK.

"${GRPC[@]}" -max-time 30 -proto kentik/label/v202210/label.proto -d '{}' \
  grpc.api.kentik.com:443 kentik.label.v202210.LabelService/ListLabels
# OK (control)
```

`-max-time` values of 1, 30, and 300 seconds all fail on every one of the six
services, so the value of the deadline does not matter.

### Live results

Run on 2026-10-21 at 23:59 UTC with `reports/scripts/grpc-deadlines/deadline_checks.sh`. Each
row is the List call of the service with `-d '{}'`.

| Service | No deadline | 1 s | 30 s | 300 s |
| --- | --- | --- | --- | --- |
| alerting (`MitigationMethodsService/List`) | OK | RangeError `dbcn3wqzked0081h4jk0` | RangeError `dbcn3wqzked00d9jk18g` | RangeError `dbcn3wzsmfx00f1gmn50` |
| audit (`ListAuditEvents`) | OK | RangeError `dbcn3x7zked00bhrq860` | RangeError `dbcn3x7smfx009sztybg` | RangeError `dbcn3x7zked004gestg0` |
| custom_application (`ListCustomApplications`) | OK | RangeError `dbcn3xfzked004gestgg` | RangeError `dbcn3xfsmfx009sztyc0` | RangeError `dbcn3xqsmfx0068xvybg` |
| custom_dimension (`ListCustomDimensions`) | OK | RangeError `dbcn3xzsmfx00gt3trf0` | RangeError `dbcn3xzsmfx00bhm1r6g` | RangeError `dbcn3y7zked00bhrq86g` |
| plan (`ListPlans`) | OK | RangeError `dbcn3y7smfx0068xvyc0` | RangeError `dbcn3yfzked00f1h88f0` | RangeError `dbcn3yfsmfx009sztycg` |
| saved_filter (`ListSavedFilters`) | OK | RangeError `dbcn3yqzked009sd2hqg` | RangeError `dbcn3yqsmfx00bhm1r70` | RangeError `dbcn3yzzked004gesth0` |
| label (`ListLabels`), control | OK | OK | OK | OK |

The API team can repeat this with the commands above, or with
`reports/scripts/grpc-deadlines/deadline_checks.sh`.

### Expected

The server honors or ignores `grpc-timeout`, and the call succeeds.

### Actual

Through the community SDK, which always sets a deadline, every read call of
these services that the SDK sent returned `RangeError`:

| Service | Read calls that returned `RangeError` |
| --- | --- |
| alerting | 10 of 14. The SDK did not send the other 4: it rejected the test's placeholder values (text in integer and enum fields) before the call, with `ConfigurationError`. |
| audit | 3 of 3 |
| custom_application | 2 of 2 |
| custom_dimension | 4 of 4 |
| plan | 1 of 1 |
| saved_filter | 3 of 3 |

No read call to these 26 other gRPC services returned `RangeError`:
`ai_advisor`, `as_group`, `asset_tags`, `bgp_monitoring`, `capacity_plan`,
`cloud_export`, `cost`, `credential`, `device`, `dictionary`, `flow_tag`,
`interface`, `journeys`, `kagent`, `kmeta`, `kmi`, `label`, `mkp`,
`network_class`, `nms`, `notification_channel`, `rbux`, `site`,
`synthetics`, `user`, `vault`. Some of these calls failed for other reasons,
for example 404 for a test ID that does not exist.

### Likely cause

Confirmed in the source code and in a local reproduction. Not yet confirmed
in the production logs.

1. In `kentik/ui-app` (branch `develop`, commit `e227e67afd`),
   `createWrapper` in `src/node-lib/api-lib/grpc/server.js` calls
   `impl(camelify(call))` when `wrapperOptions.camelify` is true.
2. `camelify` in `src/shared/util/changeCase.js` copies an object
   recursively with `_.transform` and has no check for cycles.
3. `tsRegister` in `src/servers/util/service/register.ts` always passes
   `{ camelify: true }`. A code search finds `tsRegister(` in exactly six
   files, one for each failing service:
   `src/servers/{alerting/public_v202505,audit/public/v202601,custom_application/v202501alpha1,custom_dimension/v202411alpha1,plan/v202501alpha1,saved_filter/v202501alpha1}/setup.ts`.
4. `label` registers with plain `register(...)` in
   `src/api/packages/servers/src/label/v202210/index.js`, without `camelify`.
   `ai_advisor` calls `register` with `{ camelify: false }` and the comment
   "a grpc-js call is cyclic and must not be transformed".
5. When the client sends `grpc-timeout`, grpc-js stores a
   `call.call.deadlineTimer`. This is a Node `Timeout`, and its
   `_idlePrev` and `_idleNext` links form a cycle. `camelify` follows the
   cycle until the stack overflows: `RangeError: Maximum call stack size
   exceeded`. With no deadline, there is no timer and no cycle.
6. `createWrapper` catches the error, and the response becomes
   `internal error (name:RangeError type:object)`.

Local reproduction (`reports/scripts/grpc-deadlines/camelify_repro.js`): a minimal
grpc-js 1.14.6 server, with lodash 4, runs the same `camelify(call)`. A call
with no deadline succeeds. Calls with 1 s, 30 s, and 300 s deadlines all
fail with `RangeError: Maximum call stack size exceeded`.

Remaining check for the API team: search the node-apiv6 logs for the request
IDs above. The logged stack must show `camelify` and
`Maximum call stack size exceeded`.

Possible fixes, for the API team to choose: register these six services
with `{ camelify: false }`, as `ai_advisor` does, or make `camelify` copy
only the request message and skip the call object.

### Request IDs

See the live results table. Earlier runs: `dbcmdpesmfx00gt3tkkg` (alerting),
`dbcmdppsmfx00d9r3k90` (custom application), `dbcmdtfzked00gt87q00`,
`dbcmdtqsmfx00gt3tkp0`, `dbcmdtzsmfx00gt3tkpg` (saved filter).

---

## 3. Every flow tag write returns 500 `StatusCodeError`

- **Type:** Bug
- **Components:** API (flow_tag v202404alpha1)
- **Labels:** `api-v6`, `rest`, `grpc`, `community-sdk`

### Description

`CreateFlowTag` and `UpdateFlowTag` always return
`500 internal error (name:StatusCodeError type:object)`. This happens over
REST and gRPC, with either body spelling, and with a body that has only a
name. The gRPC call sets no deadline, so the cause is not issue 2. Reads work:
a GET for a missing ID returns a correct 404. On the same account, V5 batch
flow tag upserts work.

### Steps to reproduce

```bash
curl -X POST "$BASE/flow_tag/v202404alpha1/tag" "${AUTH[@]}" \
  -d '{"flowTag":{"name":"sdk-e2e-test-x","ip":{"addresses":["192.0.2.1/32"]}}}'
# HTTP 500 internal error (name:StatusCodeError type:object)

curl -X POST "$BASE/flow_tag/v202404alpha1/tag" "${AUTH[@]}" \
  -d '{"flowTag":{"name":"sdk-e2e-test-x"}}'
# HTTP 500, the same error

"${GRPC[@]}" -proto kentik/flow_tag/v202404alpha1/flow_tag.proto \
  -d '{"flowTag":{"name":"sdk-e2e-test-x","ip":{"addresses":["192.0.2.1/32"]}}}' \
  grpc.api.kentik.com:443 kentik.flow_tag.v202404alpha1.FlowTagService/CreateFlowTag
# ERROR: Code: Internal  Message: internal error (name:StatusCodeError type:object)

curl -X GET "$BASE/flow_tag/v202404alpha1/tag/999999999" "${AUTH[@]}"
# HTTP 404 Flow tag id 999999999 does not exist (control)
```

`UpdateFlowTag` on a missing ID also returns the same 500, not 404.

### Expected

The create returns 200 with the new flow tag. An invalid body returns 400
with the name of the field.

### Actual

500 for every write request.

### Request IDs

`dbcmdbxzked00bhrq35g`, `dbcmdc5zked00d9jjw30` (REST create),
`dbcmdc5smfx00f1gmh10` (gRPC create), `dbck71mzked00d9jjmkg` (REST update).

---

## 4. CreateSavedFilter with a filter rule returns 500 `ValidationError`

- **Type:** Bug
- **Components:** API (saved_filter v202501alpha1)
- **Labels:** `api-v6`, `rest`, `community-sdk`

### Description

`POST /saved-filter/v202501alpha1` succeeds with only a name. It returns
`500 internal error (name:ValidationError type:object)` as soon as the body
has a filter group with a rule. We tried three body layouts and got the same
result each time:

- The minimal one below.
- One with `any`, `not`, `savedFilterIds`, and `nestedFilterGroups` set.
- One that copies the layout of an existing saved filter from
  `ListSavedFilters`, with `filterFieldString`, `metric`, `aggregate`, and
  `rightFilterField`.

### Steps to reproduce

```bash
curl -X POST "$BASE/saved-filter/v202501alpha1" "${AUTH[@]}" -d '{
  "filterName": "sdk-e2e-test-x",
  "filterDescription": "sdk e2e",
  "filterLevel": "FILTER_LEVEL_COMPANY",
  "filters": {"filterGroups": [{"filters": [{
    "filterField": "FILTER_FIELD_INET_DST_ADDR",
    "operator": "FILTER_OPERATOR_EQUAL",
    "filterValue": "192.0.2.1"}]}]}}'
# HTTP 500 internal error (name:ValidationError type:object)

curl -X POST "$BASE/saved-filter/v202501alpha1" "${AUTH[@]}" \
  -d '{"filterName": "sdk-e2e-test-y"}'
# HTTP 200, filter created with no groups (delete it after the test)
```

### Expected

The filter is created. If the body is invalid, the response is 400 and
names the invalid field.

### Actual

500, with no field named.

### Request IDs

`dbcmdcdsmfx00gt3tkfg` (curl), `dbcj9yqzked00d9jje90`, `dbcjak2zked0068dgwag`,
`dbcjawksmfx0081rvfx0` (SDK variants).

---

## 5. Custom application: GET of a missing ID returns 200 with an empty object, and DELETE returns 500

- **Type:** Bug
- **Components:** API (custom_application v202501alpha1)
- **Labels:** `api-v6`, `rest`, `community-sdk`

### Description

A GET for a custom application that was deleted, or that never existed,
returns 200 with every field empty. A DELETE of an application that was
already deleted returns 500. A client cannot tell "not found" from a real
object without checking for an empty `id`.

### Steps to reproduce

```bash
curl -X POST "$BASE/custom_application/v202501alpha1" "${AUTH[@]}" \
  -d '{"name":"sdk-e2e-test-x","ipRange":["192.0.2.0/24"],"protocol":[6],"port":[8443]}'
# HTTP 200, note the id
curl -X DELETE "$BASE/custom_application/v202501alpha1/$ID" "${AUTH[@]}"       # HTTP 200
curl -X GET "$BASE/custom_application/v202501alpha1/$ID" "${AUTH[@]}"
# HTTP 200 {"application":{"id":"","name":"","description":"","ipRange":[],"protocol":[],"port":[],"asn":[],"userId":""}}
curl -X GET "$BASE/custom_application/v202501alpha1/999999999" "${AUTH[@]}"
# HTTP 200, the same empty object
curl -X DELETE "$BASE/custom_application/v202501alpha1/$ID" "${AUTH[@]}"
# HTTP 500 internal error
```

### Expected

GET and DELETE of a missing ID return 404 `NOT_FOUND`, as the flow tag
service does.

### Actual

GET returns 200 with an empty object. A second DELETE returns 500.

---

## 6. Missing AS group or site market returns 400 `INVALID_ARGUMENT`, not 404 `NOT_FOUND`

- **Type:** Improvement
- **Components:** API (as_group, site)
- **Labels:** `api-v6`, `rest`, `grpc`, `community-sdk`

### Description

A GET for a missing AS group or site market returns 400 with gRPC code 3
(`INVALID_ARGUMENT`). Flow tag returns 404 with code 5 (`NOT_FOUND`) for the
same case. A client cannot tell a bad request from a missing object by the
status code.

### Steps to reproduce

```bash
curl -X GET "$BASE/site/v202509/site_markets/999999999" "${AUTH[@]}"
# HTTP 400 {"code":3,"message":"Site Market with id '999999999' does not exist ..."}
curl -X GET "$BASE/as_group/v202212/as_group/1" "${AUTH[@]}"
# HTTP 400 {"code":3,"message":"AS group with id '1' does not exist ..."}
curl -X GET "$BASE/flow_tag/v202404alpha1/tag/999999999" "${AUTH[@]}"
# HTTP 404 {"code":5,...} (control)
```

### Expected

404 and code 5 (`NOT_FOUND`) for a missing object.

### Actual

400 and code 3 (`INVALID_ARGUMENT`).

### Note

Twice, during SDK tests on 2026-10-21, a GET right after a successful update
reported an existing site market as missing. It returned 400
`Site Market with id ... does not exist` (`dbcm6q2smfx0081rvpn0`), and the
same object was readable a second later. 15 immediate reads after updates in
a later run did not show this. If you see it again, it can be a separate
read-after-write issue.

### Request IDs

`dbcmdedsmfx00f1gmh1g` (site market), `dbcm6yvsmfx0081rvpq0` (AS group).

---

## 7. GET of a missing ID returns 500 on alerting, audit, and vault

- **Type:** Bug
- **Components:** API (alerting v202505, audit v202601, vault v202312alpha1)
- **Labels:** `api-v6`, `rest`, `grpc`, `community-sdk`

### Description

A read of an ID that does not exist returns 500 `INTERNAL` on these
operations, over REST and gRPC. Other operations of the same services return
a correct 404 for the same ID, for example `GET /v202505/policies/...` and
`GET /v202505/mitigations/{id}/actions`. A client cannot tell "not found"
from a server failure, and a client that retries on 5xx retries a request
that can never succeed.

### Steps to reproduce

Read-only. The ID `999999999` does not exist.

```bash
curl "$BASE/v202505/alerts/ack/auto/999999999" "${AUTH[@]}"
# 500 Could not process the request. Please try again.
curl "$BASE/v202505/alerts/silence/999999999" "${AUTH[@]}"                 # 500, same
curl "$BASE/v202505/suppressions/999999999" "${AUTH[@]}"                   # 500, same
curl "$BASE/v202505/alerts/999999999/comments" "${AUTH[@]}"
# 500 Couldn't list comments. Please try again.
curl "$BASE/audit/v202601/events/999999999" "${AUTH[@]}"
# 500 internal error (name:Error type:object)
curl "$BASE/audit/v202601/events/999999999/2024-01-01T00:00:00Z" "${AUTH[@]}" # 500, same
curl "$BASE/vault/v202312alpha1/secrets/999999999" "${AUTH[@]}"            # 500, same
curl "$BASE/vault/v202312alpha1/secrets?names=999999999" "${AUTH[@]}"      # 500, same

curl "$BASE/v202505/policies/POLICY_TYPE_PROTECT/999999999" "${AUTH[@]}"
# 404 Policy not found (control)
```

### Expected

404 `NOT_FOUND` for a missing object. For `ListSecret` with an unknown name,
either 404 or 200 with an empty list.

### Actual

500 `INTERNAL` (code 13).

### Request IDs

Run on 2026-10-26 at 15:57 UTC: `dbfqgmtzked00d968jp0` (auto-ack),
`dbfqgmt4p3k009sr1gsg` (silence), `dbfqgna4p3k009sr1gvg` (suppression),
`dbfqgmt4p3k009sr1gt0` (comments), `dbfqgpjzked009s8hz1g` and
`dbfqgqj4p3k00818xf60` (audit), `dbfqgqt4p3k004g4r9kg` and
`dbfqgqt4p3k00bhv13pg` (vault).

---

## 8. A malformed ID returns 500, not 400

- **Type:** Improvement
- **Components:** API (alerting v202505, custom_application v202501alpha1, kmi v202212)
- **Labels:** `api-v6`, `rest`, `grpc`, `community-sdk`

### Description

These path fields are strings in the proto, but the server expects a number.
A value that is not a number reaches the handler and fails there with 500.
Where the proto field is `int64`, the gateway already returns a correct 400,
for example `GET /audit/v202601/events/not-a-number` returns
`400 id: invalid value "not-a-number" for type TYPE_INT64`.

### Steps to reproduce

Read-only.

```bash
curl "$BASE/v202505/mitigations/action_value" "${AUTH[@]}"
# 500 internal error (name:SyntaxError type:object)
curl "$BASE/v202505/policies/POLICY_TYPE_PROTECT/id_value" "${AUTH[@]}"
# 500 internal error (name:SyntaxError type:object)
curl "$BASE/custom_application/v202501alpha1/not-a-number" "${AUTH[@]}"
# 500 internal error (name:error type:object)
curl "$BASE/kmi/v202212/insights/not-a-number" "${AUTH[@]}"
# 500 internal error (name:error type:object)

curl "$BASE/v202505/mitigations/999999999" "${AUTH[@]}"
# 404 (control: a number that does not exist)
```

The same reads over gRPC also return `INTERNAL`.

### Expected

400 `INVALID_ARGUMENT` that names the field.

### Actual

500 `INTERNAL`.

### Request IDs

`dbfqh0w4p3k009sr1gy0` (mitigation), `dbfqh0w4p3k004g4r9q0` (policy),
`dbfqgrvzked008179k40` (custom application), `dbfqgrv4p3k004g4r9m0` (kmi).

---

## 9. kagent capabilities and kmeta ServiceNow operations are published but return 501

- **Type:** Bug
- **Components:** API (kagent v202401, kmeta v202607alpha1), schema publication
- **Labels:** `api-v6`, `rest`, `grpc`, `community-sdk`

### Description

`api-schema-public` publishes these operations, so the SDK generates client
methods for them. The server returns 501 `UNIMPLEMENTED` for each one, over
REST and gRPC:

- `kentik.kagent.v202401.CapabilityAdminService/ListCapabilities`
- `kentik.kagent.v202401.CapabilityAdminService/GetCapability`
- `kentik.kmeta.v202607alpha1.KmetaService/ListServiceNowConfigs`
- `kentik.kmeta.v202607alpha1.KmetaService/GetServiceNowConfig`

### Steps to reproduce

```bash
curl "$BASE/kagent/v202401/capabilities" "${AUTH[@]}"
# 501 The server does not implement the method /kentik.kagent.v202401.CapabilityAdminService/ListCapabilities
curl "$BASE/kmeta/v202607alpha1/1/servicenow/config" "${AUTH[@]}"
# 501 The server does not implement the method /kentik.kmeta.v202607alpha1.KmetaService/ListServiceNowConfigs
```

### Expected

Either the server implements the operations, or the public schema does not
publish them until it does.

### Actual

501 for every call.
