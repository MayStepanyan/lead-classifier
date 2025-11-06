from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client for API integration tests."""
    with TestClient(app) as test_client:
        yield test_client
