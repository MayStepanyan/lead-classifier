from collections.abc import Sequence

from fastapi import APIRouter

from app.schemas.lead_created_v1 import LeadCreatedV1
from app.schemas.lead_intent_v1 import LeadIntentV1

router = APIRouter(tags=["classification"])


@router.post(
    "/batch",
    response_model=list[LeadIntentV1],
    summary="Classify a batch of leads",
)
def classify_batch(leads: Sequence[LeadCreatedV1]) -> list[LeadIntentV1]:
    """Stub handler that returns placeholder classification responses for each lead."""
    return [LeadIntentV1(intent="unknown", confidence=0.0, reasons=[]) for _ in leads]
