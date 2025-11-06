from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.schemas.lead_intent_v1 import LeadIntentV1


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    # timestamp should be parseable ISO format
    datetime.fromisoformat(payload["timestamp"])


def test_classify_endpoint_returns_stubbed_intent(client: TestClient) -> None:
    payload = {
        "lead_id": "123",
        "email": "lead@example.com",
        "full_name": "Lead Example",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "web",
        "metadata": {"campaign": "spring"},
    }

    response = client.post("/classify", json=payload)

    assert response.status_code == 200
    body = response.json()
    # Validate schema shape against Pydantic model to ensure compatibility
    LeadIntentV1.model_validate(body)
    assert body["intent"] == "unknown"
    assert body["confidence"] == 0.0
    assert body["reasons"] == []


def test_metrics_endpoint_exposes_process_metrics(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    text = response.text
    # Default process collector metrics should be present
    assert "process_cpu_seconds_total" in text
    assert "python_info" in text
