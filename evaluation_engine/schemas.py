from pydantic import BaseModel, Field
from typing import List, Optional

class PatientSimulationConfig(BaseModel):
    condition: str
    severity: str
    demographics: dict

class ConversationTurn(BaseModel):
    role: str
    content: str

class ClinicalAuditResult(BaseModel):
    passed_safety_gate: bool
    hallucination_index: float = Field(..., ge=0.0, le=1.0)
    critical_red_flags_identified: List[str]
    detected_medical_errors: List[str]
    severity_assessment_accuracy: str
    justification_summary: str
