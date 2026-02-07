from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from app.utils.security import create_access_token
from app.crud.user import UserCRUD
from app.crud.course import CourseCRUD
from app.schemas.user import UserCreate
from app.schemas.course import CourseCreate, CourseUpdate


class TestCourseAPI:
    """Test course API endpoints"""

    def test_create_course(self, client: TestClient, db_session):
        """Test creating a new course"""
        user_data = {
            "username": "course_creator",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        token = create_access_token(data={"sub": str(user.id)})

        course_data = {
            "title": "Test Course",
            "description": "A test course description",
            "keyword": "testing",
            "created_by": str(user.id),
            "is_active": True
        }
        response = client.post(
            "/api/courses",
            json=course_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Course"
        assert data["description"] == "A test course description"

    def test_get_courses(self, client: TestClient, db_session):
        """Test getting all courses"""
        user_data = {
            "username": "course_user",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Test Course 1",
            "description": "First test course",
            "keyword": "test",
            "created_by": str(user.id),
            "is_active": True
        }
        CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        response = client.get("/api/courses")

        assert response.status_code == 200
        courses = response.json()
        assert len(courses) >= 1

    def test_get_course_by_id(self, client: TestClient, db_session):
        """Test getting a specific course by ID"""
        user_data = {
            "username": "course_finder",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Specific Course",
            "description": "A specific course",
            "keyword": "specific",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        response = client.get(f"/api/courses/{course.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Specific Course"

    def test_update_course(self, client: TestClient, db_session):
        """Test updating a course"""
        user_data = {
            "username": "course_updater",
            "auth_type": "local",
            "authorizations": {"role": "user"},
            "is_active": True
        }
        user = UserCRUD.create_user(db_session, UserCreate(**user_data))

        course_data = {
            "title": "Original Title",
            "description": "Original description",
            "keyword": "original",
            "created_by": str(user.id),
            "is_active": True
        }
        course = CourseCRUD.create_course(db_session, CourseCreate(**course_data), user)

        token = create_access_token(data={"sub": str(user.id)})

        update_data = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        response = client.put(
            f"/api/courses/{course.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"

    def test_get_course_not_found(self, client: TestClient):
        """Test getting non-existent course"""
        fake_id = uuid4()
        response = client.get(f"/api/courses/{fake_id}")
        assert response.status_code == 404