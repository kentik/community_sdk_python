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
    AutoAckCreateError,
    AutoAckDeleteError,
    AutoAckGetError,
    AutoAckListError,
    AutoAckReplaceError,
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
    data: AlertAutoAckServiceCreateRequest,
) -> AlertAutoAckServiceCreateResponse:
    """
    Create Auto-Ack

    Creates a new auto-ack configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/alerts/ack/auto",
        path_template="/v202505/alerts/ack/auto",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Create",
        error_cls=AutoAckCreateError,
    )

    return parse_response_model(
        AlertAutoAckServiceCreateResponse,
        body,
        operation_name="Create",
        method="post",
        path="/v202505/alerts/ack/auto",
    )


def List(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: AlertAutoAckServiceListRequest,
) -> AlertAutoAckServiceListResponse:
    """
    List Auto-Acks

    Returns a list of auto-ack configurations.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/alerts/ack/auto/list",
        path_template="/v202505/alerts/ack/auto/list",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="List",
        error_cls=AutoAckListError,
    )

    return parse_response_model(
        AlertAutoAckServiceListResponse,
        body,
        operation_name="List",
        method="post",
        path="/v202505/alerts/ack/auto/list",
    )


def Get(
    api_config_override: Optional[APIConfig] = None, *, autoAckid: str
) -> AlertAutoAckServiceGetResponse:
    """
    Get Auto-Ack

    Returns an auto-ack configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/v202505/alerts/ack/auto/{path_segment(autoAckid)}",
        path_template="/v202505/alerts/ack/auto/{autoAck.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Get",
        error_cls=AutoAckGetError,
    )

    return parse_response_model(
        AlertAutoAckServiceGetResponse,
        body,
        operation_name="Get",
        method="get",
        path="/v202505/alerts/ack/auto/{autoAck.id}",
    )


def Delete(
    api_config_override: Optional[APIConfig] = None, *, autoAckid: str
) -> AlertAutoAckServiceDeleteResponse:
    """
    Delete Auto-Ack

    Deletes an auto-ack configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="delete",
        path=f"/v202505/alerts/ack/auto/{path_segment(autoAckid)}",
        path_template="/v202505/alerts/ack/auto/{autoAck.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Delete",
        error_cls=AutoAckDeleteError,
    )

    return parse_response_model(
        AlertAutoAckServiceDeleteResponse,
        body,
        operation_name="Delete",
        method="delete",
        path="/v202505/alerts/ack/auto/{autoAck.id}",
    )


def Replace(
    api_config_override: Optional[APIConfig] = None,
    *,
    autoAckid: str,
    data: AlertAutoAckServiceReplaceBody,
) -> AlertAutoAckServiceReplaceResponse:
    """
    Replace Auto-Ack

    Replaces an auto-ack configuration.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="patch",
        path=f"/v202505/alerts/ack/auto/{path_segment(autoAckid)}",
        path_template="/v202505/alerts/ack/auto/{autoAck.id}",
        api_config_override=api_config_override,
        query_params=query_params,
        # Upstream REST drops this camelCase key: AGENTS.md, Upstream workarounds.
        json_body={
            {"autoAck": "auto_ack"}.get(key, key): value
            for key, value in data.model_dump(by_alias=True, exclude_unset=True).items()
        },
        header_params=header_params,
        expected_status=200,
        operation_name="Replace",
        error_cls=AutoAckReplaceError,
    )

    return parse_response_model(
        AlertAutoAckServiceReplaceResponse,
        body,
        operation_name="Replace",
        method="patch",
        path="/v202505/alerts/ack/auto/{autoAck.id}",
    )
