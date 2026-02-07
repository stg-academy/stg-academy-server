from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import httpx
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, KakaoLoginRequest, KakaoLoginResponse
from ..crud.user import UserCRUD
from ..utils.auth import get_current_user
from ..utils.security import create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/kakao")
async def kakao_login():
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"response_type=code&"
        f"client_id={settings.kakao_client_id}&"
        f"redirect_uri={settings.kakao_redirect_uri}"
    )
    return RedirectResponse(url=kakao_auth_url, status_code=302)


@router.post("/kakao/login", response_model=KakaoLoginResponse)
async def kakao_login(request: KakaoLoginRequest, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": settings.kakao_client_id,
                "client_secret": settings.kakao_client_secret,
                "code": request.code,
                # "redirect_uri": settings.kakao_redirect_uri,
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
            "token": access_token,
            "user": {
                "id": str(user.id),
                "nickname": user.username,
                "email": None  # 카카오에서 이메일을 제공하지 않는 경우
            }
        }


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
