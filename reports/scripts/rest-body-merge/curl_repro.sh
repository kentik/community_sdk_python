#!/usr/bin/env bash
# Reproduces reports/upstream/upstream-rest-update-body-merge.html with curl and grpcurl only, no SDK.
#
# MUTATING, on disposable objects only: it creates one AS group, one site market,
# and one label named sdk-e2e-test-curl-<hex>, and deletes them on exit.
# Needs KENTIK_EMAIL and KENTIK_API_TOKEN in the environment, curl 8.3+ (for
# --expand-header), jq, grpcurl, and ../api-schema-public checked out.
# Credentials never appear in argv: curl and grpcurl expand them from the environment.
set -euo pipefail

: "${KENTIK_EMAIL:?set KENTIK_EMAIL}" "${KENTIK_API_TOKEN:?set KENTIK_API_TOKEN}"
BASE="https://grpc.api.kentik.com"
GRPC_HOST="grpc.api.kentik.com:443"
SCHEMA="${SCHEMA:-../api-schema-public}"
NAME="sdk-e2e-test-curl-$(openssl rand -hex 4)"
AS_ID="" MARKET_ID="" LABEL_ID=""

kcurl() { # METHOD PATH [JSON]
  local args=(-sS -X "$1" "$BASE$2" --variable %KENTIK_EMAIL --variable %KENTIK_API_TOKEN
    --expand-header 'X-CH-Auth-Email: {{KENTIK_EMAIL}}'
    --expand-header 'X-CH-Auth-API-Token: {{KENTIK_API_TOKEN}}'
    -H 'Content-Type: application/json' -w '\n%{http_code}')
  [[ $# -ge 3 ]] && args+=(-d "$3")
  curl "${args[@]}"
}

kgrpc() { # PROTO METHOD JSON
  grpcurl -expand-headers \
    -H 'X-CH-Auth-Email: ${KENTIK_EMAIL}' -H 'X-CH-Auth-API-Token: ${KENTIK_API_TOKEN}' \
    -import-path "$SCHEMA/proto" \
    -import-path "$SCHEMA/protovendor/github.com/googleapis/googleapis" \
    -import-path "$SCHEMA/protovendor/github.com/grpc-ecosystem/grpc-gateway" \
    -proto "$1" -d "$3" "$GRPC_HOST" "$2" 2>&1 | jq -c . 2>/dev/null || true
}

step() { # LABEL METHOD PATH [JSON]; prints the request and "HTTP <status> <body>"
  echo
  echo "## $1"
  echo "curl -X $2 \$BASE$3${4:+ -d '$4'}"
  local out; out=$(kcurl "${@:2}")
  echo "HTTP ${out##*$'\n'} $(jq -c . <<<"${out%$'\n'*}" 2>/dev/null || echo "${out%$'\n'*}")"
  LAST_BODY="${out%$'\n'*}"
}

cleanup() {
  echo
  echo "## Cleanup"
  [[ -n $AS_ID ]] && echo "DELETE as_group $AS_ID: HTTP $(kcurl DELETE "/as_group/v202212/as_group/$AS_ID" | tail -1)"
  [[ -n $MARKET_ID ]] && echo "DELETE site_market $MARKET_ID: HTTP $(kcurl DELETE "/site/v202509/site_markets/$MARKET_ID" | tail -1)"
  [[ -n $LABEL_ID ]] && echo "DELETE label $LABEL_ID: HTTP $(kcurl DELETE "/label/v202210/labels/$LABEL_ID" | tail -1)"
  return 0
}
trap cleanup EXIT

echo "# AS group"
step "A1. REST create, camelCase key" POST /as_group/v202212/as_group "{\"asGroup\":{\"name\":\"$NAME\",\"asn\":[\"36459\"]}}"
AS_ID=$(jq -r .asGroup.id <<<"$LAST_BODY")
step "A2. REST update, camelCase key (as documented)" PUT "/as_group/v202212/as_group/$AS_ID" "{\"asGroup\":{\"name\":\"$NAME-camel\",\"asn\":[\"36459\"]}}"
step "A3. REST update, snake_case key" PUT "/as_group/v202212/as_group/$AS_ID" "{\"as_group\":{\"name\":\"$NAME-snake\",\"asn\":[\"36459\"]}}"
step "A4. REST update, both keys" PUT "/as_group/v202212/as_group/$AS_ID" "{\"asGroup\":{\"name\":\"$NAME-a\",\"asn\":[\"36459\"]},\"as_group\":{\"name\":\"$NAME-b\",\"asn\":[\"36459\"]}}"
step "A5. REST read back" GET "/as_group/v202212/as_group/$AS_ID"
echo
echo "## A6. gRPC UpdateASGroup, camelCase JSON (grpcurl, ProtoJSON)"
kgrpc kentik/as_group/v202212/as_group.proto kentik.as_group.v202212.ASGroupService/UpdateASGroup \
  "{\"asGroup\":{\"id\":\"$AS_ID\",\"name\":\"$NAME-grpc\",\"asn\":[\"36459\",\"46489\"]}}"
step "A7. REST read back" GET "/as_group/v202212/as_group/$AS_ID"

echo
echo "# Site market"
step "B1. REST create, camelCase key" POST /site/v202509/site_markets "{\"siteMarket\":{\"name\":\"$NAME\"}}"
MARKET_ID=$(jq -r .siteMarket.id <<<"$LAST_BODY")
step "B2. REST update, camelCase key (as documented)" PUT "/site/v202509/site_markets/$MARKET_ID" "{\"siteMarket\":{\"name\":\"$NAME\",\"description\":\"camel\"}}"
step "B3. REST update, snake_case key" PUT "/site/v202509/site_markets/$MARKET_ID" "{\"site_market\":{\"name\":\"$NAME\",\"description\":\"snake\"}}"
step "B4. REST update, both keys" PUT "/site/v202509/site_markets/$MARKET_ID" "{\"siteMarket\":{\"name\":\"$NAME\",\"description\":\"camel\"},\"site_market\":{\"name\":\"$NAME\",\"description\":\"snake\"}}"
step "B5. REST read back" GET "/site/v202509/site_markets/$MARKET_ID"
echo
echo "## B6. gRPC UpdateSiteMarket, camelCase JSON (grpcurl, ProtoJSON)"
kgrpc kentik/site/v202509/site.proto kentik.site.v202509.SiteService/UpdateSiteMarket \
  "{\"siteMarket\":{\"id\":\"$MARKET_ID\",\"name\":\"$NAME\",\"description\":\"grpc\"}}"
step "B7. REST read back" GET "/site/v202509/site_markets/$MARKET_ID"

echo
echo "# Control: label (the key is \"label\" in both spellings)"
step "C1. REST create" POST /label/v202210/labels "{\"label\":{\"name\":\"$NAME\",\"color\":\"#5289D9\"}}"
LABEL_ID=$(jq -r .label.id <<<"$LAST_BODY")
step "C2. REST update" POST "/label/v202210/labels/$LABEL_ID" "{\"label\":{\"name\":\"$NAME-updated\",\"color\":\"#E35B5B\"}}"
