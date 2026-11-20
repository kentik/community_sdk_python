from typing import Optional, Union, cast

import kentik_api.gen.v5.services.BatchService as RestV5Module1
import kentik_api.gen.v5.services.QueryService as RestV5Module2
from kentik_api.core.api_config import APIConfig
from kentik_api.gen.v5 import models as rest_models
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


class V5ServiceWrapper:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_service_wrappers().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    Unified Service routing to either gRPC or REST.
    """

    def __init__(self, transport: Union[GrpcTransport, RestTransport]):
        self._transport = transport
        if isinstance(self._transport, GrpcTransport):
            pass  # gRPC not yet implemented for this service

    def batch_tags(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.BatchPart,
    ) -> rest_models.BatchResponse:
        """
        Batch flow tags

        Creates, updates, or deletes flow tags in bulk. Sends one part of a batch. The API applies upserts as parts arrive and deletes only after the part with complete=true. Each part is at most 4 MB. Every part after the first carries the guid from the first response. kentik_api.v5_tools.split_batch() and send_batch() do this. The SDK never resends a part.
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for BatchService_Tags is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module1.BatchService_Tags(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def batch_populators(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        dimensionName: str,
        data: rest_models.BatchPart,
    ) -> rest_models.BatchResponse:
        """
        Batch populators

        Creates, updates, or deletes the populators of one custom dimension in bulk. Sends one part of a batch. The API applies upserts as parts arrive and deletes only after the part with complete=true. Each part is at most 4 MB. Every part after the first carries the guid from the first response. kentik_api.v5_tools.split_batch() and send_batch() do this. The SDK never resends a part.
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for BatchService_Populators is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module1.BatchService_Populators(
                api_config_override=api_config_override or rest_transport.api_config,
                dimensionName=dimensionName,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def batch_status(
        self, *, api_config_override: Optional[APIConfig] = None, guid: str
    ) -> rest_models.BatchStatus:
        """
        Batch status

        Returns the progress of a batch. kentik_api.v5_tools.wait_for_batch() polls it until is_complete is true.
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for BatchService_Status is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module1.BatchService_Status(
                api_config_override=api_config_override or rest_transport.api_config,
                guid=guid,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def top_x_data(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.QueryRequest,
    ) -> rest_models.TopXDataResponse:
        """
        Top-X data query

        Runs one or more queries on the Kentik Data Engine and returns the result rows of each bucket, with time series for the top-X rows.
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for QueryService_TopXData is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module2.QueryService_TopXData(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def top_x_chart(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.ChartRequest,
    ) -> rest_models.ChartResponse:
        """
        Top-X chart query

        Runs one or more queries and returns a chart image as a base64 data URI. Not verified: in a live check on 2026-10-16 this endpoint gave no response within 180 seconds. Decode the result with kentik_api.v5_tools.decode_chart().
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for QueryService_TopXChart is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module2.QueryService_TopXChart(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )

    def query_url(
        self,
        *,
        api_config_override: Optional[APIConfig] = None,
        data: rest_models.QueryRequest,
    ) -> str:
        """
        Data Explorer URL

        Returns a link that opens Data Explorer in the Kentik portal with the sidebar set to the query.
        """
        if isinstance(self._transport, GrpcTransport):
            raise NotImplementedError(
                "gRPC translation for QueryService_Url is not yet implemented."
            )
        elif isinstance(self._transport, RestTransport):
            rest_transport = cast(RestTransport, self._transport)
            return RestV5Module2.QueryService_Url(
                api_config_override=api_config_override or rest_transport.api_config,
                data=data,
            )
        else:
            raise TypeError(
                f"Unsupported transport type: {self._transport.__class__.__name__}"
            )
