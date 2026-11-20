# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BitwiseOp import BitwiseOp
from .TCPFlag import TCPFlag


class TCPFlagsPredicate(BaseModel):
    """
    TCPFlagsPredicate model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    operator: Optional[BitwiseOp] = Field(validation_alias="operator", default=None)

    values: Optional[List[Optional[TCPFlag]]] = Field(
        validation_alias="values", default=None
    )
