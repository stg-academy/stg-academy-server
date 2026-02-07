import json
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from app.crud import UserCRUD
from app.database import get_db
from app.models import User
from app.utils.security import verify_token

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserCRUD.get_user(db, UUID(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_user_role(user: User) -> str:
    """사용자의 역할을 추출"""
    if user.authorizations:
        auth_data = user.authorizations if isinstance(user.authorizations, dict) else json.loads(user.authorizations)
        return auth_data.get("role", "user")
    return "user"


def check_user_role(required_roles: List[str]):
    """
    특정 역할을 가진 사용자만 접근 가능하도록 검증하는 dependency

    Args:
        required_roles: 허용할 역할 리스트 (예: ["admin"] 또는 ["admin", "user"])
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = get_user_role(current_user)

        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"접근 권한이 없습니다. 필요한 권한: {', '.join(required_roles)}"
            )

        return current_user

    return role_checker


# 편의를 위한 미리 정의된 dependency들
require_admin = check_user_role(["admin"])
require_user_or_admin = check_user_role(["user", "admin"])
