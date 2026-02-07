from fastapi.testclient import TestClient
from uuid import uuid4
from app.utils.security import create_access_token


class TestUserAPI:
    """Test user API endpoints"""

    def test_get_users_as_admin(self, client: TestClient, db_session):
        """Test getting all users as admin"""
        # Create an admin user
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate

        admin_data = {
            "username": "admin_user",
            "auth_type": "local",
            "authorizations": {"role": "admin"},
            "is_active": True
        }
        admin = UserCRUD.create_user(db_session, UserCreate(**admin_data))

        # Create a regular user
        user_data = {
            "username": "test_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate admin token
        token = create_access_token(data={"sub": str(admin.id)})

        # Get all users
        response = client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        users = response.json()
        assert len(users) >= 2

    def test_get_users_without_admin_fails(self, client: TestClient, db_session):
        """Test getting all users without admin role fails"""
        # Create a regular user
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate

        user_data = {
            "username": "regular_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate token
        token = create_access_token(data={"sub": str(user.id)})

        # Try to get all users
        response = client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403

    def test_get_user_by_id(self, client: TestClient, db_session):
        """Test getting a specific user by ID"""
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate

        user_data = {
            "username": "target_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate token
        token = create_access_token(data={"sub": str(user.id)})

        # Get user by ID
        response = client.get(
            f"/api/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["username"] == user.username

    def test_update_user(self, client: TestClient, db_session):
        """Test updating a user"""
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate, UserUpdate

        user_data = {
            "username": "update_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate token
        token = create_access_token(data={"sub": str(user.id)})

        # Update user
        update_data = {
            "username": "updated_username",
            "authorizations": {"role": "admin"}
        }
        response = client.put(
            f"/api/users/{user.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["username"] == "updated_username"

    def test_delete_user(self, client: TestClient, db_session):
        """Test deleting (deactivating) a user"""
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate

        user_data = {
            "username": "delete_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate token
        token = create_access_token(data={"sub": str(user.id)})

        # Delete user
        response = client.delete(
            f"/api/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == {"message": "User deactivated successfully"}

    def test_get_user_not_found(self, client: TestClient, db_session):
        """Test getting non-existent user"""
        from app.crud.user import UserCRUD
        from app.schemas.user import UserCreate

        user_data = {
            "username": "auth_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        # Generate token
        token = create_access_token(data={"sub": str(user.id)})

        # Try to get non-existent user
        fake_id = uuid4()
        response = client.get(
            f"/api/users/{fake_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404