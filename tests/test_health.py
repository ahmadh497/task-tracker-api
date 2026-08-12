"""
Tests for the /health endpoint using pytest and FastAPI's TestClient.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    """The /health endpoint should respond with HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_expected_shape():
    """The response body should contain 'status' and 'timestamp' keys."""
    response = client.get("/health")
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_health_timestamp_is_iso_format():
    """The timestamp should be parseable as an ISO 8601 datetime string."""
    from datetime import datetime

    response = client.get("/health")
    timestamp = response.json()["timestamp"]
    # Raises ValueError if not a valid ISO 8601 string
    datetime.fromisoformat(timestamp)