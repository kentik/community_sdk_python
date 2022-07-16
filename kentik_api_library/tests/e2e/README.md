# End-to-End (e2e) tests

The e2e test suite verifies:
- CRUD operations for all supported test types
- listing of all tests
- listing of all agents

It interacts with production Kentik API and requires account with sufficient synthetic test credits.
User credentials myst be passed in KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN env variables.
Target API endpoint may be set  via the KTAPI_URL environment variable (default: "https://grpc.api.kentik.com").

Agent and test labels and alarm notification channels must exist in the target
environment before they can be used. There is currently no way to create them programmatically.
The test suite allows to pass those attributes `test_labels` and `notification_channels` to `pytest`.
Both arguments expect comma separated list of strings and default to empty strings.

The Kentik synthetics API allows to pass modification date in update requests as a measure allowing to
guard against concurrent modifications. Due to a bug in the API, this feature is currently disabled
by default. It can be enabled by passing the `pass_edate_on_update` argument to `pytest`.

Example test invocations:
```shell
python3 -m pytest --test_labels="label1,label2" --notification_channels="123,456" tests/e2e/synthetics
python3 -m pytest --pass_edate_on_update tests/e2e/synthetics/test_agent.py
```
