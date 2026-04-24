import pytest
from fastapi.testclient import TestClient
from api.main import app
from db.models import User
from core.database import SessionLocal

client = TestClient(app)

import time

def test_register_user():
    email = f"test_{int(time.time())}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "testpassword123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == email

def test_register_duplicate_user():
    # Attempt to register the same user again
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test_auth@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test_auth@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test_auth@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_nonexistent_user():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nobody@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 401
