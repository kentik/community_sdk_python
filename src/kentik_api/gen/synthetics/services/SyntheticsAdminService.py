# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    CreateAgentAlertError,
    CreateTestError,
    DeleteAgentAlertError,
    DeleteAgentError,
    DeleteTestError,
    GetAgentAlertError,
    GetAgentError,
    GetTestError,
    ListAgentAlertsError,
    ListAgentsError,
    ListTestsError,
    SetTestStatusError,
    UpdateAgentAlertError,
    UpdateAgentError,
    UpdateTestError,
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


def ListAgentAlerts(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentIds: Optional[List[str]] = None,
) -> ListAgentAlertsResponse:
    """
    List agent alert configurations

    Lists all agent alert configurations, optionally filtered by a list of agent ids.
    """
    query_params: Dict[str, Any] = {"agentIds": agentIds}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/synthetics/v202309/agentAlerts",
        path_template="/synthetics/v202309/agentAlerts",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAgentAlerts",
        error_cls=ListAgentAlertsError,
    )

    return parse_response_model(
        ListAgentAlertsResponse,
        body,
        operation_name="ListAgentAlerts",
        method="get",
        path="/synthetics/v202309/agentAlerts",
    )


def CreateAgentAlert(
    api_config_override: Optional[APIConfig] = None, *, data: CreateAgentAlertRequest
) -> CreateAgentAlertResponse:
    """
    Create an agent alert configuration

    Creates a new agent alert configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v202309/agentAlerts",
        path_template="/synthetics/v202309/agentAlerts",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateAgentAlert",
        error_cls=CreateAgentAlertError,
    )

    return parse_response_model(
        CreateAgentAlertResponse,
        body,
        operation_name="CreateAgentAlert",
        method="post",
        path="/synthetics/v202309/agentAlerts",
    )


def GetAgentAlert(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetAgentAlertResponse:
    """
    Get an agent alert configuration

    Retrieves an existing agent alert configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/synthetics/v202309/agentAlerts/{path_segment(id)}",
        path_template="/synthetics/v202309/agentAlerts/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAgentAlert",
        error_cls=GetAgentAlertError,
    )

    return parse_response_model(
        GetAgentAlertResponse,
        body,
        operation_name="GetAgentAlert",
        method="get",
        path="/synthetics/v202309/agentAlerts/{id}",
    )


def UpdateAgentAlert(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: SyntheticsAdminServiceUpdateAgentAlertBody,
) -> UpdateAgentAlertResponse:
    """
    Update an agent alert configuration

    Updates an existing agent alert configuration with the time threshold and notification channels provided.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/synthetics/v202309/agentAlerts/{path_segment(id)}",
        path_template="/synthetics/v202309/agentAlerts/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateAgentAlert",
        error_cls=UpdateAgentAlertError,
    )

    return parse_response_model(
        UpdateAgentAlertResponse,
        body,
        operation_name="UpdateAgentAlert",
        method="put",
        path="/synthetics/v202309/agentAlerts/{id}",
    )


def DeleteAgentAlert(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteAgentAlertResponse:
    """
    Delete an agent alert configuration

    Deletes an existing agent alert configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/synthetics/v202309/agentAlerts/{path_segment(id)}",
        path_template="/synthetics/v202309/agentAlerts/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteAgentAlert",
        error_cls=DeleteAgentAlertError,
    )

    return parse_response_model(
        DeleteAgentAlertResponse,
        body,
        operation_name="DeleteAgentAlert",
        method="delete",
        path="/synthetics/v202309/agentAlerts/{id}",
    )


def ListAgents(api_config_override: Optional[APIConfig] = None) -> ListAgentsResponse:
    """
    List available agents

    Returns list of all synthetic agents available in the account.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/synthetics/v202309/agents",
        path_template="/synthetics/v202309/agents",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListAgents",
        error_cls=ListAgentsError,
    )

    return parse_response_model(
        ListAgentsResponse,
        body,
        operation_name="ListAgents",
        method="get",
        path="/synthetics/v202309/agents",
    )


def GetAgent(
    api_config_override: Optional[APIConfig] = None, *, agentid: str
) -> GetAgentResponse:
    """
    Get information about an agent

    Returns information about the requested synthetic agent.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/synthetics/v202309/agents/{path_segment(agentid)}",
        path_template="/synthetics/v202309/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetAgent",
        error_cls=GetAgentError,
    )

    return parse_response_model(
        GetAgentResponse,
        body,
        operation_name="GetAgent",
        method="get",
        path="/synthetics/v202309/agents/{agent.id}",
    )


def UpdateAgent(
    api_config_override: Optional[APIConfig] = None,
    *,
    agentid: str,
    data: SyntheticsAdminServiceUpdateAgentBody,
) -> UpdateAgentResponse:
    """
    Update configuration of an agent

    Update configuration of a synthetic agent.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/synthetics/v202309/agents/{path_segment(agentid)}",
        path_template="/synthetics/v202309/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateAgent",
        error_cls=UpdateAgentError,
    )

    return parse_response_model(
        UpdateAgentResponse,
        body,
        operation_name="UpdateAgent",
        method="put",
        path="/synthetics/v202309/agents/{agent.id}",
    )


def DeleteAgent(
    api_config_override: Optional[APIConfig] = None, *, agentid: str
) -> DeleteAgentResponse:
    """
    Delete an agent

    Deletes the requested agent. The deleted agent is removed from configuration of all tests.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/synthetics/v202309/agents/{path_segment(agentid)}",
        path_template="/synthetics/v202309/agents/{agent.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteAgent",
        error_cls=DeleteAgentError,
    )

    return parse_response_model(
        DeleteAgentResponse,
        body,
        operation_name="DeleteAgent",
        method="delete",
        path="/synthetics/v202309/agents/{agent.id}",
    )


def ListTests(api_config_override: Optional[APIConfig] = None) -> ListTestsResponse:
    """
    List all tests

    Returns a list of all configured active and paused synthetic tests.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/synthetics/v202309/tests",
        path_template="/synthetics/v202309/tests",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="ListTests",
        error_cls=ListTestsError,
    )

    return parse_response_model(
        ListTestsResponse,
        body,
        operation_name="ListTests",
        method="get",
        path="/synthetics/v202309/tests",
    )


def CreateTest(
    api_config_override: Optional[APIConfig] = None, *, data: CreateTestRequest
) -> CreateTestResponse:
    """
    Create a test

    Create synthetic test based on configuration provided in the request.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/synthetics/v202309/tests",
        path_template="/synthetics/v202309/tests",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="CreateTest",
        error_cls=CreateTestError,
    )

    return parse_response_model(
        CreateTestResponse,
        body,
        operation_name="CreateTest",
        method="post",
        path="/synthetics/v202309/tests",
    )


def GetTest(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> GetTestResponse:
    """
    Get information about a test

    Returns configuration and status for the requested synthetic test.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/synthetics/v202309/tests/{path_segment(id)}",
        path_template="/synthetics/v202309/tests/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="GetTest",
        error_cls=GetTestError,
    )

    return parse_response_model(
        GetTestResponse,
        body,
        operation_name="GetTest",
        method="get",
        path="/synthetics/v202309/tests/{id}",
    )


def UpdateTest(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: SyntheticsAdminServiceUpdateTestBody,
) -> UpdateTestResponse:
    """
    Update configuration of a test

    Updates configuration of a synthetic test.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/synthetics/v202309/tests/{path_segment(id)}",
        path_template="/synthetics/v202309/tests/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="UpdateTest",
        error_cls=UpdateTestError,
    )

    return parse_response_model(
        UpdateTestResponse,
        body,
        operation_name="UpdateTest",
        method="put",
        path="/synthetics/v202309/tests/{id}",
    )


def DeleteTest(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> DeleteTestResponse:
    """
    Delete a synthetic test.

    Deletes the synthetics test. All accumulated results for the test cease to be accessible.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/synthetics/v202309/tests/{path_segment(id)}",
        path_template="/synthetics/v202309/tests/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="DeleteTest",
        error_cls=DeleteTestError,
    )

    return parse_response_model(
        DeleteTestResponse,
        body,
        operation_name="DeleteTest",
        method="delete",
        path="/synthetics/v202309/tests/{id}",
    )


def SetTestStatus(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: SyntheticsAdminServiceSetTestStatusBody,
) -> SetTestStatusResponse:
    """
    Update status of a synthetic test
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="put",
        path=f"/synthetics/v202309/tests/{path_segment(id)}/status",
        path_template="/synthetics/v202309/tests/{id}/status",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="SetTestStatus",
        error_cls=SetTestStatusError,
    )

    return parse_response_model(
        SetTestStatusResponse,
        body,
        operation_name="SetTestStatus",
        method="put",
        path="/synthetics/v202309/tests/{id}/status",
    )
