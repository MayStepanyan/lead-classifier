from __future__ import annotations

from fastapi import APIRouter

from app.schemas.lead_created_v1 import LeadCreatedV1
from app.schemas.lead_intent_v1 import LeadIntentV1

router = APIRouter(tags=["classification"])


@router.post("/classify", response_model=LeadIntentV1, summary="Classify a single lead")
def classify_lead(lead: LeadCreatedV1) -> LeadIntentV1:
    """Stub handler that returns a placeholder classification response."""
    # Return a deterministic stub payload that conforms to the response schema.
    return LeadIntentV1.model_validate(LeadIntentV1.example())
