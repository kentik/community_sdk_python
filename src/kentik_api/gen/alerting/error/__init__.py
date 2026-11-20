# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException

from ..models import rpcStatus


class AlertingError(HTTPException):
    """Base service-local error for the alerting API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "AlertingError":
        preview = getattr(response, "text", "")[:200].replace("\n", " ")
        headers = getattr(response, "headers", {})
        content_type = (
            headers.get("content-type", "unknown")
            if hasattr(headers, "get")
            else "unknown"
        )
        details: dict[str, Any] = {
            "content_type": content_type,
            "preview": preview,
        }
        message = f"{operation_name} failed with status code: {getattr(response, 'status_code', 'unknown')}"
        try:
            payload = response.json()
        except Exception:
            payload = None
        if isinstance(payload, dict):
            details["response_json"] = payload
            if isinstance(payload.get("error"), str) and payload["error"]:
                message = f"{message}: {payload['error']}"
            try:
                status = rpcStatus.model_validate(payload)
            except Exception:
                status = None
            if status is not None:
                details["rpc_status"] = payload
                if status.code is not None:
                    details["rpc_status_code"] = status.code
                if status.message:
                    message = status.message
                else:
                    message = payload.get("message") or message
            else:
                message = payload.get("message") or message
        elif payload is not None:
            details["response_json"] = payload
        return cls(
            getattr(response, "status_code", 500),
            message,
            method=method,
            path=path,
            details=details,
        )

    @classmethod
    def from_response(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "AlertingError":
        status_key = str(getattr(response, "status_code", ""))
        response_error_map = getattr(cls, "response_error_map", {})
        target_cls = (
            response_error_map.get(status_key)
            or response_error_map.get("default")
            or cls
        )
        return target_cls._build_error(
            response,
            operation_name=operation_name,
            method=method,
            path=path,
        )


class AckError(AlertingError):
    """Operation-local error for client.alerting.ack()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AckUnexpectedError(AckError):
    """Operation-local response error for ack (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AckError.response_error_map = {
    "default": AckUnexpectedError,
}


class ActError(AlertingError):
    """Operation-local error for client.alerting.act()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class ActUnexpectedError(ActError):
    """Operation-local response error for act (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ActError.response_error_map = {
    "default": ActUnexpectedError,
}


class AddCommentError(AlertingError):
    """Operation-local error for client.alerting.add_comment()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AddCommentUnexpectedError(AddCommentError):
    """Operation-local response error for add_comment (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AddCommentError.response_error_map = {
    "default": AddCommentUnexpectedError,
}


class AutoAckCreateError(AlertingError):
    """Operation-local error for client.alerting.auto_ack_create()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AutoAckCreateUnexpectedError(AutoAckCreateError):
    """Operation-local response error for auto_ack_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AutoAckCreateError.response_error_map = {
    "default": AutoAckCreateUnexpectedError,
}


class AutoAckDeleteError(AlertingError):
    """Operation-local error for client.alerting.auto_ack_delete()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AutoAckDeleteUnexpectedError(AutoAckDeleteError):
    """Operation-local response error for auto_ack_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AutoAckDeleteError.response_error_map = {
    "default": AutoAckDeleteUnexpectedError,
}


class AutoAckGetError(AlertingError):
    """Operation-local error for client.alerting.auto_ack_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AutoAckGetUnexpectedError(AutoAckGetError):
    """Operation-local response error for auto_ack_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AutoAckGetError.response_error_map = {
    "default": AutoAckGetUnexpectedError,
}


class AutoAckListError(AlertingError):
    """Operation-local error for client.alerting.auto_ack_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AutoAckListUnexpectedError(AutoAckListError):
    """Operation-local response error for auto_ack_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AutoAckListError.response_error_map = {
    "default": AutoAckListUnexpectedError,
}


class AutoAckReplaceError(AlertingError):
    """Operation-local error for client.alerting.auto_ack_replace()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AutoAckReplaceUnexpectedError(AutoAckReplaceError):
    """Operation-local response error for auto_ack_replace (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AutoAckReplaceError.response_error_map = {
    "default": AutoAckReplaceUnexpectedError,
}


class AvailableActionsError(AlertingError):
    """Operation-local error for client.alerting.available_actions()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AvailableActionsUnexpectedError(AvailableActionsError):
    """Operation-local response error for available_actions (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AvailableActionsError.response_error_map = {
    "default": AvailableActionsUnexpectedError,
}


class AvailableActionsForMitigationError(AlertingError):
    """Operation-local error for client.alerting.available_actions_for_mitigation()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class AvailableActionsForMitigationUnexpectedError(AvailableActionsForMitigationError):
    """Operation-local response error for available_actions_for_mitigation (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


AvailableActionsForMitigationError.response_error_map = {
    "default": AvailableActionsForMitigationUnexpectedError,
}


class ClearError(AlertingError):
    """Operation-local error for client.alerting.clear()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class ClearUnexpectedError(ClearError):
    """Operation-local response error for clear (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ClearError.response_error_map = {
    "default": ClearUnexpectedError,
}


class DisableError(AlertingError):
    """Operation-local error for client.alerting.disable()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class DisableUnexpectedError(DisableError):
    """Operation-local response error for disable (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


DisableError.response_error_map = {
    "default": DisableUnexpectedError,
}


class EnableError(AlertingError):
    """Operation-local error for client.alerting.enable()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class EnableUnexpectedError(EnableError):
    """Operation-local response error for enable (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


EnableError.response_error_map = {
    "default": EnableUnexpectedError,
}


class GetError(AlertingError):
    """Operation-local error for client.alerting.get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class GetUnexpectedError(GetError):
    """Operation-local response error for get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


GetError.response_error_map = {
    "default": GetUnexpectedError,
}


class ListError(AlertingError):
    """Operation-local error for client.alerting.list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class ListUnexpectedError(ListError):
    """Operation-local response error for list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListError.response_error_map = {
    "default": ListUnexpectedError,
}


class ListCommentsError(AlertingError):
    """Operation-local error for client.alerting.list_comments()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class ListCommentsUnexpectedError(ListCommentsError):
    """Operation-local response error for list_comments (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


ListCommentsError.response_error_map = {
    "default": ListCommentsUnexpectedError,
}


class MitigationMethodsGetError(AlertingError):
    """Operation-local error for client.alerting.mitigation_methods_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationMethodsGetUnexpectedError(MitigationMethodsGetError):
    """Operation-local response error for mitigation_methods_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationMethodsGetError.response_error_map = {
    "default": MitigationMethodsGetUnexpectedError,
}


class MitigationMethodsListError(AlertingError):
    """Operation-local error for client.alerting.mitigation_methods_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationMethodsListUnexpectedError(MitigationMethodsListError):
    """Operation-local response error for mitigation_methods_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationMethodsListError.response_error_map = {
    "default": MitigationMethodsListUnexpectedError,
}


class MitigationPlatformsGetError(AlertingError):
    """Operation-local error for client.alerting.mitigation_platforms_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationPlatformsGetUnexpectedError(MitigationPlatformsGetError):
    """Operation-local response error for mitigation_platforms_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationPlatformsGetError.response_error_map = {
    "default": MitigationPlatformsGetUnexpectedError,
}


class MitigationPlatformsListError(AlertingError):
    """Operation-local error for client.alerting.mitigation_platforms_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationPlatformsListUnexpectedError(MitigationPlatformsListError):
    """Operation-local response error for mitigation_platforms_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationPlatformsListError.response_error_map = {
    "default": MitigationPlatformsListUnexpectedError,
}


class MitigationsCreateError(AlertingError):
    """Operation-local error for client.alerting.mitigations_create()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationsCreateUnexpectedError(MitigationsCreateError):
    """Operation-local response error for mitigations_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationsCreateError.response_error_map = {
    "default": MitigationsCreateUnexpectedError,
}


class MitigationsGetError(AlertingError):
    """Operation-local error for client.alerting.mitigations_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationsGetUnexpectedError(MitigationsGetError):
    """Operation-local response error for mitigations_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationsGetError.response_error_map = {
    "default": MitigationsGetUnexpectedError,
}


class MitigationsListError(AlertingError):
    """Operation-local error for client.alerting.mitigations_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class MitigationsListUnexpectedError(MitigationsListError):
    """Operation-local response error for mitigations_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


MitigationsListError.response_error_map = {
    "default": MitigationsListUnexpectedError,
}


class PolicyGetError(AlertingError):
    """Operation-local error for client.alerting.policy_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class PolicyGetUnexpectedError(PolicyGetError):
    """Operation-local response error for policy_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PolicyGetError.response_error_map = {
    "default": PolicyGetUnexpectedError,
}


class PolicyListError(AlertingError):
    """Operation-local error for client.alerting.policy_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class PolicyListUnexpectedError(PolicyListError):
    """Operation-local response error for policy_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


PolicyListError.response_error_map = {
    "default": PolicyListUnexpectedError,
}


class SetExternalContextError(AlertingError):
    """Operation-local error for client.alerting.set_external_context()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SetExternalContextUnexpectedError(SetExternalContextError):
    """Operation-local response error for set_external_context (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SetExternalContextError.response_error_map = {
    "default": SetExternalContextUnexpectedError,
}


class SilenceNotificationsCreateError(AlertingError):
    """Operation-local error for client.alerting.silence_notifications_create()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SilenceNotificationsCreateUnexpectedError(SilenceNotificationsCreateError):
    """Operation-local response error for silence_notifications_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SilenceNotificationsCreateError.response_error_map = {
    "default": SilenceNotificationsCreateUnexpectedError,
}


class SilenceNotificationsDeleteError(AlertingError):
    """Operation-local error for client.alerting.silence_notifications_delete()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SilenceNotificationsDeleteUnexpectedError(SilenceNotificationsDeleteError):
    """Operation-local response error for silence_notifications_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SilenceNotificationsDeleteError.response_error_map = {
    "default": SilenceNotificationsDeleteUnexpectedError,
}


class SilenceNotificationsGetError(AlertingError):
    """Operation-local error for client.alerting.silence_notifications_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SilenceNotificationsGetUnexpectedError(SilenceNotificationsGetError):
    """Operation-local response error for silence_notifications_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SilenceNotificationsGetError.response_error_map = {
    "default": SilenceNotificationsGetUnexpectedError,
}


class SilenceNotificationsListError(AlertingError):
    """Operation-local error for client.alerting.silence_notifications_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SilenceNotificationsListUnexpectedError(SilenceNotificationsListError):
    """Operation-local response error for silence_notifications_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SilenceNotificationsListError.response_error_map = {
    "default": SilenceNotificationsListUnexpectedError,
}


class SilenceNotificationsReplaceError(AlertingError):
    """Operation-local error for client.alerting.silence_notifications_replace()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SilenceNotificationsReplaceUnexpectedError(SilenceNotificationsReplaceError):
    """Operation-local response error for silence_notifications_replace (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SilenceNotificationsReplaceError.response_error_map = {
    "default": SilenceNotificationsReplaceUnexpectedError,
}


class SuppressionCreateError(AlertingError):
    """Operation-local error for client.alerting.suppression_create()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SuppressionCreateUnexpectedError(SuppressionCreateError):
    """Operation-local response error for suppression_create (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SuppressionCreateError.response_error_map = {
    "default": SuppressionCreateUnexpectedError,
}


class SuppressionDeleteError(AlertingError):
    """Operation-local error for client.alerting.suppression_delete()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SuppressionDeleteUnexpectedError(SuppressionDeleteError):
    """Operation-local response error for suppression_delete (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SuppressionDeleteError.response_error_map = {
    "default": SuppressionDeleteUnexpectedError,
}


class SuppressionGetError(AlertingError):
    """Operation-local error for client.alerting.suppression_get()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SuppressionGetUnexpectedError(SuppressionGetError):
    """Operation-local response error for suppression_get (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SuppressionGetError.response_error_map = {
    "default": SuppressionGetUnexpectedError,
}


class SuppressionListError(AlertingError):
    """Operation-local error for client.alerting.suppression_list()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SuppressionListUnexpectedError(SuppressionListError):
    """Operation-local response error for suppression_list (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SuppressionListError.response_error_map = {
    "default": SuppressionListUnexpectedError,
}


class SuppressionReplaceError(AlertingError):
    """Operation-local error for client.alerting.suppression_replace()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class SuppressionReplaceUnexpectedError(SuppressionReplaceError):
    """Operation-local response error for suppression_replace (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


SuppressionReplaceError.response_error_map = {
    "default": SuppressionReplaceUnexpectedError,
}


class UnAckError(AlertingError):
    """Operation-local error for client.alerting.un_ack()."""

    response_error_map: dict[str, type[AlertingError]] = {}


class UnAckUnexpectedError(UnAckError):
    """Operation-local response error for un_ack (default: An unexpected error response. #/components/schemas/rpcStatus)."""

    pass


UnAckError.response_error_map = {
    "default": UnAckUnexpectedError,
}

ERROR_BY_METHOD: dict[str, type[AlertingError]] = {
    "ack": AckError,
    "act": ActError,
    "add_comment": AddCommentError,
    "auto_ack_create": AutoAckCreateError,
    "auto_ack_delete": AutoAckDeleteError,
    "auto_ack_get": AutoAckGetError,
    "auto_ack_list": AutoAckListError,
    "auto_ack_replace": AutoAckReplaceError,
    "available_actions": AvailableActionsError,
    "available_actions_for_mitigation": AvailableActionsForMitigationError,
    "clear": ClearError,
    "disable": DisableError,
    "enable": EnableError,
    "get": GetError,
    "list": ListError,
    "list_comments": ListCommentsError,
    "mitigation_methods_get": MitigationMethodsGetError,
    "mitigation_methods_list": MitigationMethodsListError,
    "mitigation_platforms_get": MitigationPlatformsGetError,
    "mitigation_platforms_list": MitigationPlatformsListError,
    "mitigations_create": MitigationsCreateError,
    "mitigations_get": MitigationsGetError,
    "mitigations_list": MitigationsListError,
    "policy_get": PolicyGetError,
    "policy_list": PolicyListError,
    "set_external_context": SetExternalContextError,
    "silence_notifications_create": SilenceNotificationsCreateError,
    "silence_notifications_delete": SilenceNotificationsDeleteError,
    "silence_notifications_get": SilenceNotificationsGetError,
    "silence_notifications_list": SilenceNotificationsListError,
    "silence_notifications_replace": SilenceNotificationsReplaceError,
    "suppression_create": SuppressionCreateError,
    "suppression_delete": SuppressionDeleteError,
    "suppression_get": SuppressionGetError,
    "suppression_list": SuppressionListError,
    "suppression_replace": SuppressionReplaceError,
    "un_ack": UnAckError,
}

__all__ = [
    "AlertingError",
    "AckUnexpectedError",
    "ActUnexpectedError",
    "AddCommentUnexpectedError",
    "AutoAckCreateUnexpectedError",
    "AutoAckDeleteUnexpectedError",
    "AutoAckGetUnexpectedError",
    "AutoAckListUnexpectedError",
    "AutoAckReplaceUnexpectedError",
    "AvailableActionsUnexpectedError",
    "AvailableActionsForMitigationUnexpectedError",
    "ClearUnexpectedError",
    "DisableUnexpectedError",
    "EnableUnexpectedError",
    "GetUnexpectedError",
    "ListUnexpectedError",
    "ListCommentsUnexpectedError",
    "MitigationMethodsGetUnexpectedError",
    "MitigationMethodsListUnexpectedError",
    "MitigationPlatformsGetUnexpectedError",
    "MitigationPlatformsListUnexpectedError",
    "MitigationsCreateUnexpectedError",
    "MitigationsGetUnexpectedError",
    "MitigationsListUnexpectedError",
    "PolicyGetUnexpectedError",
    "PolicyListUnexpectedError",
    "SetExternalContextUnexpectedError",
    "SilenceNotificationsCreateUnexpectedError",
    "SilenceNotificationsDeleteUnexpectedError",
    "SilenceNotificationsGetUnexpectedError",
    "SilenceNotificationsListUnexpectedError",
    "SilenceNotificationsReplaceUnexpectedError",
    "SuppressionCreateUnexpectedError",
    "SuppressionDeleteUnexpectedError",
    "SuppressionGetUnexpectedError",
    "SuppressionListUnexpectedError",
    "SuppressionReplaceUnexpectedError",
    "UnAckUnexpectedError",
    "AckError",
    "ActError",
    "AddCommentError",
    "AutoAckCreateError",
    "AutoAckDeleteError",
    "AutoAckGetError",
    "AutoAckListError",
    "AutoAckReplaceError",
    "AvailableActionsError",
    "AvailableActionsForMitigationError",
    "ClearError",
    "DisableError",
    "EnableError",
    "GetError",
    "ListError",
    "ListCommentsError",
    "MitigationMethodsGetError",
    "MitigationMethodsListError",
    "MitigationPlatformsGetError",
    "MitigationPlatformsListError",
    "MitigationsCreateError",
    "MitigationsGetError",
    "MitigationsListError",
    "PolicyGetError",
    "PolicyListError",
    "SetExternalContextError",
    "SilenceNotificationsCreateError",
    "SilenceNotificationsDeleteError",
    "SilenceNotificationsGetError",
    "SilenceNotificationsListError",
    "SilenceNotificationsReplaceError",
    "SuppressionCreateError",
    "SuppressionDeleteError",
    "SuppressionGetError",
    "SuppressionListError",
    "SuppressionReplaceError",
    "UnAckError",
    "ERROR_BY_METHOD",
]
