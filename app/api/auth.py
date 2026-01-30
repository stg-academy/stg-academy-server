from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import httpx
import uuid
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from ..crud.user import UserCRUD
from ..utils.security import create_access_token, verify_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.get("/kakao")
async def kakao_login():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"response_type=code&"
        f"client_id={settings.kakao_client_id}&"
        f"redirect_uri={settings.kakao_redirect_uri}"
    )
    return {"auth_url": kakao_auth_url}

@router.get("/kakao/callback")
async def kakao_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": settings.kakao_client_id,
                "client_secret": settings.kakao_client_secret,
                "code": code,
                "redirect_uri": settings.kakao_redirect_uri,
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        user_response = await client.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")

        user_data = user_response.json()
        kakao_id = str(user_data["id"])
        nickname = user_data["kakao_account"]["profile"]["nickname"]

        existing_user = UserCRUD.get_user_by_kakao_id(db, kakao_id)

        if existing_user:
            existing_user.last_login = datetime.utcnow()
            db.commit()
            user = existing_user
        else:
            user_create = UserCreate(
                username=nickname,
                auth_type="kakao",
                kakao_id=kakao_id,
                authorizations={"role": "user"}
            )
            user = UserCRUD.create_user(db, user_create)

        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}

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

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user