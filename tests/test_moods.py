import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture
def auth_header():
    # Register and login to get a valid token
    email = "mood_test@example.com"
    password = "testpassword123"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_mood_history_authenticated(auth_header):
    response = client.get("/api/v1/moods/", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_mood_history_unauthorized():
    response = client.get("/api/v1/moods/")
    # Should fail because no token provided
    assert response.status_code == 401
