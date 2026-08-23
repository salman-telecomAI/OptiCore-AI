"""
Data contracts for OptiCore AI.

Field names copied verbatim from LLD Section 6 (Data Contracts Between
Components) - do not rename during build. Any change to these fields
is an architecture decision, not a coding one, and belongs back in the
Blueprint/LLD docs first, per Blueprint v2.0 Section 1.
"""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel

Ring = Literal["Ring 1", "Ring 2", "Ring 3"]
Vendor = Literal["Huawei", "Ciena", "Nokia"]
AffectedLayer = Literal["Physical", "OTN", "SDH", "Ethernet"]
TwinLayer = Literal[0, 1, 2, 3]
Recommendation = Literal["Auto-proceed", "Escalate to human"]


class NormalisedAlarmObject(BaseModel):
    # LLD 6.1
    incident_id: str
    source_ring: Ring
    source_vendor: Vendor
    native_alarm_ref: str
    severity_normalised: Literal["Critical", "Major", "Minor", "Warning"]
    affected_layer: AffectedLayer
    timestamp: datetime


class SimulationResultObject(BaseModel):
    # LLD 6.2
    proposed_action: str
    confidence_score: int  # 0-100
    blast_radius: str
    layers_validated: list[TwinLayer]
    cross_domain: bool
    recommendation: Recommendation
