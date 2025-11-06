from datetime import datetime

from fastapi.testclient import TestClient

from app.schemas.lead_created_v1 import LeadCreatedV1
from app.schemas.lead_intent_v1 import LeadIntentV1


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    # timestamp should be parseable ISO format
    datetime.fromisoformat(payload["timestamp"])


def test_classify_endpoint_returns_stubbed_intent(client: TestClient) -> None:
    payload = LeadCreatedV1.example()

    response = client.post("/classify", json=payload)

    assert response.status_code == 200
    body = response.json()
    # Validate schema shape against Pydantic model to ensure compatibility
    LeadIntentV1.model_validate(body)
    assert body["class"] == "COLD"
    assert body["score"] == 0.42
    assert body["tier_thresholds"]["hot"] == 0.8
    assert body["tier_thresholds"]["warm"] == 0.6


def test_metrics_endpoint_exposes_process_metrics(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    text = response.text
    # Default process collector metrics should be present
    assert "process_cpu_seconds_total" in text
    assert "python_info" in text
