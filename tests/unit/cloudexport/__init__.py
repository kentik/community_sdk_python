from copy import deepcopy

import kentik_api.generated.kentik.cloud_export.v202101beta1.cloud_export_pb2 as pb


def clear_readonly_fields(export: pb.CloudExport) -> pb.CloudExport:
    """For sending a request - clear the server-generated fields"""

    export = deepcopy(export)  # to avoid interference between tests
    export.ClearField("current_status")
    export.ClearField("api_root")
    export.ClearField("flow_dest")
    return export
