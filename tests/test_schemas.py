from __future__ import annotations

from datetime import timezone

import pytest
from pydantic import ValidationError

from app.schemas.lead_created_v1 import LeadCreatedV1
from app.schemas.lead_intent_v1 import LeadIntentV1


@pytest.mark.parametrize(
    ("field", "value", "error_message"),
    [
        ("name", "   ", "must not be empty"),
        ("message", "", "must not be empty"),
        ("email", "not-an-email", "value is not a valid email address"),
        ("phone", "12", "phone must be between 7 and 15 digits"),
    ],
)
def test_lead_created_v1_invalid_inputs(field: str, value: object, error_message: str) -> None:
    payload = LeadCreatedV1.example()
    payload[field] = value  # type: ignore[index]

    with pytest.raises(ValidationError) as exc:
        LeadCreatedV1.model_validate(payload)

    assert error_message in str(exc.value)


@pytest.mark.parametrize(
    ("message", "is_valid"),
    [
        pytest.param("   ", False, id="empty-message"),
        pytest.param("こんにちは✨", True, id="unicode-message"),
    ],
)
def test_lead_created_v1_message_edge_cases(message: str, is_valid: bool) -> None:
    payload = LeadCreatedV1.example()
    payload["message"] = message

    if is_valid:
        model = LeadCreatedV1.model_validate(payload)
        assert model.message == message.strip()
    else:
        with pytest.raises(ValidationError):
            LeadCreatedV1.model_validate(payload)


def test_lead_created_v1_missing_optional_fields() -> None:
    payload = LeadCreatedV1.example()
    payload.pop("source", None)
    payload.pop("timestamp", None)

    model = LeadCreatedV1.model_validate(payload)

    assert model.source is None
    assert model.timestamp is None


def test_lead_created_v1_normalizes_phone_number() -> None:
    payload = LeadCreatedV1.example()
    payload["phone"] = " +1 (555) 123-4567 "

    model = LeadCreatedV1.model_validate(payload)

    assert model.phone == "+15551234567"


def test_lead_created_v1_timestamp_coerced_to_utc() -> None:
    payload = LeadCreatedV1.example()
    payload["timestamp"] = "2024-01-01T01:00:00-05:00"

    model = LeadCreatedV1.model_validate(payload)

    assert model.timestamp is not None
    assert model.timestamp.tzinfo == timezone.utc
    assert model.timestamp.isoformat() == "2024-01-01T06:00:00+00:00"


def test_lead_intent_v1_validates_alias_payload() -> None:
    payload = LeadIntentV1.example()

    model = LeadIntentV1.model_validate(payload)

    assert model.classification == "COLD"
    assert model.reason.top_features == ["pricing", "enterprise"]
    assert model.model.updated_at.tzinfo == timezone.utc


def test_lead_intent_v1_deduplicates_labels() -> None:
    payload = LeadIntentV1.example()
    payload["labels"] = [" Follow-Up ", "follow-up", "NEW"]

    model = LeadIntentV1.model_validate(payload)

    assert model.labels == ["Follow-Up", "NEW"]
