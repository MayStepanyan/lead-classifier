from fastapi import APIRouter

from app.schemas.lead_created_v1 import LeadCreatedV1
from app.schemas.lead_intent_v1 import LeadIntentV1

router = APIRouter(tags=["classification"])


@router.post("/classify", response_model=LeadIntentV1, summary="Classify a single lead")
def classify_lead(lead: LeadCreatedV1) -> LeadIntentV1:
    """Stub handler that returns a placeholder classification response."""
    return LeadIntentV1(intent="unknown", confidence=0.0, reasons=[])
