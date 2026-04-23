from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "is running" in response.json()["message"]

def test_predict_mental_health():
    response = client.post(
        "/api/v1/predict/",
        json={"text": "I feel very lonely and sad"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk" in data
    assert "score" in data
    assert "keywords" in data
    assert "response" in data

def test_predict_mental_health_empty():
    response = client.post(
        "/api/v1/predict/",
        json={"text": ""}
    )
    assert response.status_code == 422
