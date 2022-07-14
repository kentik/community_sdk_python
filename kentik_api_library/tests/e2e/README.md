# e2e tests

E2E tests connect to production Kentik server and require valid credentials passed
in KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN env variables. Target API endpoint may be set
via the KTAPI_URL environment variable (default: "https://grpc.api.kentik.com")