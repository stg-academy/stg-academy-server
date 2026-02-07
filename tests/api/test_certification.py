from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token
from app.crud.user import UserCRUD
from app.crud.course import CourseCRUD
from app.crud.session import SessionCRUD
from app.crud.certification import CertificationCRUD
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate
from app.schemas.session import SessionCreate
from app.schemas.certification import CertificationCreate


class TestCertificationAPI:
    """Test certification API endpoints"""

    def test_create_certification(self, client: TestClient, db_session):
        """Test creating a new certification"""
        user_data = {
            "username": "cert_creator",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Test Course",
            "description": "A test course",
            "keyword": "test",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        certification_data = {
            "course_id": str(course.id),
            "user_id": str(user.id),
            "session_ids": [str(session.id)],
            "issued_at": datetime.utcnow().isoformat()
        }
        response = client.post(
            "/api/certifications",
            json=certification_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["course_id"] == str(course.id)
        assert data["user_id"] == str(user.id)

    def test_get_certifications(self, client: TestClient, db_session):
        """Test getting all certifications"""
        user_data = {
            "username": "cert_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Certifications",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        certification_data = {
            "course_id": str(course.id),
            "user_id": str(user.id),
            "session_ids": [str(session.id)],
            "issued_at": datetime.utcnow().isoformat()
        }
        CertificationCRUD.create_certification(db_session, CertificationCreate(**certification_data), user)

        response = client.get("/api/certifications")

        assert response.status_code == 200
        certifications = response.json()
        assert len(certifications) >= 1

    def test_get_certifications_by_user(self, client: TestClient, db_session):
        """Test getting certifications for a specific user"""
        user_data = {
            "username": "cert_by_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for User Certifications",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        certification_data = {
            "course_id": str(course.id),
            "user_id": str(user.id),
            "session_ids": [str(session.id)],
            "issued_at": datetime.utcnow().isoformat()
        }
        CertificationCRUD.create_certification(db_session, CertificationCreate(**certification_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        response = client.get(
            f"/api/certifications/user/{user.id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        certifications = response.json()
        assert len(certifications) >= 1
        assert certifications[0]["user_id"] == str(user.id)

    def test_get_certification_by_id(self, client: TestClient, db_session):
        """Test getting a specific certification by ID"""
        user_data = {
            "username": "cert_finder",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Course for Certification",
            "description": "Course",
            "keyword": "course",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        session_data = {
            "course_id": str(course.id),
            "title": "Test Session",
            "lecturer_info": "Instructor",
            "date_info": "2024-01"
        }
        session = SessionCRUD.create_session(db_session, SessionCreate(**session_data), user)

        certification_data = {
            "course_id": str(course.id),
            "user_id": str(user.id),
            "session_ids": [str(session.id)],
            "issued_at": datetime.utcnow().isoformat()
        }
        certification = CertificationCRUD.create_certification(db_session, CertificationCreate(**certification_data), user)

        response = client.get(f"/api/certifications/{certification.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["course_id"] == str(course.id)

    def test_get_certification_not_found(self, client: TestClient):
        """Test getting non-existent certification"""
        fake_id = uuid4()
        response = client.get(f"/api/certifications/{fake_id}")
        assert response.status_code == 404