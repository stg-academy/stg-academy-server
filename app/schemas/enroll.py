from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class EnrollBase(BaseModel):
    user_id: UUID
    session_id: UUID
    enroll_status: Optional[str] = None

class EnrollCreate(EnrollBase):
    pass

class EnrollUpdate(BaseModel):
    enroll_status: Optional[str] = None

class EnrollResponse(EnrollBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID

class EnrollDetailResponse(EnrollBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_name: str
    auth_type: str
    session_title: str
    course_name: str
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID