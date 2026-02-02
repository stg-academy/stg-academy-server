import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.models.user import User
from app.crud.user import UserCRUD
from app.utils.security import create_access_token


class TestKakaoAuth:
    def test_get_kakao_login_url(self, client: TestClient):
        response = client.get("/auth/kakao")

        assert response.status_code == 200
        data = response.json()
        assert "auth_url" in data
        assert "https://kauth.kakao.com/oauth/authorize" in data["auth_url"]
        assert "client_id=" in data["auth_url"]
        assert "redirect_uri=" in data["auth_url"]

    @patch('httpx.AsyncClient')
    def test_kakao_callback_new_user(self, mock_client, client: TestClient, db_session):
        # Mock Kakao API responses
        mock_token_response = AsyncMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "test_token"}

        mock_user_response = AsyncMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "id": 12345,
            "kakao_account": {
                "profile": {
                    "nickname": "Test User"
                }
            }
        }

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_token_response
        mock_client_instance.get.return_value = mock_user_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        response = client.get("/auth/kakao/login?code=test_code")

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "Test User"
        assert data["user"]["auth_type"] == "kakao"

    @patch('httpx.AsyncClient')
    def test_kakao_callback_existing_user(self, mock_client, client: TestClient, db_session):
        # Create existing user
        existing_user = User(
            username="Existing User",
            auth_type="kakao",
            kakao_id="12345",
            authorizations={"role": "user"},
            is_active=True
        )
        db_session.add(existing_user)
        db_session.commit()
        db_session.refresh(existing_user)

        # Mock Kakao API responses
        mock_token_response = AsyncMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {"access_token": "test_token"}

        mock_user_response = AsyncMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "id": 12345,
            "kakao_account": {
                "profile": {
                    "nickname": "Existing User"
                }
            }
        }

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_token_response
        mock_client_instance.get.return_value = mock_user_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        response = client.get("/auth/kakao/login?code=test_code")

        assert response.status_code == 200
        data = response.json()
        assert data["user"]["username"] == "Existing User"

    @patch('httpx.AsyncClient')
    def test_kakao_callback_token_error(self, mock_client, client: TestClient):
        mock_token_response = AsyncMock()
        mock_token_response.status_code = 400

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_token_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        response = client.get("/auth/kakao/login?code=test_code")

        assert response.status_code == 400
        assert "Failed to get access token" in response.json()["detail"]


class TestJWTAuth:
    def test_get_current_user_info_valid_token(self, client: TestClient, db_session):
        # Create test user
        user = User(
            username="Test User",
            auth_type="kakao",
            kakao_id="12345",
            authorizations={"role": "user"},
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Create valid token
        token = create_access_token(data={"sub": str(user.id)})

        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "Test User"
        assert data["auth_type"] == "kakao"

    def test_get_current_user_info_invalid_token(self, client: TestClient):
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401
        assert "Invalid token" in response.json()["detail"]

    def test_get_current_user_info_no_token(self, client: TestClient):
        response = client.get("/auth/me")

        assert response.status_code == 403

    def test_logout(self, client: TestClient):
        response = client.post("/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"