from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    auth_type: str
    authorizations: Optional[Dict[str, Any]] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: Optional[str] = None
    kakao_id: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    authorizations: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    keyword: Optional[str] = None
    is_active: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    keyword: Optional[str] = None
    is_active: Optional[bool] = None
    updated_by: str

class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

class ClassBase(BaseModel):
    title: str
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    title: Optional[str] = None
    lecturer_info: Optional[str] = None
    date_info: Optional[str] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    updated_by: str

class ClassResponse(ClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

class LectureBase(BaseModel):
    title: str
    sequence: int
    attendance_type: Optional[str] = None
    lecture_date: Optional[datetime] = None

class LectureCreate(LectureBase):
    pass

class LectureUpdate(BaseModel):
    title: Optional[str] = None
    sequence: Optional[int] = None
    attendance_type: Optional[str] = None
    lecture_date: Optional[datetime] = None
    updated_by: str

class LectureResponse(LectureBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    class_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

class AttendanceBase(BaseModel):
    status: str
    detail_type: Optional[str] = None
    description: Optional[str] = None
    assignment_id: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    user_id: UUID

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    detail_type: Optional[str] = None
    description: Optional[str] = None
    assignment_id: Optional[str] = None
    updated_by: str

class AttendanceResponse(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lecture_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

class CertificationBase(BaseModel):
    class_ids: Optional[List[str]] = None

class CertificationCreate(CertificationBase):
    course_id: UUID
    user_id: UUID
    issued_at: datetime

class CertificationUpdate(BaseModel):
    class_ids: Optional[List[str]] = None
    updated_by: str

class CertificationResponse(CertificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    user_id: UUID
    issued_at: datetime
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str