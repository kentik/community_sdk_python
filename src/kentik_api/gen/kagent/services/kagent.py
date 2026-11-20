from typing import List, Optional, Union, cast

import kentik_api.gen.kagent.services.AgentCapabilityService as RestKagentModule1
import kentik_api.gen.kagent.services.AgentService as RestKagentModule2
import kentik_api.gen.kagent.services.CapabilityAdminService as RestKagentModule3
import kentik_api.gen.kagent.services.CapabilityReleaseService as RestKagentModule4
import kentik_api.gen.kagent.services.ConfigService as RestKagentModule5
import kentik_api.gen.kagent.services.ProvisioningTokenService as RestKagentModule6
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.kagent import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class KagentServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.agent_capabilities_pb2 as _pb2_1_mod
                import kentik_api.gen.kagent.pb.agent_capabilities_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.AgentCapabilityServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.agent_pb2 as _pb2_2_mod
                import kentik_api.gen.kagent.pb.agent_pb2_grpc as _pb2_grpc_2_mod

                self._grpc_pb2_2 = _pb2_2_mod
                self._grpc_stub_2 = _pb2_grpc_2_mod.AgentServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_2 = None
                self._grpc_stub_2 = None
                self._grpc_import_error_2 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.capability_pb2 as _pb2_3_mod
                import kentik_api.gen.kagent.pb.capability_pb2_grpc as _pb2_grpc_3_mod

                self._grpc_pb2_3 = _pb2_3_mod
                self._grpc_stub_3 = _pb2_grpc_3_mod.CapabilityReleaseServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_3 = None
                self._grpc_stub_3 = None
                self._grpc_import_error_3 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.capability_pb2 as _pb2_4_mod
                import kentik_api.gen.kagent.pb.capability_pb2_grpc as _pb2_grpc_4_mod

                self._grpc_pb2_4 = _pb2_4_mod
                self._grpc_stub_4 = _pb2_grpc_4_mod.CapabilityAdminServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_4 = None
                self._grpc_stub_4 = None
                self._grpc_import_error_4 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.config_pb2 as _pb2_5_mod
                import kentik_api.gen.kagent.pb.config_pb2_grpc as _pb2_grpc_5_mod

                self._grpc_pb2_5 = _pb2_5_mod
                self._grpc_stub_5 = _pb2_grpc_5_mod.ConfigServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_5 = None
                self._grpc_stub_5 = None
                self._grpc_import_error_5 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.kagent.pb.provisioning_token_pb2 as _pb2_6_mod
                import kentik_api.gen.kagent.pb.provisioning_token_pb2_grpc as _pb2_grpc_6_mod

                self._grpc_pb2_6 = _pb2_6_mod
                self._grpc_stub_6 = _pb2_grpc_6_mod.ProvisioningTokenServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_6 = None
                self._grpc_stub_6 = None
                self._grpc_import_error_6 = exc

    def list_agent_capabilities(
        self, *, api_config_override: Optional[APIConfig] = None, agentId: str
    ) -> rest_models.ListAgentCapabilitiesResponse:
        """
        List agent capabilities.

        Returns a list of all capabilities of the specified agent.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.ListAgentCapabilitiesRequest,
                None,
                {"agent_id": agentId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListAgentCapabilities,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule1.ListAgentCapabilitiesError,
            )
            return parse_grpc_response(
                rest_models.ListAgentCapabilitiesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListAgentCapabilities,
                operation_name="ListAgentCapabilities",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule1.ListAgentCapabilities(
                api_config_override=api_config_override or rest_transport.api_config,
                agentId=agentId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_agent_capability(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentId: str,
        capabilityname: str,
    ) -> rest_models.GetAgentCapabilityResponse:
        """
        Get an agent capability.

        Returns configuration of the named capability of the specified agent.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetAgentCapabilityRequest,
                None,
                {"agent_id": agentId, "capability": capabilityname},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetAgentCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule1.GetAgentCapabilityError,
            )
            return parse_grpc_response(
                rest_models.GetAgentCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetAgentCapability,
                operation_name="GetAgentCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule1.GetAgentCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                agentId=agentId,
                capabilityname=capabilityname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_agent_capability(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentId: str,
        capabilityname: str,
    ) -> rest_models.DeleteAgentCapabilityResponse:
        """
        Delete an agent capability.

        Removes the named capability from the specified agent.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeleteAgentCapabilityRequest,
                None,
                {"agent_id": agentId, "capability": capabilityname},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeleteAgentCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule1.DeleteAgentCapabilityError,
            )
            return parse_grpc_response(
                rest_models.DeleteAgentCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeleteAgentCapability,
                operation_name="DeleteAgentCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule1.DeleteAgentCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                agentId=agentId,
                capabilityname=capabilityname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def upsert_agent_capability(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentId: str,
        capabilityname: str,
        data: rest_models.AgentCapabilityServiceUpsertAgentCapabilityBody,
        mask: Optional[str] = None,
    ) -> rest_models.UpsertAgentCapabilityResponse:
        """
        Create or update an agent capability.

        Adds the capability to the agent, or updates it if already present.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpsertAgentCapabilityRequest,
                {"capability": data.model_dump(by_alias=True, exclude_unset=True)},
                {"agent_id": agentId, "capability.name": capabilityname, "mask": mask},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpsertAgentCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule1.UpsertAgentCapabilityError,
            )
            return parse_grpc_response(
                rest_models.UpsertAgentCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpsertAgentCapability,
                operation_name="UpsertAgentCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule1.UpsertAgentCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                agentId=agentId,
                capabilityname=capabilityname,
                data=data,
                mask=mask,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_agents(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        unregistered: Optional[bool] = None,
        ids: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        includeDesiredState: Optional[bool] = None,
    ) -> rest_models.ListAgentsResponse:
        """
        List agents.

        Returns a list of agents in the account, optionally filtered by registration state, IDs or capabilities.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.ListAgentsRequest,
                None,
                {
                    "unregistered": unregistered,
                    "ids": ids,
                    "capabilities": capabilities,
                    "includeDesiredState": includeDesiredState,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.ListAgents,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.ListAgentsError,
            )
            return parse_grpc_response(
                rest_models.ListAgentsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.ListAgents,
                operation_name="ListAgents",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.ListAgents(
                api_config_override=api_config_override or rest_transport.api_config,
                unregistered=unregistered,
                ids=ids,
                capabilities=capabilities,
                includeDesiredState=includeDesiredState,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_agent(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateAgentRequest,
    ) -> rest_models.CreateAgentResponse:
        """
        Create an agent.

        Registers a new agent based on configuration in the request and returns it together with the commands for installing it on the target host.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.CreateAgentRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.CreateAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.CreateAgentError,
            )
            return parse_grpc_response(
                rest_models.CreateAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.CreateAgent,
                operation_name="CreateAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.CreateAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def authorize(
        self, *, api_config_override: Optional[APIConfig] = None, installId: str
    ) -> rest_models.AuthorizeResponse:
        """
        Authorize an unregistered agent.

        Approves the agent installed under the specified install ID and returns the ID assigned to it.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.AuthorizeRequest, None, {"install_id": installId}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.Authorize,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.AuthorizeError,
            )
            return parse_grpc_response(
                rest_models.AuthorizeResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.Authorize,
                operation_name="Authorize",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.Authorize(
                api_config_override=api_config_override or rest_transport.api_config,
                installId=installId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def generate_install_commands(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.GenerateInstallCommandsRequest,
    ) -> rest_models.GenerateInstallCommandsResponse:
        """
        Generate agent install commands.

        Returns commands for deploying an agent. The commands embed a provisioning token and are ready to execute on the target host.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GenerateInstallCommandsRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GenerateInstallCommands,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.GenerateInstallCommandsError,
            )
            return parse_grpc_response(
                rest_models.GenerateInstallCommandsResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GenerateInstallCommands,
                operation_name="GenerateInstallCommands",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.GenerateInstallCommands(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_agent(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentid: str,
        unregistered: Optional[bool] = None,
    ) -> rest_models.GetAgentResponse:
        """
        Get agent configuration and state.

        Returns configuration and state of the agent with the specified ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetAgentRequest,
                None,
                {"id": agentid, "unregistered": unregistered},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.GetAgentError,
            )
            return parse_grpc_response(
                rest_models.GetAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetAgent,
                operation_name="GetAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.GetAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
                unregistered=unregistered,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_agent(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentid: str,
        unregistered: Optional[bool] = None,
    ) -> rest_models.DeleteAgentResponse:
        """
        Delete an agent.

        Deletes the agent with the specified ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.DeleteAgentRequest,
                None,
                {"id": agentid, "unregistered": unregistered},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.DeleteAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.DeleteAgentError,
            )
            return parse_grpc_response(
                rest_models.DeleteAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.DeleteAgent,
                operation_name="DeleteAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.DeleteAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
                unregistered=unregistered,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_agent(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        agentid: str,
        data: rest_models.AgentServiceUpdateAgentBody,
        mask: Optional[str] = None,
    ) -> rest_models.UpdateAgentResponse:
        """
        Update configuration of an agent.

        Updates the attributes of an agent selected by the field mask in the request.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.UpdateAgentRequest,
                {"agent": data.model_dump(by_alias=True, exclude_unset=True)},
                {"agent.id": agentid, "mask": mask},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.UpdateAgent,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule2.UpdateAgentError,
            )
            return parse_grpc_response(
                rest_models.UpdateAgentResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.UpdateAgent,
                operation_name="UpdateAgent",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule2.UpdateAgent(
                api_config_override=api_config_override or rest_transport.api_config,
                agentid=agentid,
                data=data,
                mask=mask,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_capabilities(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListCapabilitiesResponse:
        """
        List all capabilities
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.ListCapabilitiesRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.ListCapabilities,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule3.ListCapabilitiesError,
            )
            return parse_grpc_response(
                rest_models.ListCapabilitiesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.ListCapabilities,
                operation_name="CapabilityAdminService_ListCapabilities",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule3.CapabilityAdminService_ListCapabilities(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_capability(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.Capability,
    ) -> rest_models.CreateCapabilityResponse:
        """
        Create a new capability
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.CreateCapabilityRequest,
                {"capability": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.CreateCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule3.CreateCapabilityError,
            )
            return parse_grpc_response(
                rest_models.CreateCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.CreateCapability,
                operation_name="CapabilityAdminService_CreateCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule3.CapabilityAdminService_CreateCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_capability(
        self, *, api_config_override: Optional[APIConfig] = None, capabilityname: str
    ) -> rest_models.GetCapabilityResponse:
        """
        Get a capabilities
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.GetCapabilityRequest, None, {"name": capabilityname}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.GetCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule3.GetCapabilityError,
            )
            return parse_grpc_response(
                rest_models.GetCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.GetCapability,
                operation_name="CapabilityAdminService_GetCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule3.CapabilityAdminService_GetCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                capabilityname=capabilityname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_capability(
        self, *, api_config_override: Optional[APIConfig] = None, capabilityname: str
    ) -> rest_models.DeleteCapabilityResponse:
        """
        Delete a capability
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.DeleteCapabilityRequest, None, {"name": capabilityname}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.DeleteCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule3.DeleteCapabilityError,
            )
            return parse_grpc_response(
                rest_models.DeleteCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.DeleteCapability,
                operation_name="CapabilityAdminService_DeleteCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule3.CapabilityAdminService_DeleteCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                capabilityname=capabilityname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_capability(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        capabilityname: str,
        data: rest_models.CapabilityAdminServiceUpdateCapabilityBody,
    ) -> rest_models.UpdateCapabilityResponse:
        """
        Update an existing capability
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_4 is None or self._grpc_stub_4 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_4!r}"
                ) from self._grpc_import_error_4
            _req = build_grpc_request(
                self._grpc_pb2_4.UpdateCapabilityRequest,
                {"capability": data.model_dump(by_alias=True, exclude_unset=True)},
                {"capability.name": capabilityname},
                update_mask_from="capability",
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_4.UpdateCapability,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule3.UpdateCapabilityError,
            )
            return parse_grpc_response(
                rest_models.UpdateCapabilityResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_4.UpdateCapability,
                operation_name="CapabilityAdminService_UpdateCapability",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule3.CapabilityAdminService_UpdateCapability(
                api_config_override=api_config_override or rest_transport.api_config,
                capabilityname=capabilityname,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_capability_release(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        os: Optional[str] = None,
        arch: Optional[str] = None,
        channel: Optional[str] = None,
        capability: Optional[str] = None,
        semver: Optional[str] = None,
        distro: Optional[str] = None,
    ) -> rest_models.GetCapabilityReleaseResponse:
        """
        GetCapabilityRelease can be used by install/upgrade modules to fetch a single release.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.GetCapabilityReleaseRequest,
                None,
                {
                    "os": os,
                    "arch": arch,
                    "channel": channel,
                    "capability": capability,
                    "semver": semver,
                    "distro": distro,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetCapabilityRelease,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule4.GetCapabilityReleaseError,
            )
            return parse_grpc_response(
                rest_models.GetCapabilityReleaseResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetCapabilityRelease,
                operation_name="CapabilityReleaseService_GetCapabilityRelease",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule4.CapabilityReleaseService_GetCapabilityRelease(
                api_config_override=api_config_override or rest_transport.api_config,
                os=os,
                arch=arch,
                channel=channel,
                capability=capability,
                semver=semver,
                distro=distro,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_capability_latest_releases(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        os: Optional[str] = None,
        arch: Optional[str] = None,
        channel: Optional[str] = None,
        installId: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
        distro: Optional[str] = None,
    ) -> rest_models.GetCapabilityLatestReleasesResponse:
        """
        GetCapabilityLatestReleases can be used by install/upgrade modules to fetch the latest available releases.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.GetCapabilityLatestReleasesRequest,
                None,
                {
                    "os": os,
                    "arch": arch,
                    "channel": channel,
                    "installId": installId,
                    "capabilities": capabilities,
                    "distro": distro,
                },
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetCapabilityLatestReleases,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule4.GetCapabilityLatestReleasesError,
            )
            return parse_grpc_response(
                rest_models.GetCapabilityLatestReleasesResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetCapabilityLatestReleases,
                operation_name="CapabilityReleaseService_GetCapabilityLatestReleases",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return (
                RestKagentModule4.CapabilityReleaseService_GetCapabilityLatestReleases(
                    api_config_override=api_config_override
                    or rest_transport.api_config,
                    os=os,
                    arch=arch,
                    channel=channel,
                    installId=installId,
                    capabilities=capabilities,
                    distro=distro,
                )
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_capability_supported_distros(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        capabilities: Optional[List[str]] = None,
    ) -> rest_models.GetCapabilitySupportedDistrosResponse:
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.GetCapabilitySupportedDistrosRequest,
                None,
                {"capabilities": capabilities},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.GetCapabilitySupportedDistros,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule4.GetCapabilitySupportedDistrosError,
            )
            return parse_grpc_response(
                rest_models.GetCapabilitySupportedDistrosResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.GetCapabilitySupportedDistros,
                operation_name="CapabilityReleaseService_GetCapabilitySupportedDistros",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule4.CapabilityReleaseService_GetCapabilitySupportedDistros(
                api_config_override=api_config_override or rest_transport.api_config,
                capabilities=capabilities,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_config(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.Config,
    ) -> rest_models.CreateConfigResponse:
        """
        Create a config.

        Creates a new config based on the request and returns it.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.CreateConfigRequest,
                {"config": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.CreateConfig,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule5.CreateConfigError,
            )
            return parse_grpc_response(
                rest_models.CreateConfigResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.CreateConfig,
                operation_name="CreateConfig",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule5.CreateConfig(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_config(
        self, *, api_config_override: Optional[APIConfig] = None, configname: str
    ) -> rest_models.GetConfigResponse:
        """
        Get a config.

        Returns the config with the specified name.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.GetConfigRequest, None, {"name": configname}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.GetConfig,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule5.GetConfigError,
            )
            return parse_grpc_response(
                rest_models.GetConfigResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.GetConfig,
                operation_name="GetConfig",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule5.GetConfig(
                api_config_override=api_config_override or rest_transport.api_config,
                configname=configname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def delete_config(
        self, *, api_config_override: Optional[APIConfig] = None, configname: str
    ) -> rest_models.DeleteConfigResponse:
        """
        Delete a config.

        Deletes the config with the specified name.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.DeleteConfigRequest, None, {"name": configname}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.DeleteConfig,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule5.DeleteConfigError,
            )
            return parse_grpc_response(
                rest_models.DeleteConfigResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.DeleteConfig,
                operation_name="DeleteConfig",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule5.DeleteConfig(
                api_config_override=api_config_override or rest_transport.api_config,
                configname=configname,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def update_config(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        configname: str,
        data: rest_models.ConfigServiceUpdateConfigBody,
    ) -> rest_models.UpdateConfigResponse:
        """
        Update a config.

        Updates the attributes of a config selected by the field mask in the request.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_5 is None or self._grpc_stub_5 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_5!r}"
                ) from self._grpc_import_error_5
            _req = build_grpc_request(
                self._grpc_pb2_5.UpdateConfigRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"config.name": configname},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_5.UpdateConfig,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule5.UpdateConfigError,
            )
            return parse_grpc_response(
                rest_models.UpdateConfigResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_5.UpdateConfig,
                operation_name="UpdateConfig",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule5.UpdateConfig(
                api_config_override=api_config_override or rest_transport.api_config,
                configname=configname,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_provisioning_tokens(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListProvisioningTokensResponse:
        """
        List provisioning tokens.

        Returns a list of all provisioning tokens in the account.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.ListProvisioningTokensRequest, None, {}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.ListProvisioningTokens,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule6.ListProvisioningTokensError,
            )
            return parse_grpc_response(
                rest_models.ListProvisioningTokensResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.ListProvisioningTokens,
                operation_name="ListProvisioningTokens",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule6.ListProvisioningTokens(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def create_provisioning_token(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.ProvisioningToken,
    ) -> rest_models.CreateProvisioningTokenResponse:
        """
        Create a provisioning token.

        Creates a new provisioning token based on configuration in the request and returns it, including its secret value.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.CreateProvisioningTokenRequest,
                {"token": data.model_dump(by_alias=True, exclude_unset=True)},
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.CreateProvisioningToken,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule6.CreateProvisioningTokenError,
            )
            return parse_grpc_response(
                rest_models.CreateProvisioningTokenResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.CreateProvisioningToken,
                operation_name="CreateProvisioningToken",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule6.CreateProvisioningToken(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def get_provisioning_token(
        self, *, api_config_override: Optional[APIConfig] = None, token: str
    ) -> rest_models.GetProvisioningTokenResponse:
        """
        Get provisioning token configuration and status.

        Returns configuration, usage and revocation status of the provisioning token with the specified value.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.GetProvisioningTokenRequest, None, {"token": token}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.GetProvisioningToken,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule6.GetProvisioningTokenError,
            )
            return parse_grpc_response(
                rest_models.GetProvisioningTokenResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.GetProvisioningToken,
                operation_name="GetProvisioningToken",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule6.GetProvisioningToken(
                api_config_override=api_config_override or rest_transport.api_config,
                token=token,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def list_agents_by_provisioning_token(
        self, *, api_config_override: Optional[APIConfig] = None, token: str
    ) -> rest_models.ListAgentsByProvisioningTokenResponse:
        """
        List agents registered with a provisioning token.

        Returns the IDs of all agents that have registered with the provisioning token with the specified value.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.ListAgentsByProvisioningTokenRequest,
                None,
                {"token": token},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.ListAgentsByProvisioningToken,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule6.ListAgentsByProvisioningTokenError,
            )
            return parse_grpc_response(
                rest_models.ListAgentsByProvisioningTokenResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.ListAgentsByProvisioningToken,
                operation_name="ListAgentsByProvisioningToken",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule6.ListAgentsByProvisioningToken(
                api_config_override=api_config_override or rest_transport.api_config,
                token=token,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def revoke_provisioning_token(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        token: str,
        data: rest_models.ProvisioningTokenServiceRevokeProvisioningTokenBody,
    ) -> rest_models.RevokeProvisioningTokenResponse:
        """
        Revoke a provisioning token.

        Revokes the provisioning token with the specified value. Agents already registered with the token are not affected, but the token can no longer be used for new registrations.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_6 is None or self._grpc_stub_6 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for kagent service failed to import: {self._grpc_import_error_6!r}"
                ) from self._grpc_import_error_6
            _req = build_grpc_request(
                self._grpc_pb2_6.RevokeProvisioningTokenRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"token": token},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_6.RevokeProvisioningToken,
                _req,
                api_config=api_config_override,
                error_cls=RestKagentModule6.RevokeProvisioningTokenError,
            )
            return parse_grpc_response(
                rest_models.RevokeProvisioningTokenResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_6.RevokeProvisioningToken,
                operation_name="RevokeProvisioningToken",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestKagentModule6.RevokeProvisioningToken(
                api_config_override=api_config_override or rest_transport.api_config,
                token=token,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
