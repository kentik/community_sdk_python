# community_sdk_python - developer

## Getting started

Precondition: python3 and pip3 are already installed.

### Recommended steps

1. Create dedicated virtual environment  
`python -m venv .venv`

1. Activate virtualenv  
`source .venv/bin/activate`

1. Clone the library repository  
`git clone https://github.com/kentik/community_sdk_python.git`

1. `cd community_sdk_python/kentik_api_library/`

1. Install Python dependencies  
`pip install -r requirements.txt`  
`pip install -r requirements-dev.txt`  

1. Generate grpc client code  
`python setup.py grpc_stubs`

1. Install the library from repository  
`pip install -e .`

1. Run unit tests  
`python setup.py pytest`

1. Run mypy  
`python setup.py mypy`

1. Run black and isort checks  
`python setup.py format --check`

## Example

The example below illustrates how to create a new device using the library:

```python
# library-specific imports
from kentik_api.public.types import ID
from kentik_api import (
    KentikAPI,
    Device,
    DeviceSubtype,
    CDNAttribute,
)

# initialize Kentik API client
api_client = KentikAPI("<API_EMAIL_STRING>", "<API_TOKEN_STRING>")

# prepare device object
device = Device.new_dns(
    device_name="example-device-1",
    device_subtype=DeviceSubtype.aws_subnet,
    cdn_attr=CDNAttribute.yes,
    device_sample_rate=100,
    plan_id=ID(11466),
    site_id=ID(8483),
    device_bgp_flowspec=True,
)

# create the device
created = api_client.devices.create(device)

# print returned device's attributes
print(created.__dict__)
```

## Example explained

### Structure

- `kentik_api` package is the root package of the library
- `api_resources` package contains implementations of all the KentikAPI resource manipulation classes
- `public` package contains classes representing all KentikAPI resources
- `request_payloads` package contains serialization/deserialization structures for each KentikAPI resource
- `api_calls` package contains definitions of all requests that enable interaction with each KentikAPI resource

Main components taking part in creating a device:  
![Create Device - Component Diagram](./diagrams/device_create_component.png)

### Behaviour

A sequence of interactions that leads to creating a new device:  
![Create Device - Sequence Diagram](./diagrams/device_create_sequence.png)

## Error handling

For error handling there is an exception hierarchy that allows to handle:
- validation errors - when library user tries to create an incomplete/invalid resource
- deserialization erors - when invalid or incomplete resource json representation is received from KentikAPI
- protocol errors - errors covering selected HTTP error codes, in particular:
  - `IntermittentError` - request can be reattempted and succeed after a delay
  - `RateLimitExceededError` - effect of throttling on KentikAPI side

![Exception Hierarchy - Class Diagram](./diagrams/error_hierarchy_class.png)

## Release

The release process for the kentik-api library is based on Git repository tags. Every tag with format `v[0-9].[0-9].[0-9]` will trigger an automatic build of the package and publish it in the PyPi repository.

To build and release package:
1. Make sure that all code that you want to release is in the _main_ branch
1. Create a tag with format `v[0-9].[0-9].[0-9]` in GitHub. [Releases](https://github.com/kentik/community_sdk_python/releases) -> Draft a new release -> Put tag version, name and description
1. Go to [GitHub Actions](https://github.com/kentik/community_sdk_python/actions)
