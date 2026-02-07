import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token


def test_kakao_login_redirect(client: TestClient):
    """Test Kakao login redirect endpoint"""
    response = client.get("/auth/kakao")
    # Kakao config might be missing, so we accept 404 if not configured
    if response.status_code == 404:
        pytest.skip("Kakao client ID not configured")
    assert response.status_code == 302
    assert "kauth.kakao.com" in response.headers.get("location", "")


def test_kakao_login_with_mock_code(client: TestClient, db_session):
    """Test Kakao login with mock authorization code"""
    response = client.post("/auth/kakao/login", json={"code": "test_code"})
    assert response.status_code in [400, 404]


def test_logout(client: TestClient):
    """Test logout endpoint"""
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}


def test_get_current_user_info_no_auth(client: TestClient):
    """Test getting current user info without authentication"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_current_user_info_with_auth(client: TestClient, db_session, test_user_data):
    """Test getting current user info with valid authentication"""
    from app.crud.user import UserCRUD
    from app.schemas.user import UserCreate

    user_create = UserCreate(**test_user_data)
    user = UserCRUD.create_user(db_session, user_create)

    token = create_access_token(data={"sub": str(user.id)})

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == test_user_data["username"]
    assert response.json()["id"] == str(user.id)