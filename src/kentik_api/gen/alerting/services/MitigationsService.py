# AUTO-GENERATED: scripts/openapi_templates/service.jinja2 via openapi-python-generator
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional
from typing import List as TypingList

from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import (
    parse_response_model,
    path_segment,
    request_json,
)

from ..error import (
    ActError,
    AvailableActionsError,
    AvailableActionsForMitigationError,
    MitigationsCreateError,
    MitigationsGetError,
    MitigationsListError,
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


def List(
    api_config_override: Optional[APIConfig] = None,
    *,
    paginationlimit: Optional[str] = None,
    paginationoffset: Optional[str] = None,
    paginationincludeTotalCount: Optional[bool] = None,
    filterscreatedAtstart: Optional[str] = None,
    filterscreatedAtend: Optional[str] = None,
    filtersmitigationIds: Optional[TypingList[str]] = None,
    filtersalarmIds: Optional[TypingList[str]] = None,
    filtersstates: Optional[TypingList[str]] = None,
    filtersplatformIds: Optional[TypingList[str]] = None,
    filtersmethodIds: Optional[TypingList[str]] = None,
    filtersipCidrs: Optional[TypingList[str]] = None,
    filtersipCidrPattern: Optional[str] = None,
    filterstypes: Optional[TypingList[str]] = None,
) -> MitigationsServiceListResponse:
    """
    List Mitigations

    Returns a list of mitigations.
    """
    query_params: Dict[str, Any] = {
        "pagination.limit": paginationlimit,
        "pagination.offset": paginationoffset,
        "pagination.includeTotalCount": paginationincludeTotalCount,
        "filters.createdAt.start": filterscreatedAtstart,
        "filters.createdAt.end": filterscreatedAtend,
        "filters.mitigationIds": filtersmitigationIds,
        "filters.alarmIds": filtersalarmIds,
        "filters.states": filtersstates,
        "filters.platformIds": filtersplatformIds,
        "filters.methodIds": filtersmethodIds,
        "filters.ipCidrs": filtersipCidrs,
        "filters.ipCidrPattern": filtersipCidrPattern,
        "filters.types": filterstypes,
    }

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/v202505/mitigations",
        path_template="/v202505/mitigations",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="List",
        error_cls=MitigationsListError,
    )

    return parse_response_model(
        MitigationsServiceListResponse,
        body,
        operation_name="List",
        method="get",
        path="/v202505/mitigations",
    )


def Create(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: MitigationsServiceCreateRequest,
) -> MitigationsServiceCreateResponse:
    """
    Create Mitigation

    Creates a new manual mitigation.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path="/v202505/mitigations",
        path_template="/v202505/mitigations",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Create",
        error_cls=MitigationsCreateError,
    )

    return parse_response_model(
        MitigationsServiceCreateResponse,
        body,
        operation_name="Create",
        method="post",
        path="/v202505/mitigations",
    )


def AvailableActions(
    api_config_override: Optional[APIConfig] = None,
) -> MitigationsServiceAvailableActionsResponse:
    """
    Get Available Actions

    Returns available actions for mitigations.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path="/v202505/mitigations/actions",
        path_template="/v202505/mitigations/actions",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="AvailableActions",
        error_cls=AvailableActionsError,
    )

    return parse_response_model(
        MitigationsServiceAvailableActionsResponse,
        body,
        operation_name="AvailableActions",
        method="get",
        path="/v202505/mitigations/actions",
    )


def Get(
    api_config_override: Optional[APIConfig] = None, *, action: str
) -> MitigationsServiceGetResponse:
    """
    Get Mitigation

    Returns a mitigation.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/v202505/mitigations/{path_segment(action)}",
        path_template="/v202505/mitigations/{action}",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="Get",
        error_cls=MitigationsGetError,
    )

    return parse_response_model(
        MitigationsServiceGetResponse,
        body,
        operation_name="Get",
        method="get",
        path="/v202505/mitigations/{action}",
    )


def Act(
    api_config_override: Optional[APIConfig] = None,
    *,
    action: str,
    data: MitigationsServiceActBody,
) -> MitigationsServiceActResponse:
    """
    Act on Mitigation

    Performs an action on one or more mitigations.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="post",
        path=f"/v202505/mitigations/{path_segment(action)}",
        path_template="/v202505/mitigations/{action}",
        api_config_override=api_config_override,
        query_params=query_params,
        json_body=data.model_dump(by_alias=True, exclude_unset=True),
        header_params=header_params,
        expected_status=200,
        operation_name="Act",
        error_cls=ActError,
    )

    return parse_response_model(
        MitigationsServiceActResponse,
        body,
        operation_name="Act",
        method="post",
        path="/v202505/mitigations/{action}",
    )


def AvailableActionsForMitigation(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> MitigationsServiceAvailableActionsForMitigationResponse:
    """
    Get Available Actions for Mitigation

    Returns available actions for a specific mitigation.
    """
    query_params: Dict[str, Any] = {}

    header_params: Dict[str, Any] = {}

    body = request_json(
        method="get",
        path=f"/v202505/mitigations/{path_segment(id)}/actions",
        path_template="/v202505/mitigations/{id}/actions",
        api_config_override=api_config_override,
        query_params=query_params,
        header_params=header_params,
        expected_status=200,
        operation_name="AvailableActionsForMitigation",
        error_cls=AvailableActionsForMitigationError,
    )

    return parse_response_model(
        MitigationsServiceAvailableActionsForMitigationResponse,
        body,
        operation_name="AvailableActionsForMitigation",
        method="get",
        path="/v202505/mitigations/{id}/actions",
    )
