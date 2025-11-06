from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

LeadIntentClass = Literal["HOT", "WARM", "COLD", "SPAM"]


class LeadIntentReason(BaseModel):
    """Explainability information for an intent decision."""

    model_config = ConfigDict(str_strip_whitespace=True)

    top_features: list[str] = Field(default_factory=list, description="Top contributing n-grams")
    rules_fired: list[str] = Field(default_factory=list, description="Rule identifiers that matched")

    @field_validator("top_features", "rules_fired", mode="before")
    @classmethod
    def _default_to_list(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return []
        return value

    @field_validator("top_features", "rules_fired")
    @classmethod
    def _normalize_entries(cls, value: list[str]) -> list[str]:
        normalized: list[str] = []
        for entry in value:
            if not isinstance(entry, str):
                raise TypeError("reason values must be strings")
            stripped = entry.strip()
            if stripped:
                normalized.append(stripped)
        return normalized


class LeadIntentTierThresholds(BaseModel):
    """Score thresholds that delineate tier boundaries."""

    hot: float = Field(..., ge=0.0, le=1.0, description="Score threshold for HOT leads")
    warm: float = Field(..., ge=0.0, le=1.0, description="Score threshold for WARM leads")

    @model_validator(mode="after")
    def _ensure_hot_not_lower_than_warm(self) -> "LeadIntentTierThresholds":
        if self.hot < self.warm:
            raise ValueError("hot threshold must be >= warm threshold")
        return self


class LeadIntentModelMetadata(BaseModel):
    """Version metadata for the predictive model."""

    model_config = ConfigDict(str_strip_whitespace=True)

    version: str = Field(..., description="Semantic version of the classifier model")
    updated_at: datetime = Field(..., description="Timestamp when the model artifacts were updated")

    @field_validator("version")
    @classmethod
    def _ensure_version_non_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("version must not be empty")
        return value

    @field_validator("updated_at", mode="before")
    @classmethod
    def _clean_updated_at(cls, value: datetime | str) -> datetime | str:
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("updated_at")
    @classmethod
    def _ensure_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value


class LeadIntentV1(BaseModel):
    """Schema representing the inferred intent of a lead."""

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    classification: LeadIntentClass = Field(
        ..., alias="class", description="Tiered classification assigned to the lead"
    )
    score: float = Field(..., ge=0.0, le=1.0, description="Model score between 0 and 1")
    labels: list[str] = Field(default_factory=list, description="Optional labels attached to the lead")
    reason: LeadIntentReason = Field(
        default_factory=LeadIntentReason, description="Explainability signals for the prediction"
    )
    tier_thresholds: LeadIntentTierThresholds = Field(
        ..., description="Score thresholds for each tier"
    )
    model: LeadIntentModelMetadata = Field(
        ..., description="Metadata about the model that produced the prediction"
    )

    _allowed_classes: ClassVar[set[str]] = {"HOT", "WARM", "COLD", "SPAM"}

    @field_validator("classification", mode="before")
    @classmethod
    def _normalize_class(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("class must be provided as a string")
        normalized = value.strip().upper()
        if normalized not in cls._allowed_classes:
            raise ValueError("class must be one of HOT, WARM, COLD, SPAM")
        return normalized

    @field_validator("labels", mode="before")
    @classmethod
    def _default_labels(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return []
        return value

    @field_validator("labels")
    @classmethod
    def _normalize_labels(cls, value: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for label in value:
            if not isinstance(label, str):
                raise TypeError("labels must be strings")
            stripped = label.strip()
            if not stripped:
                continue
            key = stripped.lower()
            if key not in seen:
                seen.add(key)
                normalized.append(stripped)
        return normalized

    @classmethod
    def example(cls) -> dict[str, object]:
        now = datetime.now(timezone.utc)
        return {
            "class": "COLD",
            "score": 0.42,
            "labels": ["follow-up"],
            "reason": {
                "top_features": ["pricing", "enterprise"],
                "rules_fired": ["keyword:pricing"],
            },
            "tier_thresholds": {"hot": 0.8, "warm": 0.6},
            "model": {"version": "1.0.0", "updated_at": now.isoformat()},
        }


__all__ = [
    "LeadIntentV1",
    "LeadIntentReason",
    "LeadIntentTierThresholds",
    "LeadIntentModelMetadata",
    "LeadIntentClass",
]
