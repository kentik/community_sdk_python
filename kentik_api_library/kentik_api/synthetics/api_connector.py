import functools
from typing import Any, Callable, List, Optional

from google.protobuf.timestamp_pb2 import Timestamp
from grpc import RpcError, StatusCode
from grpc._channel import _InactiveRpcError

import kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2 as pb
from kentik_api.generated.kentik.synthetics.v202202.synthetics_pb2_grpc import (
    SyntheticsAdminService,
    SyntheticsDataService,
)
from kentik_api.public.errors import (
    AuthError,
    BadRequestError,
    KentikAPIError,
    NotFoundError,
    ProtocolError,
    TimedOutError,
    UnavailabilityError,
)


def wrap_grpc_errors(func: Callable) -> Callable:
    """Wrap GRPC error into KentikAPIError"""

    @functools.wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except RpcError as error:
            raise new_api_error(error) from error

    return inner


class APISyntheticsConnector:
    """
    APISyntheticsConnector implements APISyntheticsConnectorProtocol.
    Allows sending authorized grpc requests to Kentik Synthetics API
    """

    def __init__(self, api_url: str, auth_email: str, auth_token: str):
        self._url = api_url
        self._admin = SyntheticsAdminService()
        self._data = SyntheticsDataService()
        self._credentials = [
            ("x-ch-auth-email", auth_email),
            ("x-ch-auth-api-token", auth_token),
        ]

    @wrap_grpc_errors
    def get_all_agents(self) -> List[pb.Agent]:
        request = pb.ListAgentsRequest()
        agents = self._admin.ListAgents(request=request, metadata=self._credentials, target=self._url).agents
        return [agent for agent in agents]  # convert from protobuf internal container type to list

    @wrap_grpc_errors
    def get_agent(self, agent_id: str) -> pb.Agent:
        request = pb.GetAgentRequest(id=agent_id)
        return self._admin.GetAgent(request=request, metadata=self._credentials, target=self._url).agent

    @wrap_grpc_errors
    def update_agent(self, agent: pb.Agent) -> pb.Agent:
        request = pb.UpdateAgentRequest(agent=agent)
        return self._admin.UpdateAgent(request=request, metadata=self._credentials, target=self._url).agent

    @wrap_grpc_errors
    def delete_agent(self, agent_id: str) -> None:
        request = pb.DeleteAgentRequest(id=agent_id)
        self._admin.DeleteAgent(request=request, metadata=self._credentials, target=self._url)

    @wrap_grpc_errors
    def get_all_tests(self) -> List[pb.Test]:
        request = pb.ListTestsRequest()
        tests = self._admin.ListTests(request=request, metadata=self._credentials, target=self._url).tests
        return [test for test in tests]  # convert from protobuf internal container type to list

    @wrap_grpc_errors
    def get_test(self, test_id: str) -> pb.Test:
        request = pb.GetTestRequest(id=test_id)
        return self._admin.GetTest(request=request, metadata=self._credentials, target=self._url).test

    @wrap_grpc_errors
    def create_test(self, test: pb.Test) -> pb.Test:
        test.ClearField("id")  # CreateTestRequest doesn't accept id
        request = pb.CreateTestRequest(test=test)
        return self._admin.CreateTest(request=request, metadata=self._credentials, target=self._url).test

    @wrap_grpc_errors
    def update_test(self, test: pb.Test) -> pb.Test:
        request = pb.UpdateTestRequest(test=test)
        return self._admin.UpdateTest(request=request, metadata=self._credentials, target=self._url).test

    @wrap_grpc_errors
    def delete_test(self, test_id: str) -> None:
        request = pb.DeleteTestRequest(id=test_id)
        self._admin.DeleteTest(request=request, metadata=self._credentials, target=self._url)

    @wrap_grpc_errors
    def test_status_update(self, test_id: str, status: pb.TestStatus) -> None:
        request = pb.SetTestStatusRequest(id=test_id, status=status)
        self._admin.SetTestStatus(request=request, metadata=self._credentials, target=self._url)

    @wrap_grpc_errors
    def results_for_tests(
        self,
        test_ids: List[str],
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        task_ids: Optional[List[str]] = None,
    ) -> pb.GetResultsForTestsResponse:
        request = pb.GetResultsForTestsRequest(
            ids=test_ids,
            start_time=start,
            end_time=end,
            agent_ids=agent_ids or [],
            targets=task_ids or [],
        )
        return self._data.GetResultsForTests(request=request, metadata=self._credentials, target=self._url)

    @wrap_grpc_errors
    def trace_for_test(
        self,
        test_id: str,
        start: Timestamp,
        end: Timestamp,
        agent_ids: Optional[List[str]] = None,
        target_ips: Optional[List[str]] = None,
    ) -> pb.GetTraceForTestResponse:
        request = pb.GetTraceForTestRequest(
            id=test_id,
            start_time=start,
            end_time=end,
            agent_ids=agent_ids or [],
            target_ips=target_ips or [],
        )
        return self._data.GetTraceForTest(request=request, metadata=self._credentials, target=self._url)


def new_api_error(error: RpcError) -> KentikAPIError:
    """Create API error from gRPC error"""

    PROTOCOL_GRPC = "gRPC"

    if not isinstance(error, _InactiveRpcError):
        return KentikAPIError(str(error))

    # _InactiveRpcError holds error code details
    code: StatusCode = error.code()
    status_code, status_name = code.value

    if code == StatusCode.INVALID_ARGUMENT:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.DEADLINE_EXCEEDED:
        return TimedOutError(f"grpc_status: {status_code} - '{status_name}'")
    if code == StatusCode.NOT_FOUND:
        return NotFoundError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.ALREADY_EXISTS:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.PERMISSION_DENIED:
        return AuthError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.UNIMPLEMENTED:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.UNAVAILABLE:
        return UnavailabilityError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.UNAUTHENTICATED:
        return AuthError(PROTOCOL_GRPC, status_code, status_name)

    # StatusCode.CANCELLED
    # StatusCode.UNKNOWN
    # StatusCode.FAILED_PRECONDITION
    # StatusCode.ABORTED
    # StatusCode.OUT_OF_RANGE
    # StatusCode.INTERNAL
    # StatusCode.DATA_LOSS
    return ProtocolError(PROTOCOL_GRPC, status_code, status_name)
