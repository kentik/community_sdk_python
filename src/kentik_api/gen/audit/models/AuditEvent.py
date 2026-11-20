# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .GenericEvent import GenericEvent


class AuditEvent(BaseModel):
    """
    AuditEvent represents an audit event with request and enriched contextual information.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    userId: Optional[str] = Field(
        validation_alias="userId",
        default=None,
        description="ID of the user that produced the event",
    )

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier of the event",
    )

    ctime: Optional[str] = Field(
        validation_alias="ctime",
        default=None,
        description="Timestamp when the event was produced",
    )

    apiMethod: Optional[str] = Field(
        validation_alias="apiMethod",
        default=None,
        description="HTTP method of the request (GET, POST, PUT, PATCH, DELETE)",
    )

    apiPath: Optional[str] = Field(
        validation_alias="apiPath", default=None, description="URL path of the request"
    )

    ipAddress: Optional[str] = Field(
        validation_alias="ipAddress", default=None, description="Client IP Address"
    )

    authority: Optional[str] = Field(
        validation_alias="authority",
        default=None,
        description="Authority header from the request",
    )

    kentikUserId: Optional[str] = Field(
        validation_alias="kentikUserId",
        default=None,
        description="Kentik user ID extracted from request metadata",
    )

    kentikUserEmail: Optional[str] = Field(
        validation_alias="kentikUserEmail",
        default=None,
        description="Kentik user email extracted from request metadata",
    )

    objectType: Optional[str] = Field(
        validation_alias="objectType",
        default=None,
        description="The type of object that was affected",
    )

    objectName: Optional[str] = Field(
        validation_alias="objectName",
        default=None,
        description="Human-readable name of the affected object",
    )

    apiAction: Optional[str] = Field(
        validation_alias="apiAction",
        default=None,
        description="The action performed on the object",
    )

    source: Optional[str] = Field(
        validation_alias="source", default=None, description="The source of the request"
    )

    objectId: Optional[str] = Field(
        validation_alias="objectId",
        default=None,
        description="The ID of the affected object",
    )

    parentId: Optional[str] = Field(
        validation_alias="parentId",
        default=None,
        description="The ID of the parent object",
    )

    portalPath: Optional[str] = Field(
        validation_alias="portalPath",
        default=None,
        description="Path to view the affected object",
    )

    generic: Optional[GenericEvent] = Field(validation_alias="generic", default=None)

    titleField: Optional[str] = Field(
        validation_alias="titleField",
        default=None,
        description="Non Generic route title field",
    )

    eventPayload: Optional[str] = Field(
        validation_alias="eventPayload", default=None, description="Request Payload"
    )

    userAgent: Optional[str] = Field(
        validation_alias="userAgent", default=None, description="User agent"
    )
