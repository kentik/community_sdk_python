# AUTO-GENERATED: scripts/generate_sdk.py, _compile_proto_companions()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

# isort: skip_file
"""
Proto companion registry: loads all shared vendor descriptors into the pool.

The load order is critical for proto descriptor registration and must not be
changed. The isort: skip_file directive prevents ruff from resorting these imports.
"""

# foundation: google/protobuf/descriptor.proto
from google.protobuf import descriptor_pb2 as _descriptor_pb2  # noqa: F401

# google/api/*.proto from googleapis-common-protos
from google.api import annotations_pb2 as _ga_annotations  # noqa: F401
from google.api import client_pb2 as _ga_client  # noqa: F401
from google.api import field_behavior_pb2 as _ga_field_behavior  # noqa: F401
from google.protobuf import duration_pb2 as _duration  # noqa: F401
from google.protobuf import struct_pb2 as _struct  # noqa: F401
from google.protobuf import timestamp_pb2 as _timestamp  # noqa: F401

# protoc-gen-openapiv2/options/*.proto from grpc-gateway (must be before kentik/core)
# openapiv2_pb2 must be before annotations_pb2 (annotations imports openapiv2)
from .protoc_gen_openapiv2.options import openapiv2_pb2 as _oa_openapiv2  # noqa: F401
from .protoc_gen_openapiv2.options import annotations_pb2 as _oa_annotations  # noqa: F401

# kentik/core/v202303/*.proto (must be after protoc-gen-openapiv2 companions)
import kentik_api.gen.core.pb.annotations_pb2 as _core_annotations  # noqa: F401, E402
import kentik_api.gen.core.pb.user_info_pb2 as _core_user_info  # noqa: F401, E402
