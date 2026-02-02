from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

# SQLite 호환 테스트 모델들
class TestUser(Base):
    __tablename__ = "test_users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False, unique=True)
    auth_type = Column(String, nullable=False)
    password = Column(String)
    kakao_id = Column(String)
    authorizations = Column(JSON)  # SQLite에서 JSON 사용
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, nullable=False, default=True)

    attendances = relationship("TestAttendance", back_populates="user")
    certifications = relationship("TestCertification", back_populates="user")

class TestCourse(Base):
    __tablename__ = "test_courses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    keyword = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    sessions = relationship("TestSession", back_populates="course")
    certifications = relationship("TestCertification", back_populates="course")

class TestSession(Base):
    __tablename__ = "test_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("test_courses.id"), nullable=False)
    title = Column(String, nullable=False)
    lecturer_info = Column(String)
    date_info = Column(String)
    begin_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    course = relationship("TestCourse", back_populates="sessions")
    lectures = relationship("TestLecture", back_populates="session")

class TestLecture(Base):
    __tablename__ = "test_lectures"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("test_sessions.id"), nullable=False)
    title = Column(String, nullable=False)
    sequence = Column(Integer, nullable=False)
    attendance_type = Column(String)
    lecture_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)

    session = relationship("TestSession", back_populates="lectures")
    attendances = relationship("TestAttendance", back_populates="lecture")

class TestAttendance(Base):
    __tablename__ = "test_attendances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lecture_id = Column(String, ForeignKey("test_lectures.id"), nullable=False)
    user_id = Column(String, ForeignKey("test_users.id"), nullable=False)
    status = Column(String, nullable=False)
    detail_type = Column(String)
    description = Column(Text)
    assignment_id = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)

    lecture = relationship("TestLecture", back_populates="attendances")
    user = relationship("TestUser", back_populates="attendances")

class TestCertification(Base):
    __tablename__ = "test_certifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("test_courses.id"), nullable=False)
    user_id = Column(String, ForeignKey("test_users.id"), nullable=False)
    session_ids = Column(JSON)  # SQLite에서 JSON 사용
    issued_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)

    course = relationship("TestCourse", back_populates="certifications")
    user = relationship("TestUser", back_populates="certifications")