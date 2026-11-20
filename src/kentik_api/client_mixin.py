from typing import TYPE_CHECKING

from kentik_api.gen.ai_advisor.services.ai_advisor import AiAdvisorServiceWrapper
from kentik_api.gen.alerting.services.alerting import AlertingServiceWrapper
from kentik_api.gen.as_group.services.as_group import AsGroupServiceWrapper
from kentik_api.gen.asset_tags.services.asset_tags import AssetTagsServiceWrapper
from kentik_api.gen.audit.services.audit import AuditServiceWrapper
from kentik_api.gen.bgp_monitoring.services.bgp_monitoring import (
    BgpMonitoringServiceWrapper,
)
from kentik_api.gen.capacity_plan.services.capacity_plan import (
    CapacityPlanServiceWrapper,
)
from kentik_api.gen.cloud_export.services.cloud_export import CloudExportServiceWrapper
from kentik_api.gen.connectivity_checker.services.connectivity_checker import (
    ConnectivityCheckerServiceWrapper,
)
from kentik_api.gen.cost.services.cost import CostServiceWrapper
from kentik_api.gen.credential.services.credential import CredentialServiceWrapper
from kentik_api.gen.custom_application.services.custom_application import (
    CustomApplicationServiceWrapper,
)
from kentik_api.gen.custom_dimension.services.custom_dimension import (
    CustomDimensionServiceWrapper,
)
from kentik_api.gen.device.services.device import DeviceServiceWrapper
from kentik_api.gen.dictionary.services.dictionary import DictionaryServiceWrapper
from kentik_api.gen.enrichments.services.enrichments import EnrichmentsServiceWrapper
from kentik_api.gen.flow_tag.services.flow_tag import FlowTagServiceWrapper
from kentik_api.gen.interface.services.interface import InterfaceServiceWrapper
from kentik_api.gen.journeys.services.journeys import JourneysServiceWrapper
from kentik_api.gen.kagent.services.kagent import KagentServiceWrapper
from kentik_api.gen.kmeta.services.kmeta import KmetaServiceWrapper
from kentik_api.gen.kmi.services.kmi import KmiServiceWrapper
from kentik_api.gen.ktbgp.services.ktbgp import KtbgpServiceWrapper
from kentik_api.gen.label.services.label import LabelServiceWrapper
from kentik_api.gen.mkp.services.mkp import MkpServiceWrapper
from kentik_api.gen.network_class.services.network_class import (
    NetworkClassServiceWrapper,
)
from kentik_api.gen.nms.services.nms import NmsServiceWrapper
from kentik_api.gen.notification_channel.services.notification_channel import (
    NotificationChannelServiceWrapper,
)
from kentik_api.gen.pathfinder.services.pathfinder import PathfinderServiceWrapper
from kentik_api.gen.plan.services.plan import PlanServiceWrapper
from kentik_api.gen.rbux.services.rbux import RbuxServiceWrapper
from kentik_api.gen.saved_filter.services.saved_filter import SavedFilterServiceWrapper
from kentik_api.gen.site.services.site import SiteServiceWrapper
from kentik_api.gen.synthetics.services.synthetics import SyntheticsServiceWrapper
from kentik_api.gen.user.services.user import UserServiceWrapper
from kentik_api.gen.v5.services.v5 import V5ServiceWrapper
from kentik_api.gen.vault.services.vault import VaultServiceWrapper

if TYPE_CHECKING:
    from kentik_api.transports.grpc_client import GrpcTransport
    from kentik_api.transports.rest_client import RestTransport


class KentikClientMixin:
    """AUTO-GENERATED: scripts/generation/wrapper_generation.py, _generate_client_mixin().
    Rebuilt on every `uv run poe generate`. Do not edit by hand.
    """

    if TYPE_CHECKING:
        _transport: "GrpcTransport | RestTransport"
        _v5_transport: "RestTransport"
        ai_advisor: "AiAdvisorServiceWrapper"
        alerting: "AlertingServiceWrapper"
        as_group: "AsGroupServiceWrapper"
        asset_tags: "AssetTagsServiceWrapper"
        audit: "AuditServiceWrapper"
        bgp_monitoring: "BgpMonitoringServiceWrapper"
        capacity_plan: "CapacityPlanServiceWrapper"
        cloud_export: "CloudExportServiceWrapper"
        connectivity_checker: "ConnectivityCheckerServiceWrapper"
        cost: "CostServiceWrapper"
        credential: "CredentialServiceWrapper"
        custom_application: "CustomApplicationServiceWrapper"
        custom_dimension: "CustomDimensionServiceWrapper"
        device: "DeviceServiceWrapper"
        dictionary: "DictionaryServiceWrapper"
        enrichments: "EnrichmentsServiceWrapper"
        flow_tag: "FlowTagServiceWrapper"
        interface: "InterfaceServiceWrapper"
        journeys: "JourneysServiceWrapper"
        kagent: "KagentServiceWrapper"
        kmeta: "KmetaServiceWrapper"
        kmi: "KmiServiceWrapper"
        ktbgp: "KtbgpServiceWrapper"
        label: "LabelServiceWrapper"
        mkp: "MkpServiceWrapper"
        network_class: "NetworkClassServiceWrapper"
        nms: "NmsServiceWrapper"
        notification_channel: "NotificationChannelServiceWrapper"
        pathfinder: "PathfinderServiceWrapper"
        plan: "PlanServiceWrapper"
        rbux: "RbuxServiceWrapper"
        saved_filter: "SavedFilterServiceWrapper"
        site: "SiteServiceWrapper"
        synthetics: "SyntheticsServiceWrapper"
        user: "UserServiceWrapper"
        v5: "V5ServiceWrapper"
        vault: "VaultServiceWrapper"

    def _mount_generated_services(self) -> None:
        """Mounts all generated service wrappers using the active transport."""
        self.ai_advisor = AiAdvisorServiceWrapper(self._transport)
        self.alerting = AlertingServiceWrapper(self._transport)
        self.as_group = AsGroupServiceWrapper(self._transport)
        self.asset_tags = AssetTagsServiceWrapper(self._transport)
        self.audit = AuditServiceWrapper(self._transport)
        self.bgp_monitoring = BgpMonitoringServiceWrapper(self._transport)
        self.capacity_plan = CapacityPlanServiceWrapper(self._transport)
        self.cloud_export = CloudExportServiceWrapper(self._transport)
        self.connectivity_checker = ConnectivityCheckerServiceWrapper(self._transport)
        self.cost = CostServiceWrapper(self._transport)
        self.credential = CredentialServiceWrapper(self._transport)
        self.custom_application = CustomApplicationServiceWrapper(self._transport)
        self.custom_dimension = CustomDimensionServiceWrapper(self._transport)
        self.device = DeviceServiceWrapper(self._transport)
        self.dictionary = DictionaryServiceWrapper(self._transport)
        self.enrichments = EnrichmentsServiceWrapper(self._transport)
        self.flow_tag = FlowTagServiceWrapper(self._transport)
        self.interface = InterfaceServiceWrapper(self._transport)
        self.journeys = JourneysServiceWrapper(self._transport)
        self.kagent = KagentServiceWrapper(self._transport)
        self.kmeta = KmetaServiceWrapper(self._transport)
        self.kmi = KmiServiceWrapper(self._transport)
        self.ktbgp = KtbgpServiceWrapper(self._transport)
        self.label = LabelServiceWrapper(self._transport)
        self.mkp = MkpServiceWrapper(self._transport)
        self.network_class = NetworkClassServiceWrapper(self._transport)
        self.nms = NmsServiceWrapper(self._transport)
        self.notification_channel = NotificationChannelServiceWrapper(self._transport)
        self.pathfinder = PathfinderServiceWrapper(self._transport)
        self.plan = PlanServiceWrapper(self._transport)
        self.rbux = RbuxServiceWrapper(self._transport)
        self.saved_filter = SavedFilterServiceWrapper(self._transport)
        self.site = SiteServiceWrapper(self._transport)
        self.synthetics = SyntheticsServiceWrapper(self._transport)
        self.user = UserServiceWrapper(self._transport)
        self.v5 = V5ServiceWrapper(self._v5_transport)
        self.vault = VaultServiceWrapper(self._transport)
