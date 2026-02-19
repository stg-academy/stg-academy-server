from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timedelta

from ..database import get_db
from ..models.user import User
from ..schemas.user import (
    UserCreate, UserResponse, KakaoLoginRequest, KakaoLoginResponse,
    GeneralLoginRequest, GeneralLoginResponse, GeneralRegisterRequest,
    GeneralRegisterResponse, KakaoRegisterRequest, KakaoRegisterResponse,
    UsernameCheckResponse, ManualRegisterRequest, ManualRegisterResponse
)
from ..crud.user import UserCRUD
from ..utils.auth import get_current_user, hash_password, verify_password, get_temp_user, require_admin
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
            # 기존 사용자 - 로그인 처리
            existing_user.last_login = datetime.utcnow()
            db.commit()

            jwt_token = create_access_token(data={"sub": str(existing_user.id)})

            return {
                "token": jwt_token,
                "user": {
                    "id": str(existing_user.id),
                    "username": existing_user.username,
                    "auth_type": existing_user.auth_type,
                    "information": existing_user.information
                },
                "requires_registration": False
            }
        else:
            # 신규 사용자 - 임시 토큰 생성
            temp_token = create_access_token(
                data={
                    "type": "temp",
                    "kakao_user": {
                        "kakao_id": kakao_id,
                        "nickname": nickname
                    }
                },
                expires_delta=timedelta(minutes=30)
            )

            return {
                "token": temp_token,
                "user": {
                    "kakao_id": kakao_id,
                    "nickname": nickname
                },
                "requires_registration": True
            }


@router.post("/login", response_model=GeneralLoginResponse)
async def general_login(request: GeneralLoginRequest, db: Session = Depends(get_db)):
    user = UserCRUD.get_user_by_username(db, request.username)

    if not user or user.auth_type != "normal" or not user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user.last_login = datetime.utcnow()
    db.commit()

    jwt_token = create_access_token(data={"sub": str(user.id)})

    return {
        "token": jwt_token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "auth_type": user.auth_type,
            "information": user.information
        }
    }


@router.post("/register", response_model=GeneralRegisterResponse)
async def general_register(request: GeneralRegisterRequest, db: Session = Depends(get_db)):
    # 사용자명 중복 확인
    existing_user = UserCRUD.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # 비밀번호 해시화
    hashed_password = hash_password(request.password)

    # 사용자 생성
    user_create = UserCreate(
        username=request.username,
        auth_type="normal",
        password=hashed_password,
        information=request.information,
        authorizations={"role": "user"}
    )

    user = UserCRUD.create_user(db, user_create)

    jwt_token = create_access_token(data={"sub": str(user.id)})

    return {
        "token": jwt_token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "auth_type": user.auth_type,
            "information": user.information
        }
    }


@router.post("/kakao/register", response_model=KakaoRegisterResponse)
async def kakao_register(request: KakaoRegisterRequest, kakao_user: dict = Depends(get_temp_user),
                         db: Session = Depends(get_db)):
    # 이미 등록된 카카오 사용자인지 확인
    existing_kakao_user = UserCRUD.get_user_by_kakao_id(db, kakao_user["kakao_id"])
    if existing_kakao_user:
        raise HTTPException(status_code=409, detail="Already registered Kakao user")

    # 사용자명 중복 확인
    existing_user = UserCRUD.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # 카카오 사용자 생성
    user_create = UserCreate(
        username=request.username,
        auth_type="kakao",
        kakao_id=kakao_user["kakao_id"],
        information=request.information,
        authorizations={"role": "user"}
    )

    user = UserCRUD.create_user(db, user_create)

    jwt_token = create_access_token(data={"sub": str(user.id)})

    return {
        "token": jwt_token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "auth_type": user.auth_type,
            "information": user.information
        }
    }


@router.get("/username", response_model=UsernameCheckResponse)
async def check_username(username: str = Query(...), db: Session = Depends(get_db)):
    existing_user = UserCRUD.get_user_by_username(db, username)

    if existing_user:
        return {
            "available": False,
            "message": "이미 사용 중인 아이디입니다"
        }
    else:
        return {
            "available": True,
            "message": "사용 가능한 아이디입니다"
        }


@router.post("/manual/register", response_model=ManualRegisterResponse)
async def manual_register(
        request: ManualRegisterRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin)
):
    # 사용자명 중복 확인
    existing_user = UserCRUD.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # 관리자가 직접 사용자 생성
    user_create = UserCreate(
        username=request.username,
        auth_type="manual",
        information=request.information,
        authorizations={"role": request.auth}
    )

    user = UserCRUD.create_user(db, user_create)

    return {
        "user": {
            "id": str(user.id),
            "username": user.username,
            "auth_type": user.auth_type,
            "information": user.information,
            "auth": request.auth,
            "created_at": user.created_at.isoformat()
        }
    }


@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
