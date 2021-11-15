import logging
import sys
from typing import Any, Dict, Optional, Tuple

from .api_transport import KentikAPIRequestError, KentikAPITransport

sys.path.append("../generated")

# import generated.kentik.synthetics.v202101beta1.synthetics_pb2
# from generated.kentik.synthetics.v202101beta1.synthetics_pb2_grpc import SyntheticsAdminService, SyntheticsDataService

log = logging.getLogger("api_transport_grpc")


class SynthGRPCTransport(KentikAPITransport):
    def __init__(self, credentials: Tuple[str, str], url: str = "https://synthetics.api.kentik.com"):
        raise NotImplementedError

    def req(self, op: str, **kwargs) -> Any:
        return None
