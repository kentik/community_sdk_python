#!/usr/bin/env bash
# Read-only: each service's List call with no deadline, then with -max-time 1, 30, 300.
set -uo pipefail
: "${KENTIK_EMAIL:?}" "${KENTIK_API_TOKEN:?}"
S=../api-schema-public
g() {
  grpcurl -expand-headers -H 'X-CH-Auth-Email: ${KENTIK_EMAIL}' -H 'X-CH-Auth-API-Token: ${KENTIK_API_TOKEN}' \
    -import-path $S/proto -import-path $S/protovendor/github.com/googleapis/googleapis \
    -import-path $S/protovendor/github.com/grpc-ecosystem/grpc-gateway "$@" 2>&1 \
    | tr '\n' ' ' | tr -s ' ' | sed -E 's/^ERROR: Code: Internal Message: /INTERNAL /' | cut -c1-90
}
date -u +"run at %Y-%m-%dT%H:%M:%SZ"
while IFS='|' read -r name proto method; do
  for t in none 1 30 300; do
    opt=(); [[ $t != none ]] && opt=(-max-time "$t")
    echo "$name | max-time=$t | $(g ${opt[@]+"${opt[@]}"} -proto "$proto" -d '{}' grpc.api.kentik.com:443 "$method")"
  done
done <<'EOF'
alerting|kentik/alerting/public/v202505/mitigation_method.proto|kentik.alerting.public.v202505.MitigationMethodsService/List
audit|kentik/audit/public/v202601/audit.proto|kentik.audit.public.v202601.AuditService/ListAuditEvents
custom_application|kentik/custom_application/v202501alpha1/custom_application.proto|kentik.custom_application.v202501alpha1.CustomApplicationService/ListCustomApplications
custom_dimension|kentik/custom_dimension/v202411alpha1/custom_dimension.proto|kentik.custom_dimension.v202411alpha1.CustomDimensionService/ListCustomDimensions
plan|kentik/plan/v202501alpha1/plan.proto|kentik.plan.v202501alpha1.PlanService/ListPlans
saved_filter|kentik/saved_filter/v202501alpha1/saved_filter.proto|kentik.saved_filter.v202501alpha1.SavedFilterService/ListSavedFilters
label (control)|kentik/label/v202210/label.proto|kentik.label.v202210.LabelService/ListLabels
EOF
