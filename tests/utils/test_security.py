import pytest
from datetime import datetime, timedelta

from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)


class TestPasswordHashing:
    def test_password_hashing(self):
        password = "test_password"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_password_hash_uniqueness(self):
        password = "test_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Each hash should be unique due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    def test_create_and_verify_token(self):
        data = {"sub": "test_user_id", "role": "user"}
        token = create_access_token(data=data)

        assert token is not None
        assert isinstance(token, str)

        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test_user_id"
        assert payload["role"] == "user"
        assert "exp" in payload

    def test_token_with_custom_expiry(self):
        data = {"sub": "test_user_id"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data=data, expires_delta=expires_delta)

        payload = verify_token(token)
        assert payload is not None

        # Check that expiry is set correctly (within 1 second tolerance)
        expected_exp = datetime.utcnow() + expires_delta
        actual_exp = datetime.utcfromtimestamp(payload["exp"])
        time_diff = abs((expected_exp - actual_exp).total_seconds())
        assert time_diff < 1

    def test_invalid_token(self):
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)

        assert payload is None

    def test_expired_token(self):
        data = {"sub": "test_user_id"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data=data, expires_delta=expires_delta)

        payload = verify_token(token)
        assert payload is None

    def test_malformed_token(self):
        malformed_tokens = [
            "",
            "not.a.token",
            "header.payload",  # Missing signature
            "too.many.parts.in.this.token"
        ]

        for token in malformed_tokens:
            payload = verify_token(token)
            assert payload is None