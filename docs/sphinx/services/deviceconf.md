<!-- AUTO-GENERATED: scripts/generation/endpoint_docs.py, render_endpoint_docs() -->
<!-- Rebuilt on every `uv run poe generate`. Do not edit by hand. -->

# Deviceconf Service

## Endpoints

This service's schema defines shared types only. It has no REST endpoints.

## Data Models

<details>
<summary>Model relationships (27 of 27 models)</summary>

Each arrow points from a model to a model that one of its fields holds. The label names the field.

```mermaid
%%{init: {"theme": "redux", "look": "neo", "layout": "elk", "fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "themeVariables": {"fontFamily": "ui-monospace, SFMono-Regular, Menlo, monospace", "primaryColor": "#f8f9fa", "primaryBorderColor": "#495057", "primaryTextColor": "#212529", "textColor": "#212529", "lineColor": "#77818c", "edgeLabelBackground": "#ffffff", "actorBkg": "#f8f9fa", "actorBorder": "#495057", "actorTextColor": "#212529", "actorLineColor": "#a9b3be", "signalColor": "#57616d", "signalTextColor": "#212529", "labelBoxBkgColor": "#f8f9fa", "labelBoxBorderColor": "#495057", "labelTextColor": "#212529", "loopTextColor": "#57616d", "noteBkgColor": "#fff9db", "noteBorderColor": "#f08c00", "noteTextColor": "#a35a00"}, "sequence": {"activationWidth": 16}, "flowchart": {"curve": "basis", "nodeSpacing": 30, "rankSpacing": 70, "wrappingWidth": 400}}}%%
classDiagram
    class AclAction
    class AclMode
    class CommandAcl
    class CommandResult
    class CommitDetails
    class ConfigEncoding
    class DeleteDeviceConfigurationResponse
    class Device
    class DeviceCommand
    class DevicePlatform
    class DeviceSSHCreds
    class ExecuteCommandResponse
    class FetchParameters
    class GetCommandAclsResponse
    class GetDeviceAssignmentsResponse
    class GetDeviceConfigurationResponse
    class GetLatestDeviceConfigurationsResponse
    class ListDeviceConfigurationRevisionsResponse
    class MessageSignature
    class RequestDeviceConfigurationFetchResponse
    class Revision
    class SignatureAlgorithm
    class Snapshot
    class UpdateCommandAclsResponse
    class UpdateDeviceConfigurationResponse
    class protobufAny
    class rpcStatus
    CommandAcl --> AclAction : action
    CommandAcl --> AclMode : mode
    DeleteDeviceConfigurationResponse --> Revision : orphanedRevision
    Device --> DevicePlatform : platform
    Device --> DeviceSSHCreds : sshCreds
    Device --> FetchParameters : fetchParams
    ExecuteCommandResponse --> CommandResult : commandResult
    GetCommandAclsResponse --> CommandAcl : acls
    GetDeviceAssignmentsResponse --> Device : devices
    GetDeviceConfigurationResponse --> Snapshot : config
    ListDeviceConfigurationRevisionsResponse --> Revision : revisions
    MessageSignature --> SignatureAlgorithm : algorithm
    Snapshot --> CommitDetails : commitDetails
    Snapshot --> ConfigEncoding : encoding
    Snapshot --> DevicePlatform : platform
    Snapshot --> Revision : revision, diffRevision
    rpcStatus --> protobufAny : details
```

</details>

```{eval-rst}
.. autoclass:: kentik_api.gen.deviceconf.models.AclAction
   :members:
```

```{eval-rst}
.. autoclass:: kentik_api.gen.deviceconf.models.AclMode
   :members:
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.CommandAcl
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.CommandResult
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.CommitDetails
```

```{eval-rst}
.. autoclass:: kentik_api.gen.deviceconf.models.ConfigEncoding
   :members:
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.DeleteDeviceConfigurationResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.Device
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.DeviceCommand
```

```{eval-rst}
.. autoclass:: kentik_api.gen.deviceconf.models.DevicePlatform
   :members:
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.DeviceSSHCreds
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.ExecuteCommandResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.FetchParameters
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.GetCommandAclsResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.GetDeviceAssignmentsResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.GetDeviceConfigurationResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.GetLatestDeviceConfigurationsResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.ListDeviceConfigurationRevisionsResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.MessageSignature
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.RequestDeviceConfigurationFetchResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.Revision
```

```{eval-rst}
.. autoclass:: kentik_api.gen.deviceconf.models.SignatureAlgorithm
   :members:
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.Snapshot
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.UpdateCommandAclsResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.UpdateDeviceConfigurationResponse
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.protobufAny
```

```{eval-rst}
.. autopydantic_model:: kentik_api.gen.deviceconf.models.rpcStatus
```
