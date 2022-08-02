# Kentik API Python library

This is a Python client library for [Kentik APIs](https://kb.kentik.com/v0/Ab09.htm). It is distributed as [_kentik-api_ PyPI package](https://pypi.org/project/kentik-api/).

## Installation with pip

1. Install the library using pip:  
```pip3 install kentik-api```
1. Check installation successful - no errors should be reported:  
```python3 -c "import kentik_api"```
1. Run an example (optional):
  ```bash
  export KTAPI_AUTH_EMAIL=<your kentik api credentials email>
  export KTAPI_AUTH_TOKEN=<your kentik api credentials token>
  python3 examples/sites_example.py
  ```

## Getting started

The best way to get started coding with the SDK is to study provided [examples](./examples).

Interfaces for manipulating all Kentik API resources are available under the `KentikAPI` object.  
Every Kentik API resource is represented by a public class, and all related data types are located in the same source
file or directory as the implementation of the class:
- [CustomApplication](./kentik_api/public/custom_application.py)
- [CustomDimension](./kentik_api/public/custom_dimension.py)
- [DeviceLabel](./kentik_api/public/device_label.py)
- [Device](./kentik_api/public/device.py)
- [ManualMitigation](./kentik_api/public/manual_mitigation.py)
- [Plan](./kentik_api/public/plan.py)
- [QueryObject](./kentik_api/public/query_object.py)
- [QuerySQL](./kentik_api/public/query_sql.py)
- [SavedFilter](./kentik_api/public/saved_filter.py)
- [Site](./kentik_api/public/site.py)
- [Synthetic Tests](./kentik_api/synthetics/)
- [Tag](./kentik_api/public/tag.py)
- [Tenant](./kentik_api/public/tenant.py)
- [User](./kentik_api/public/user.py)

## Additional utilities available in the `utils` sub-module

### Authentication support

- `get_credentials`: function for retrieving authentication credentials from the environment or a profile stored on disk.
  API authentication credentials can be provided via environment variables `KTAPI_AUTH_EMAIL` and `KTAPI_AUTH_TOKEN`
  or via named profile (specified as argument to the `get_credentials` functions, defaulting to `default`) which is
  a JSON file with following format:
```json
{
  "email": "<email address>",
  "api-key": "<the API key>"
}
```
Path to the profile file can be provided in `KTAPI_CFG_FILE`. Otherwise it is first searched in
`${KTAPI_HOME}/<profile_name>` and then in `${HOME}/.kentik/<profile_name>`.

### Support for caching of device data

The `DeviceCache` class allows caching of device related data obtained from the Kentik API. It internally builds
index of devices by `name` and by `id`. Devices are represented by the [Device](./kentik_api/public/device.py) class which
internally builds dictionary of device interfaces  (represented by the `DeviceInterface` class) by `name`.

## Analytic support

The `analytics` package provides support for processing Kentik time series data using Pandas Dataframes.
The [pandas](https://pandas.pydata.org) and [PyYAML](https://pyyaml.org/) modules are required by the `analytics`
sub-module and are automatically installed with the `kentik-api[analytics]` option.
See [analytics readme](./kentik_api/analytics/README.md) for more details.

## Available Examples

- [alerting_example.py](./examples/alerting_example.py) - create Manual Mitigation
- [applications_example.py](./examples/applications_example.py) - create/update/delete Custom Application
- [bulk_user_create.py](./examples/bulk_user_create.py) - create users from YAML file
- [devices_example.py](./examples/devices_example.py) - create/update/get/delete/list Devices
- [dimensions_example.py](./examples/dimensions_example.py) - create/update/get/delete/list Custom Dimensions, create/update/delete Populator
- [labels_example.py](./examples/labels_example.py) - create/update/get/delete/list Device Labels
- [my_kentik_portal_example.py](./examples/my_kentik_portal_example.py) - get/list Tenants, create/delete Tenant User
- [plans_example.py](./examples/plans_example.py) - list plans
- [queries_example.py](./examples/queries_example.py) - query for SQL/URL/data/chart
- [saved_filters_example.py](./examples/saved_filters_example.py) - create/update/get/delete/list Saved Filters
- [sites_example.py](./examples/sites_example.py) - create/update/get/delete/list Sites
- [tags_example.py](./examples/tags_example.py) - create/update/get/delete/list Tags
- [users_example.py](./examples/users_example.py) - create/update/get/delete/list Users
- [error_handling_example.py](./examples/error_handling_example.py) - handling errors raised by the library
- [analytics_example_sql.py](./examples/analytics_example_sql.py) - use of `SQLQueryDefinition`, `flatness_analysis` method and the`DeviceCache`
- [analytics_example_topx.py](./examples/analytics_example_sql.py) - use of `DataQueryDefinition`, `flatness_analysis` method and the`DeviceCache`
  (see also [analytics readme](./kentik_api/analytics/README.md))
- [synthetics_example.py](./examples/synthetics_example.py) - interact with synthetics API
- [cloud_export_example.py](./examples/cloud_export_example.py) - interact with cloud export API

## Development

[Instructions for developers](../docs/README.md)

## Open-source libraries

This software uses the following open-source libraries:
- [dacite](https://pypi.org/project/dacite/) by Konrad Hałas - MIT License
- [requests](https://pypi.org/project/requests/) by Kenneth Reitz - Apache Software License (Apache 2.0)
- [typing-extensions](https://pypi.org/project/typing-extensions/) by  Guido van Rossum, Jukka Lehtosalo, Lukasz Langa, Michael Lee - PSFL License
- [pandas](https://pandas.pydata.org) supported by NumFOCUS - BSD 3-Clause License
- [pyyaml](https://pyyaml.org/) by Ingy döt Net and Kirill Simonov - MIT license
