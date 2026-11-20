from typing import Optional, Union, cast

import kentik_api.gen.mkp.services.PackageService as RestMkpModule1
import kentik_api.gen.mkp.services.TenantService as RestMkpModule2
import kentik_api.gen.mkp.services.TenantUserService as RestMkpModule3
from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    parse_grpc_response,
)
from kentik_api.gen.mkp import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class MkpServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.mkp.pb.mkp_pb2 as _pb2_1_mod
                import kentik_api.gen.mkp.pb.mkp_pb2_grpc as _pb2_grpc_1_mod

                self._grpc_pb2_1 = _pb2_1_mod
                self._grpc_stub_1 = _pb2_grpc_1_mod.PackageServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_1 = None
                self._grpc_stub_1 = None
                self._grpc_import_error_1 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.mkp.pb.mkp_pb2 as _pb2_2_mod
                import kentik_api.gen.mkp.pb.mkp_pb2_grpc as _pb2_grpc_2_mod

                self._grpc_pb2_2 = _pb2_2_mod
                self._grpc_stub_2 = _pb2_grpc_2_mod.TenantServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_2 = None
                self._grpc_stub_2 = None
                self._grpc_import_error_2 = exc
            try:
                __import__("kentik_api.gen.pb_companions")
                import kentik_api.gen.mkp.pb.mkp_pb2 as _pb2_3_mod
                import kentik_api.gen.mkp.pb.mkp_pb2_grpc as _pb2_grpc_3_mod

                self._grpc_pb2_3 = _pb2_3_mod
                self._grpc_stub_3 = _pb2_grpc_3_mod.TenantUserServiceStub(
                    self._transport.channel
                )
            except (ImportError, TypeError) as exc:
                self._grpc_pb2_3 = None
                self._grpc_stub_3 = None
                self._grpc_import_error_3 = exc

    def package_list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListPackageResponse:
        """
        List MKP packages.

        Returns a list of MKP packages.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(self._grpc_pb2_1.ListPackageRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.ListPackage,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule1.PackageListError,
            )
            return parse_grpc_response(
                rest_models.ListPackageResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.ListPackage,
                operation_name="PackageList",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule1.PackageList(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def package_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreatePackageRequest,
    ) -> rest_models.CreatePackageResponse:
        """
        Create a package template.

        Create package from request. returns created package.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.CreatePackageRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.CreatePackage,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule1.PackageCreateError,
            )
            return parse_grpc_response(
                rest_models.CreatePackageResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.CreatePackage,
                operation_name="PackageCreate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule1.PackageCreate(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def package_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetPackageResponse:
        """
        Get information aboout a package.

        Returns information about package specified with ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.GetPackageRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.GetPackage,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule1.PackageGetError,
            )
            return parse_grpc_response(
                rest_models.GetPackageResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.GetPackage,
                operation_name="PackageGet",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule1.PackageGet(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def package_update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.PackageServiceUpdatePackageBody,
    ) -> rest_models.UpdatePackageResponse:
        """
        Update a package.

        Update package attributes specified with id.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.UpdatePackageRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"package.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.UpdatePackage,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule1.PackageUpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdatePackageResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.UpdatePackage,
                operation_name="PackageUpdate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule1.PackageUpdate(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def package_delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeletePackageResponse:
        """
        Delete a package.

        Deletes the package specified with id.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_1 is None or self._grpc_stub_1 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_1!r}"
                ) from self._grpc_import_error_1
            _req = build_grpc_request(
                self._grpc_pb2_1.DeletePackageRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_1.DeletePackage,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule1.PackageDeleteError,
            )
            return parse_grpc_response(
                rest_models.DeletePackageResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_1.DeletePackage,
                operation_name="PackageDelete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule1.PackageDelete(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_list(
        self, *, api_config_override: Optional[APIConfig] = None
    ) -> rest_models.ListTenantResponse:
        """
        List MKP tenants.

        Returns a list of MKP tenants.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(self._grpc_pb2_2.ListTenantRequest, None, {})
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.ListTenant,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule2.TenantListError,
            )
            return parse_grpc_response(
                rest_models.ListTenantResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.ListTenant,
                operation_name="TenantList",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule2.TenantList(
                api_config_override=api_config_override or rest_transport.api_config
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.CreateTenantRequest,
    ) -> rest_models.CreateTenantResponse:
        """
        Create a tenant.

        Create tenant from request. returns created tenant.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.CreateTenantRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.CreateTenant,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule2.TenantCreateError,
            )
            return parse_grpc_response(
                rest_models.CreateTenantResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.CreateTenant,
                operation_name="TenantCreate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule2.TenantCreate(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_get(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.GetTenantResponse:
        """
        Get information aboout a tenant.

        Returns information about package specified with ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.GetTenantRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.GetTenant,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule2.TenantGetError,
            )
            return parse_grpc_response(
                rest_models.GetTenantResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.GetTenant,
                operation_name="TenantGet",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule2.TenantGet(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        id: str,
        data: rest_models.TenantServiceUpdateTenantBody,
    ) -> rest_models.UpdateTenantResponse:
        """
        Update a tenant.

        Update tenant attributes specified with id.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.UpdateTenantRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"tenant.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.UpdateTenant,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule2.TenantUpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateTenantResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.UpdateTenant,
                operation_name="TenantUpdate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule2.TenantUpdate(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_delete(
        self, *, api_config_override: Optional[APIConfig] = None, id: str
    ) -> rest_models.DeleteTenantResponse:
        """
        Delete a tenant.

        Deletes the tenant specified with id.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_2 is None or self._grpc_stub_2 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_2!r}"
                ) from self._grpc_import_error_2
            _req = build_grpc_request(
                self._grpc_pb2_2.DeleteTenantRequest, None, {"id": id}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_2.DeleteTenant,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule2.TenantDeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteTenantResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_2.DeleteTenant,
                operation_name="TenantDelete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule2.TenantDelete(
                api_config_override=api_config_override or rest_transport.api_config,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_user_list(
        self, *, api_config_override: Optional[APIConfig] = None, tenantId: str
    ) -> rest_models.ListTenantUserResponse:
        """
        List users for a tenant.

        Returns a list of users associated with the specified tenant.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.ListTenantUserRequest, None, {"tenant_id": tenantId}
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.ListTenantUser,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule3.TenantUserListError,
            )
            return parse_grpc_response(
                rest_models.ListTenantUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.ListTenantUser,
                operation_name="TenantUserList",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule3.TenantUserList(
                api_config_override=api_config_override or rest_transport.api_config,
                tenantId=tenantId,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_user_create(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        tenantId: str,
        data: rest_models.TenantUserServiceCreateTenantUserBody,
    ) -> rest_models.CreateTenantUserResponse:
        """
        Add a user to a tenant.

        Creates a user association with the specified tenant.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.CreateTenantUserRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"user.tenant_id": tenantId},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.CreateTenantUser,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule3.TenantUserCreateError,
            )
            return parse_grpc_response(
                rest_models.CreateTenantUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.CreateTenantUser,
                operation_name="TenantUserCreate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule3.TenantUserCreate(
                api_config_override=api_config_override or rest_transport.api_config,
                tenantId=tenantId,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_user_update(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        tenantId: str,
        id: str,
        data: rest_models.TenantUserServiceUpdateTenantUserBody,
    ) -> rest_models.UpdateTenantUserResponse:
        """
        Update a tenant user.

        Updates the user associated with the specified tenant and user ID.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.UpdateTenantUserRequest,
                data.model_dump(by_alias=True, exclude_unset=True),
                {"user.tenant_id": tenantId, "user.id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.UpdateTenantUser,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule3.TenantUserUpdateError,
            )
            return parse_grpc_response(
                rest_models.UpdateTenantUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.UpdateTenantUser,
                operation_name="TenantUserUpdate",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule3.TenantUserUpdate(
                api_config_override=api_config_override or rest_transport.api_config,
                tenantId=tenantId,
                id=id,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def tenant_user_delete(
        self, *, api_config_override: Optional[APIConfig] = None, tenantId: str, id: str
    ) -> rest_models.DeleteTenantUserResponse:
        """
        Remove a user from a tenant.

        Deletes the user association with the specified tenant.
        """
        if isinstance(self._transport, GrpcTransport):
            if self._grpc_pb2_3 is None or self._grpc_stub_3 is None:
                raise NotImplementedError(
                    f"gRPC proto modules for mkp service failed to import: {self._grpc_import_error_3!r}"
                ) from self._grpc_import_error_3
            _req = build_grpc_request(
                self._grpc_pb2_3.DeleteTenantUserRequest,
                None,
                {"tenant_id": tenantId, "id": id},
            )
            _resp, _rate_limit = call_grpc(
                self._grpc_stub_3.DeleteTenantUser,
                _req,
                api_config=api_config_override,
                error_cls=RestMkpModule3.TenantUserDeleteError,
            )
            return parse_grpc_response(
                rest_models.DeleteTenantUserResponse,
                _resp,
                _rate_limit,
                stub_method=self._grpc_stub_3.DeleteTenantUser,
                operation_name="TenantUserDelete",
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestMkpModule3.TenantUserDelete(
                api_config_override=api_config_override or rest_transport.api_config,
                tenantId=tenantId,
                id=id,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
