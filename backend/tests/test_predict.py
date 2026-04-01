from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_validation():
    # Invalid horizon
    response = client.post(
        "/api/v1/predict", json={"crop": "tomato", "mandi": "indore", "horizon_days": 100}
    )
    assert response.status_code == 422
