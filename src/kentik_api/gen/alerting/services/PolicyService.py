# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import DisableError, EnableError, PolicyGetError, PolicyListError
from ..models import (  # noqa: F401
    AggregationType,
    Alert,
    AlertAcknowledgement,
    AlertAutoAck,
    AlertAutoAckFilters,
    AlertAutoAckServiceCreateRequest,
    AlertAutoAckServiceCreateResponse,
    AlertAutoAckServiceDeleteResponse,
    AlertAutoAckServiceGetResponse,
    AlertAutoAckServiceListRequest,
    AlertAutoAckServiceListResponse,
    AlertAutoAckServiceReplaceBody,
    AlertAutoAckServiceReplaceResponse,
    AlertFilters,
    AlertPhase,
    AlertServiceAckBody,
    AlertServiceAckResponse,
    AlertServiceAddCommentBody,
    AlertServiceAddCommentResponse,
    AlertServiceClearRequest,
    AlertServiceClearResponse,
    AlertServiceGetResponse,
    AlertServiceListCommentsResponse,
    AlertServiceListRequest,
    AlertServiceListResponse,
    AlertServiceSetExternalContextBody,
    AlertServiceSetExternalContextResponse,
    AlertServiceUnAckBody,
    AlertServiceUnAckResponse,
    AlertSilenceNotificationFilters,
    AlertSilenceNotificationsDefinition,
    AlertSilenceNotificationsServiceCreateRequest,
    AlertSilenceNotificationsServiceCreateResponse,
    AlertSilenceNotificationsServiceDeleteResponse,
    AlertSilenceNotificationsServiceGetResponse,
    AlertSilenceNotificationsServiceListRequest,
    AlertSilenceNotificationsServiceListResponse,
    AlertSilenceNotificationsServiceReplaceBody,
    AlertSilenceNotificationsServiceReplaceResponse,
    AlertState,
    AttributeFilter,
    AttributeFilterStringArray,
    BaselineConditionDeltaType,
    BaselineConfigCompareMode,
    BitwiseOp,
    Comment,
    ConditionsBaselineCondition,
    ConditionsForecastCondition,
    ConditionsInterfaceCapacityCondition,
    ConditionsRatioCondition,
    ConditionsStaticCondition,
    ConditionsTopKeysCondition,
    ContextFilter,
    ContextFilterConjunction,
    EventPolicyLevelSettings,
    EventPolicySettings,
    EventPolicySettingsEventType,
    ExternalContext,
    FieldBy,
    FlowContext,
    FlowContextActivationStatus,
    FlowContextAlertKeyDetails,
    FlowContextDeviceDetails,
    FlowContextInterfaceDetails,
    FlowContextMetricValue,
    FlowContextSiteDetails,
    FlowPolicyLevelSettings,
    FlowPolicyLevelSettingsActivationSettings,
    FlowPolicyLevelSettingsConditions,
    FlowPolicyLevelSettingsConditionsOperator,
    FlowPolicyLevelSettingsMitigationAssociation,
    FlowPolicySettings,
    FlowPolicySettingsBaselineConfig,
    FlowPolicySettingsDatasetConfig,
    FlowPolicySettingsEvaluationConfig,
    FlowspecMatch,
    Fragment,
    FragmentFormula,
    FragmentPredicate,
    FragmentPredicateGroup,
    IdentityPredicate,
    IdentityPredicateIdentityList,
    IpPredicate,
    IpPredicateStringList,
    JiraCloudContext,
    KeyValue,
    KeyValueFilter,
    LabelPredicate,
    LabelPredicateStringList,
    Mitigation,
    MitigationActionDetail,
    MitigationEvent,
    MitigationFilters,
    MitigationMethod,
    MitigationMethodsFilters,
    MitigationMethodsServiceGetResponse,
    MitigationMethodsServiceListResponse,
    MitigationPlatform,
    MitigationPlatformsFilters,
    MitigationPlatformsServiceGetResponse,
    MitigationPlatformsServiceListResponse,
    MitigationPlatformType,
    MitigationsActResult,
    MitigationsServiceActBody,
    MitigationsServiceActResponse,
    MitigationsServiceAvailableActionsForMitigationResponse,
    MitigationsServiceAvailableActionsResponse,
    MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions,
    MitigationsServiceCreateRequest,
    MitigationsServiceCreateResponse,
    MitigationsServiceGetResponse,
    MitigationsServiceListResponse,
    MitigationState,
    MitigationStateEntry,
    MitigationTarget,
    MitigationType,
    MitigationUserAction,
    MultiAttributeFilter,
    NetworkScope,
    NmsActivateOrClearConditions,
    NmsCondition,
    NmsConditionConnector,
    NmsConditionGroup,
    NmsConditionOperator,
    NmsContext,
    NmsContextActivationInfo,
    NmsContextAlarmMetricMap,
    NmsContextAlarmTarget,
    NmsContextDatasetInfo,
    NmsPolicyLevelSettings,
    NmsPolicyLevelSettingsClearType,
    NmsPolicySettings,
    NmsPolicySettingsDatasetConfig,
    NmsPolicySettingsEvaluationConfig,
    NmsStateChangeCondition,
    NmsStateSet,
    NmsThresholdCondition,
    NotificationChannelAssociation,
    NumericFormula,
    NumericOp,
    NumericPredicate,
    NumericPredicateGroup,
    PaginationConfig,
    PaginationInfo,
    Policy,
    PolicyDataSources,
    PolicyDataSourcesDeviceTag,
    PolicyDimensionFilters,
    PolicyDimensionFiltersConjunction,
    PolicyDimensionFiltersEntry,
    PolicyDimensionFiltersEntryStringArray,
    PolicyFilters,
    PolicyFiltersFieldFilter,
    PolicyFiltersFilterConnector,
    PolicyFiltersOperator,
    PolicyFiltersSavedFilter,
    PolicyListFilters,
    PolicyPolicyErrorInfo,
    PolicyPolicyLevel,
    PolicyServiceDisableBody,
    PolicyServiceDisableResponse,
    PolicyServiceEnableBody,
    PolicyServiceEnableResponse,
    PolicyServiceGetResponse,
    PolicyServiceListRequest,
    PolicyServiceListResponse,
    PolicyType,
    ProducerPredicates,
    RatioConditionDirection,
    ScopedClause,
    ServiceNowContext,
    Severity,
    SimpleAttributeFilter,
    SimpleAttributeFilterStringArray,
    SortingConfig,
    SortingConfigField,
    SortingConfigOrder,
    Source,
    StringPredicate,
    StringPredicateStringList,
    SubjectPredicates,
    Suppression,
    SuppressionFilters,
    SuppressionServiceCreateRequest,
    SuppressionServiceCreateResponse,
    SuppressionServiceDeleteResponse,
    SuppressionServiceGetResponse,
    SuppressionServiceListRequest,
    SuppressionServiceListResponse,
    SuppressionServiceReplaceBody,
    SuppressionServiceReplaceResponse,
    TCPFlag,
    TCPFlagsFormula,
    TCPFlagsPredicate,
    TCPFlagsPredicateGroup,
    TimeRange,
    TimestampSetting,
    TopKeysConditionTopKeysEvent,
    protobufAny,
    rpcStatus,
    v202505AlertAcknowledgement,
    v202505PolicyType,
    v202505Source,
)


def List(
    api_config_override: Optional[APIConfig] = None, *, data: PolicyServiceListRequest
) -> PolicyServiceListResponse:
    """
    List Policies

    Returns a list of alerting policies.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/policies/list",
        path_template="/v202505/policies/list",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="List",
        error_cls=PolicyListError,
    )

    return parse_response_model(
        PolicyServiceListResponse,
        body,
        operation_name="List",
        method="post",
        path="/v202505/policies/list",
    )


def Get(
    api_config_override: Optional[APIConfig] = None, *, policyType: str, id: str
) -> PolicyServiceGetResponse:
    """
    Get Policy

    Returns an alerting policy.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/v202505/policies/{path_segment(policyType)}/{path_segment(id)}",
        path_template="/v202505/policies/{policyType}/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Get",
        error_cls=PolicyGetError,
    )

    return parse_response_model(
        PolicyServiceGetResponse,
        body,
        operation_name="Get",
        method="get",
        path="/v202505/policies/{policyType}/{id}",
    )


def Disable(
    api_config_override: Optional[APIConfig] = None,
    *,
    policyType: str,
    id: str,
    data: PolicyServiceDisableBody,
) -> PolicyServiceDisableResponse:
    """
    Disable Policy

    Disables an alerting policy.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/v202505/policies/{path_segment(policyType)}/{path_segment(id)}/disable",
        path_template="/v202505/policies/{policyType}/{id}/disable",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Disable",
        error_cls=DisableError,
    )

    return parse_response_model(
        PolicyServiceDisableResponse,
        body,
        operation_name="Disable",
        method="post",
        path="/v202505/policies/{policyType}/{id}/disable",
    )


def Enable(
    api_config_override: Optional[APIConfig] = None,
    *,
    policyType: str,
    id: str,
    data: PolicyServiceEnableBody,
) -> PolicyServiceEnableResponse:
    """
    Enable Policy

    Enables an alerting policy.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/v202505/policies/{path_segment(policyType)}/{path_segment(id)}/enable",
        path_template="/v202505/policies/{policyType}/{id}/enable",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Enable",
        error_cls=EnableError,
    )

    return parse_response_model(
        PolicyServiceEnableResponse,
        body,
        operation_name="Enable",
        method="post",
        path="/v202505/policies/{policyType}/{id}/enable",
    )
