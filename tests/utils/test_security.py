from app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)


class TestSecurityUtils:
    """Test security utility functions"""

    def test_hash_and_verify_password(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        # Hash should be different from original
        assert hashed != password

        # Should verify correctly
        assert verify_password(password, hashed) is True

        # Wrong password should fail
        assert verify_password("wrong_password", hashed) is False

    def test_create_access_token(self):
        """Test JWT token creation"""
        payload = {"sub": "user_id_123", "role": "admin"}
        token = create_access_token(payload)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_success(self):
        """Test successful token verification"""
        payload = {"sub": "user_id_456", "role": "user"}
        token = create_access_token(payload)

        verified = verify_token(token)

        assert verified is not None
        assert verified["sub"] == "user_id_456"
        assert verified["role"] == "user"

    def test_verify_token_invalid(self):
        """Test invalid token verification"""
        invalid_token = "invalid_token_string"
        verified = verify_token(invalid_token)

        assert verified is None