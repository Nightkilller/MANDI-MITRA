from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_explain_validation():
    response = client.post(
        "/api/v1/explain", json={"crop": "onion"}  # Missing mandi
    )
    assert response.status_code == 422
