# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .AssetTag import AssetTag
from .MeasurementDetail import MeasurementDetail
from .MetricFamilyDef import MetricFamilyDef
from .OperatorSet import OperatorSet


class GetDictionaryResponse(BaseModel):
    """
    GetDictionaryResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    measurements: Optional[List[Optional[MeasurementDetail]]] = Field(
        validation_alias="measurements",
        default=None,
        description="All measurements available for this company",
    )

    operatorSets: Optional[List[Optional[OperatorSet]]] = Field(
        validation_alias="operatorSets",
        default=None,
        description="All operator sets used across dimension fields",
    )

    metricFamilies: Optional[List[Optional[MetricFamilyDef]]] = Field(
        validation_alias="metricFamilies",
        default=None,
        description="All metric family definitions",
    )

    assetTags: Optional[List[Optional[AssetTag]]] = Field(
        validation_alias="assetTags",
        default=None,
        description="All asset tag definitions",
    )

    appProtocols: Optional[Dict[str, Any]] = Field(
        validation_alias="appProtocols",
        default=None,
        description="All AppProtocol definitions",
    )
