from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LeadCreatedV1(BaseModel):
    """Schema representing an inbound lead creation event."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., description="Full name provided by the lead")
    email: EmailStr = Field(..., description="Validated email address for the lead")
    phone: str = Field(..., description="Normalized E.164-like phone number for the lead")
    message: str = Field(..., description="Free form message captured with the lead")
    source: str | None = Field(
        default=None,
        description="Originating source for the lead (e.g. landing page or campaign)",
    )
    timestamp: datetime | None = Field(
        default=None,
        description="UTC timestamp when the lead was captured",
    )

    _phone_allowed_pattern: ClassVar[re.Pattern[str]] = re.compile(r"[^0-9+]")

    @field_validator("name", "message", "source", mode="before")
    @classmethod
    def _strip_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
        return value

    @field_validator("name", "message")
    @classmethod
    def _ensure_non_empty(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("must not be empty")
        return value

    @field_validator("source")
    @classmethod
    def _empty_source_to_none(cls, value: str | None) -> str | None:
        if value == "":
            return None
        return value

    @field_validator("phone", mode="before")
    @classmethod
    def _normalize_phone(cls, value: str | int | float) -> str:
        if isinstance(value, (int, float)):
            value = str(int(value))
        if not isinstance(value, str):
            raise TypeError("phone must be a string")
        digits = cls._phone_allowed_pattern.sub("", value)
        if digits.startswith("+"):
            prefix = "+"
            digit_part = re.sub(r"\D", "", digits[1:])
        else:
            prefix = ""
            digit_part = re.sub(r"\D", "", digits)
        if not digit_part.isdigit():
            raise ValueError("phone must contain digits")
        if not 7 <= len(digit_part) <= 15:
            raise ValueError("phone must be between 7 and 15 digits")
        return f"{prefix}{digit_part}" if prefix else digit_part

    @field_validator("timestamp", mode="before")
    @classmethod
    def _clean_timestamp(cls, value: datetime | str | None) -> datetime | str | None:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value

    @field_validator("timestamp")
    @classmethod
    def _ensure_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value

    @classmethod
    def example(cls) -> dict[str, object]:
        now = datetime.now(timezone.utc)
        return {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+15551234567",
            "message": "Looking for enterprise pricing details.",
            "source": "marketing-site",
            "timestamp": now.isoformat(),
        }


__all__ = ["LeadCreatedV1"]
