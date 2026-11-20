#!/usr/bin/env bash
# Read-only, no SDK: each read that answers 5xx in the e2e suite, sent with curl.
# An ID that does not exist should give 404, and a bad argument 400.
set -uo pipefail
: "${KENTIK_EMAIL:?}" "${KENTIK_API_TOKEN:?}"
H=https://grpc.api.kentik.com
get() {
  local code body
  body=$(curl -s -w '\n%{http_code}' -H "X-CH-Auth-Email: $KENTIK_EMAIL" \
    -H "X-CH-Auth-API-Token: $KENTIK_API_TOKEN" "$H$1")
  code=${body##*$'\n'}
  body=${body%$'\n'*}
  printf '%-62s %s %s\n' "$1" "$code" "$(tr -d '\n' <<<"$body" | cut -c1-110)"
}
date -u +"run at %Y-%m-%dT%H:%M:%SZ"
for id in 999999999 not-a-number; do
  get "/v202505/alerts/ack/auto/$id"
  get "/v202505/alerts/silence/$id"
  get "/v202505/alerts/$id/comments"
  get "/v202505/mitigations/$id/actions"
  get "/v202505/suppressions/$id"
  get "/v202505/policies/POLICY_TYPE_PROTECT/$id"
  get "/audit/v202601/events/$id"
  get "/audit/v202601/events/$id/2024-01-01T00:00:00Z"
  get "/custom_application/v202501alpha1/$id"
  get "/vault/v202312alpha1/secrets/$id"
  get "/vault/v202312alpha1/secrets?names=$id"
  get "/kmi/v202212/insights/$id"
done
get "/kagent/v202401/capabilities"
get "/kmeta/v202607alpha1/1/servicenow/config"
