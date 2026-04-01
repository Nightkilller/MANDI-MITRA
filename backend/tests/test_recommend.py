from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_recommend_validation():
    response = client.post(
        "/api/v1/recommend",
        json={
            "crop": "tomato",
            "mandi": "indore",
            "quantity_quintals": 10.5,
            # Missing basic fields validation
        },
    )
    assert response.status_code == 422
