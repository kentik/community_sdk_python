# Kentik API Python library

This is a Python client library for [Kentik APIs](https://kb.kentik.com/v0/Ab09.htm).
It is distributed as [_kentik-api_ PyPI package](https://pypi.org/project/kentik-api/).

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

The best way to get started coding with the SDK is to study provided [examples](examples).

Interfaces for manipulating all Kentik API resources are available under the `KentikAPI` object.  
Every Kentik API resource is represented by a public class, and all related data types are located in the same source
file or directory as the implementation of the class:
- [CustomApplication](kentik_apiublic/custom_application.py)
- [CustomDimension](kentik_apiublic/custom_dimension.py)
- [DeviceLabel](kentik_apiublic/device_label.py)
- [Device](kentik_apiublic/device.py)
- [ManualMitigation](kentik_apiublic/manual_mitigation.py)
- [Plan](kentik_apiublic/plan.py)
- [QueryObject](kentik_apiublic/query_object.py)
- [QuerySQL](kentik_apiublic/query_sql.py)
- [SavedFilter](kentik_apiublic/saved_filter.py)
- [Site](kentik_apiublic/site.py)
- [Synthetic Tests](kentik_api/synthetics/)
- [Tag](kentik_apiublic/tag.py)
- [Tenant](kentik_apiublic/tenant.py)
- [User](kentik_apiublic/user.py)

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
index of devices by `name` and by `id`. Devices are represented by the [Device](kentik_apiublic/device.py) class which
internally builds dictionary of device interfaces  (represented by the `DeviceInterface` class) by `name`.

## Analytic support

The `analytics` package provides support for processing Kentik time series data using Pandas Dataframes.
The [pandas](https://pandas.pydata.org) and [PyYAML](https://pyyaml.org/) modules are required by the `analytics`
sub-module and are automatically installed with the `kentik-api[analytics]` option.
See [analytics readme](kentik_apinalytics/README.md) for more details.

## Available Examples

- [alerting_example.py](exampleslerting_example.py) - create Manual Mitigation
- [applications_example.py](examplespplications_example.py) - create/update/delete Custom Application
- [bulk_user_create.py](examplesulk_user_create.py) - create users from YAML file
- [devices_example.py](examplesevices_example.py) - create/update/get/delete/list Devices
- [dimensions_example.py](examplesimensions_example.py) - create/update/get/delete/list Custom Dimensions, create/update/delete Populator
- [labels_example.py](examplesabels_example.py) - create/update/get/delete/list Device Labels
- [my_kentik_portal_example.py](examplesy_kentik_portal_example.py) - get/list Tenants, create/delete Tenant User
- [plans_example.py](exampleslans_example.py) - list plans
- [queries_example.py](examplesueries_example.py) - query for SQL/URL/data/chart
- [saved_filters_example.py](examplesaved_filters_example.py) - create/update/get/delete/list Saved Filters
- [sites_example.py](examplesites_example.py) - create/update/get/delete/list Sites
- [tags_example.py](examplesags_example.py) - create/update/get/delete/list Tags
- [users_example.py](examplessers_example.py) - create/update/get/delete/list Users
- [error_handling_example.py](examplesrror_handling_example.py) - handling errors raised by the library
- [analytics_example_sql.py](examplesnalytics_example_sql.py) - use of `SQLQueryDefinition`, `flatness_analysis` method and the`DeviceCache`
- [analytics_example_topx.py](examplesnalytics_example_sql.py) - use of `DataQueryDefinition`, `flatness_analysis` method and the`DeviceCache`
  (see also [analytics readme](kentik_apinalytics/README.md))
- [synthetics_example.py](examplesynthetics_example.py) - interact with synthetics API
- [cloud_export_example.py](examplesloud_export_example.py) - interact with cloud export API

## Development

[Instructions for developers](docs/README.md)

## Open-source libraries

This software uses the following open-source libraries:
- [dacite](https://pypi.org/project/dacite/) by Konrad Hałas - MIT License
- [requests](https://pypi.org/project/requests/) by Kenneth Reitz - Apache Software License (Apache 2.0)
- [typing-extensions](https://pypi.org/project/typing-extensions/) by  Guido van Rossum, Jukka Lehtosalo, Lukasz Langa, Michael Lee - PSFL License
- [pandas](https://pandas.pydata.org) supported by NumFOCUS - BSD 3-Clause License
- [pyyaml](https://pyyaml.org/) by Ingy döt Net and Kirill Simonov - MIT license
