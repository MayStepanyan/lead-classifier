from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class LeadCreatedV1(BaseModel):
    """Schema representing a newly created lead."""

    lead_id: str = Field(..., description="Unique identifier for the lead")
    email: EmailStr = Field(..., description="Primary email address of the lead")
    full_name: str | None = Field(None, description="Full name of the lead, if known")
    created_at: datetime = Field(..., description="Timestamp when the lead was created")
    source: str | None = Field(None, description="Source system that generated the lead")
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Arbitrary metadata captured at lead creation time",
    )


__all__ = ["LeadCreatedV1"]
