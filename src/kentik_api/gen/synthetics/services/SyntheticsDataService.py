# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import parse_response_model, request_json

from ..error import (
    GetResultsForTestsCsvError,
    GetResultsForTestsError,
    GetTraceForTestError,
)
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


def GetResultsForTests(
    api_config_override: Optional[APIConfig] = None, *, data: GetResultsForTestsRequest
) -> GetResultsForTestsResponse:
    """
    Get results for tests

    Returns probe results for a set of tests for specified period of time.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v202309/results",
        path_template="/synthetics/v202309/results",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetResultsForTests",
        error_cls=GetResultsForTestsError,
    )

    return parse_response_model(
        GetResultsForTestsResponse,
        body,
        operation_name="GetResultsForTests",
        method="post",
        path="/synthetics/v202309/results",
    )


def GetResultsForTestsCsv(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: GetResultsForTestsCsvRequest,
) -> GetResultsForTestsCsvResponse:
    """
    Get test results in CSV format

    Returns probe results for tests in CSV format.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v202309/results/csv",
        path_template="/synthetics/v202309/results/csv",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetResultsForTestsCsv",
        error_cls=GetResultsForTestsCsvError,
    )

    return parse_response_model(
        GetResultsForTestsCsvResponse,
        body,
        operation_name="GetResultsForTestsCsv",
        method="post",
        path="/synthetics/v202309/results/csv",
    )


def GetTraceForTest(
    api_config_override: Optional[APIConfig] = None, *, data: GetTraceForTestRequest
) -> GetTraceForTestResponse:
    """
    Get network trace data for a test

    Get network trace data for a specific synthetic test. The test must have traceroute task configured.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v202309/trace",
        path_template="/synthetics/v202309/trace",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="GetTraceForTest",
        error_cls=GetTraceForTestError,
    )

    return parse_response_model(
        GetTraceForTestResponse,
        body,
        operation_name="GetTraceForTest",
        method="post",
        path="/synthetics/v202309/trace",
    )
