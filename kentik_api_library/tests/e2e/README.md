# End-to-End (e2e) tests 

The e2e test suite verifies:
- CRUD operations for all supported test types
- listing of all tests
- listing of all agents

It interacts with production Kentik API and requires account with sufficient synthetic test
credits. User credentials myst be passed in KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN env variables.
Target API endpoint may be set  via the KTAPI_URL environment variable (default: "https://grpc.api.kentik.com")

Since labels used for labeling synthetic tests and agents must exist in the target
environment and there is currently no way to create them programmatically,
set of labels can be provided using the `test_labels` argument to the `pytest` command.
The value of the argument is comma separated list of strings. Default is no labels.

Example test suite invocation:
```
python3 -m pytest --test_labels "label1,label2" tests/e2e/synthetics/
```
