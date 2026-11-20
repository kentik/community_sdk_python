# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    SilenceNotificationsCreateError,
    SilenceNotificationsDeleteError,
    SilenceNotificationsGetError,
    SilenceNotificationsListError,
    SilenceNotificationsReplaceError,
)
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


def Create(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: AlertSilenceNotificationsServiceCreateRequest,
) -> AlertSilenceNotificationsServiceCreateResponse:
    """
    Create Alert Silence Notifications

    Creates a new alert silence notifications configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/alerts/silence",
        path_template="/v202505/alerts/silence",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Create",
        error_cls=SilenceNotificationsCreateError,
    )

    return parse_response_model(
        AlertSilenceNotificationsServiceCreateResponse,
        body,
        operation_name="Create",
        method="post",
        path="/v202505/alerts/silence",
    )


def List(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: AlertSilenceNotificationsServiceListRequest,
) -> AlertSilenceNotificationsServiceListResponse:
    """
    List Alert Notification Silences

    Returns a list of alert silence notifications configurations.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/alerts/silence/list",
        path_template="/v202505/alerts/silence/list",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="List",
        error_cls=SilenceNotificationsListError,
    )

    return parse_response_model(
        AlertSilenceNotificationsServiceListResponse,
        body,
        operation_name="List",
        method="post",
        path="/v202505/alerts/silence/list",
    )


def Get(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> AlertSilenceNotificationsServiceGetResponse:
    """
    Get Alert Silence Notifications

    Returns an alert silence notifications configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/v202505/alerts/silence/{path_segment(id)}",
        path_template="/v202505/alerts/silence/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Get",
        error_cls=SilenceNotificationsGetError,
    )

    return parse_response_model(
        AlertSilenceNotificationsServiceGetResponse,
        body,
        operation_name="Get",
        method="get",
        path="/v202505/alerts/silence/{id}",
    )


def Delete(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> AlertSilenceNotificationsServiceDeleteResponse:
    """
    Delete Alert Notification Silence

    Deletes an alert silence notifications configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/v202505/alerts/silence/{path_segment(id)}",
        path_template="/v202505/alerts/silence/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Delete",
        error_cls=SilenceNotificationsDeleteError,
    )

    return parse_response_model(
        AlertSilenceNotificationsServiceDeleteResponse,
        body,
        operation_name="Delete",
        method="delete",
        path="/v202505/alerts/silence/{id}",
    )


def Replace(
    api_config_override: Optional[APIConfig] = None,
    *,
    id: str,
    data: AlertSilenceNotificationsServiceReplaceBody,
) -> AlertSilenceNotificationsServiceReplaceResponse:
    """
    Replace Alert Notification Silence

    Replaces an alert silence notifications configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/v202505/alerts/silence/{path_segment(id)}",
        path_template="/v202505/alerts/silence/{id}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Replace",
        error_cls=SilenceNotificationsReplaceError,
    )

    return parse_response_model(
        AlertSilenceNotificationsServiceReplaceResponse,
        body,
        operation_name="Replace",
        method="patch",
        path="/v202505/alerts/silence/{id}",
    )
