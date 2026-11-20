# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DeviceSnmpV3Conf(BaseModel):
    """
    DeviceSnmpV3Conf
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    username: Optional[str] = Field(
        validation_alias="username",
        default=None,
        description="UserName (username) - the user name to use to authenticate via SNMP v3. ** UserName is required when device_snmp_v3_conf is not null",
    )

    authenticationProtocol: Optional[str] = Field(
        validation_alias="authenticationProtocol",
        default=None,
        description="Authentication Protocol (authentication_protocol) - the auth protocol to use via SNMP v3",
    )

    authenticationPassphrase: Optional[str] = Field(
        validation_alias="authenticationPassphrase",
        default=None,
        description="Authentication Passphrase (authentication_passphrase) - the passphrase to use for SNMP v3 authentication protocol (required when AuthenticationProtocol not NoAuth)",
    )

    privacyProtocol: Optional[str] = Field(
        validation_alias="privacyProtocol",
        default=None,
        description="Privacy Protocol (privacy_protocol) - the privacy protocol to use to authenticate via SNMP v3",
    )

    privacyPassphrase: Optional[str] = Field(
        validation_alias="privacyPassphrase",
        default=None,
        description="Privacy Passphrase (privacy_passphrase) - the passphrase to use for SNMP v3 privacy protocol (required when PrivacyProtocol not NoPriv)",
    )
