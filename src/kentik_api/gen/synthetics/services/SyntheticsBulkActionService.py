# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import BulkUpdateTestsError, GetBulkUpdateTestsStatusError
from ..models import (  # noqa: F401
    ActivationSettings,
    Agent,
    AgentAlert,
    AgentMetadata,
    AgentMetadataIpValue,
    AgentResults,
    AgentStatus,
    AgentTest,
    AlertingSettings,
    AlertingType,
    BulkActionItemState,
    BulkActionItemStatus,
    BulkActionState,
    BulkActionStatus,
    BulkFieldOp,
    BulkFieldOpRule,
    BulkUpdateTestsRequest,
    BulkUpdateTestsResponse,
    CreateAgentAlertRequest,
    CreateAgentAlertResponse,
    CreateTestRequest,
    CreateTestResponse,
    DeleteAgentAlertResponse,
    DeleteAgentResponse,
    DeleteTestResponse,
    DisabledMetrics,
    DNSRecord,
    DNSResponseData,
    DNSResults,
    DnsTest,
    FlowTest,
    GetAgentAlertResponse,
    GetAgentResponse,
    GetBulkUpdateTestsStatusResponse,
    GetResultsForTestsCsvRequest,
    GetResultsForTestsCsvResponse,
    GetResultsForTestsRequest,
    GetResultsForTestsResponse,
    GetTestResponse,
    GetTraceForTestRequest,
    GetTraceForTestResponse,
    GroupedAlertSetting,
    GroupedAlertSettings,
    HealthSettings,
    HostnameTest,
    HTTPResponseData,
    HTTPResults,
    ImplementType,
    IPFamily,
    IpTest,
    ListAgentAlertsResponse,
    ListAgentsResponse,
    ListTestsResponse,
    Location,
    MetricData,
    NetNode,
    NetworkMeshTest,
    PacketLossData,
    PageLoadTest,
    Path,
    PathTrace,
    PingResults,
    ScheduleSettings,
    SetTestStatusResponse,
    SrcGroupBy,
    Stats,
    SyntheticsAdminServiceSetTestStatusBody,
    SyntheticsAdminServiceUpdateAgentAlertBody,
    SyntheticsAdminServiceUpdateAgentBody,
    SyntheticsAdminServiceUpdateTestBody,
    TaskResults,
    Test,
    TestPingSettings,
    TestResults,
    TestSettings,
    TestStatus,
    TestThroughputSettings,
    TestTraceSettings,
    TraceHop,
    UpdateAgentAlertResponse,
    UpdateAgentResponse,
    UpdateTestResponse,
    UrlTest,
    UserInfo,
    protobufAny,
    rpcStatus,
    v202309ActivationSettings,
    v202309AgentTest,
    v202309AlertingSettings,
    v202309AlertingType,
    v202309DisabledMetrics,
    v202309DNSRecord,
    v202309DnsTest,
    v202309FlowTest,
    v202309GroupedAlertSetting,
    v202309GroupedAlertSettings,
    v202309HealthSettings,
    v202309HostnameTest,
    v202309IPFamily,
    v202309IpTest,
    v202309NetworkMeshTest,
    v202309PageLoadTest,
    v202309ScheduleSettings,
    v202309SrcGroupBy,
    v202309Test,
    v202309TestPingSettings,
    v202309TestSettings,
    v202309TestStatus,
    v202309TestThroughputSettings,
    v202309TestTraceSettings,
    v202309UrlTest,
)


def BulkUpdateTests(
    api_config_override: Optional[APIConfig] = None, *, data: BulkUpdateTestsRequest
) -> BulkUpdateTestsResponse:
    """
    Update multiple synthetic tests

    Applies the same attribute changes to up to 50 synthetic tests. Only some attributes can be bulk-updated, and some can be changed only on certain test types or only together with another attribute. Tests are validated first; by default, if any test fails validation no test is updated (see `allow_partial_batch`). Tests that pass are then updated asynchronously: the reply carries the initial status and, if anything was started, a `workflow_id` to pass to GetBulkUpdateTestsStatus. Fails with INVALID_ARGUMENT (HTTP 400) if the request is malformed, such as no IDs, more than 50 IDs, no attributes to update, an attribute that cannot be bulk-updated, or an attribute that does not apply to every selected test's type; RESOURCE_EXHAUSTED (HTTP 429) if the company lacks the synthetics credits for the change; and UNKNOWN (HTTP 500) if the update could not be confirmed as started. After UNKNOWN the update may still run, so check the tests before retrying.

    ### Bulk-updatable attributes
    Paths are relative to `test` and shown in JSON (camelCase) form. snake_case is also accepted, and error messages report paths in snake_case.

    | Path | Notes |
    |------|-------|
    | `name` | |
    | `status` | `TEST_STATUS_ACTIVE` or `TEST_STATUS_PAUSED` |
    | `settings.period` | |
    | `settings.agentIds` | supports ADD and REMOVE |
    | `settings.healthSettings.activation.times` | |
    | `settings.healthSettings.activation.timeWindow` | |
    | `settings.healthSettings.activation.gracePeriod` | |
    | `settings.healthSettings.latencyCritical`, `latencyWarning` | set together |
    | `settings.healthSettings.latencyCriticalStddev`, `latencyWarningStddev` | set together; also sets `latencyCritical` and `latencyWarning` to 0 |
    | `settings.healthSettings.jitterCritical`, `jitterWarning` | set together |
    | `settings.healthSettings.jitterCriticalStddev`, `jitterWarningStddev` | set together; also sets `jitterCritical` and `jitterWarning` to 0 |
    | `settings.healthSettings.packetLossCritical`, `packetLossWarning` | set together |
    | `settings.ip.targets` | supports ADD and REMOVE |
    | `settings.networkGrid.targets` | supports ADD and REMOVE |
    | `settings.dns.servers` | supports ADD and REMOVE |
    | `settings.dns.target` | |
    | `settings.dnsGrid.servers` | supports ADD and REMOVE |
    | `settings.dnsGrid.target` | |
    | `settings.hostname.target` | |
    | `settings.url.target` | |
    | `settings.pageLoad.target` | |
    | `settings.agent.target` | |

    A threshold pair and its Stddev pair cannot be set in the same request.

    ### Examples
    Change the period of several tests:
    ```json
    {"ids": ["101", "102"], "test": {"settings": {"period": 300}}}
    ```
    Add an agent to each test, keeping the agents already assigned. In JSON, a field mask is a single comma-separated string:
    ```json
    {"ids": ["101", "102"], "test": {"settings": {"agentIds": ["55"]}},
    "ops": [{"mask": "settings.agentIds", "op": "BULK_FIELD_OP_ADD"}]}
    ```
    Set attributes to zero. A zero value cannot be told apart from an unset one, so `mask` must name it:
    ```json
    {"ids": ["101"], "test": {"settings": {"healthSettings": {"jitterCritical": 0, "jitterWarning": 0}}},
    "mask": "settings.healthSettings.jitterCritical,settings.healthSettings.jitterWarning"}
    ```
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v20261005alpha1/tests/bulk_update",
        path_template="/synthetics/v20261005alpha1/tests/bulk_update",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="BulkUpdateTests",
        error_cls=BulkUpdateTestsError,
    )

    return parse_response_model(
        BulkUpdateTestsResponse,
        body,
        operation_name="BulkUpdateTests",
        method="post",
        path="/synthetics/v20261005alpha1/tests/bulk_update",
    )


def GetBulkUpdateTestsStatus(
    api_config_override: Optional[APIConfig] = None, *, workflowId: str
) -> GetBulkUpdateTestsStatusResponse:
    """
    Get status of a bulk test update

    Returns the current state and per-test outcome of a bulk update started by BulkUpdateTests. When `end_time` is set, the bulk update has finished and its status will not change. Items skipped before the update started are reported only in the BulkUpdateTests reply. Status is kept for a limited time after a bulk update finishes, so read it soon after `end_time` is set. Fails with NOT_FOUND (HTTP 404) if the workflow ID is unknown, the bulk update was started by a different user, or its status is no longer kept.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/synthetics/v20261005alpha1/tests/bulk_update/{path_segment(workflowId)}",
        path_template="/synthetics/v20261005alpha1/tests/bulk_update/{workflowId}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetBulkUpdateTestsStatus",
        error_cls=GetBulkUpdateTestsStatusError,
    )

    return parse_response_model(
        GetBulkUpdateTestsStatusResponse,
        body,
        operation_name="GetBulkUpdateTestsStatus",
        method="get",
        path="/synthetics/v20261005alpha1/tests/bulk_update/{workflowId}",
    )
