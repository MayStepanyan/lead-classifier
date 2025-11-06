from typing import Any

from pydantic import BaseModel, Field


class LeadIntentExplanation(BaseModel):
    """Explainability information for an intent decision."""

    feature: str = Field(..., description="Feature contributing to the prediction")
    weight: float = Field(..., description="Relative contribution of the feature")


class LeadIntentV1(BaseModel):
    """Schema representing the inferred intent of a lead."""

    lead_id: str | None = Field(None, description="Identifier of the evaluated lead")
    intent: str = Field(..., description="Predicted intent label for the lead")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score associated with the prediction",
    )
    reasons: list[LeadIntentExplanation] = Field(
        default_factory=list,
        description="Optional feature attributions that justify the prediction",
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Additional metadata about the prediction",
    )


__all__ = ["LeadIntentV1", "LeadIntentExplanation"]
