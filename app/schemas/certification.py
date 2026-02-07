from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class CertificationBase(BaseModel):
    session_ids: Optional[List[str]] = None

class CertificationCreate(CertificationBase):
    course_id: UUID
    user_id: UUID
    issued_at: datetime

class CertificationUpdate(BaseModel):
    session_ids: Optional[List[str]] = None
    updated_by: UUID

class CertificationResponse(CertificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    user_id: UUID
    issued_at: datetime
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID