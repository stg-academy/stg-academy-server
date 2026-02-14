from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    auth_type: str
    information: Optional[str] = None
    authorizations: Optional[Dict[str, Any]] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: Optional[str] = None
    kakao_id: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    information: Optional[str] = None
    authorizations: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class KakaoLoginRequest(BaseModel):
    code: str

class KakaoLoginResponse(BaseModel):
    token: str
    user: Dict[str, Any]
    requires_registration: bool

class GeneralLoginRequest(BaseModel):
    username: str
    password: str

class GeneralLoginResponse(BaseModel):
    token: str
    user: Dict[str, Any]

class GeneralRegisterRequest(BaseModel):
    username: str
    password: str
    display_name: str
    information: str

class GeneralRegisterResponse(BaseModel):
    token: str
    user: Dict[str, Any]

class KakaoRegisterRequest(BaseModel):
    username: str
    information: str

class KakaoRegisterResponse(BaseModel):
    token: str
    user: Dict[str, Any]

class UsernameCheckResponse(BaseModel):
    available: bool
    message: str

class UserInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    auth_type: str
    information: Optional[str] = None
    is_active: bool