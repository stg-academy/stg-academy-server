import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.models.user import User, Course, Class, Lecture, Attendance, Certification
from app.utils.security import create_access_token


@pytest.fixture
def auth_headers(db_session):
    user = User(
        username="Test User",
        auth_type="test",
        authorizations={"role": "admin"},
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}, user


class TestUserCRUD:
    def test_get_users(self, client: TestClient, db_session, auth_headers):
        headers, _ = auth_headers

        # Create test users
        for i in range(3):
            user = User(
                username=f"User {i}",
                auth_type="test",
                authorizations={"role": "user"},
                is_active=True
            )
            db_session.add(user)
        db_session.commit()

        response = client.get("/api/users", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_get_user_by_id(self, client: TestClient, db_session, auth_headers):
        headers, auth_user = auth_headers

        response = client.get(f"/api/users/{auth_user.id}", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "Test User"

    def test_get_user_not_found(self, client: TestClient, auth_headers):
        headers, _ = auth_headers
        fake_id = str(uuid4())

        response = client.get(f"/api/users/{fake_id}", headers=headers)

        assert response.status_code == 404

    def test_update_user(self, client: TestClient, db_session, auth_headers):
        headers, auth_user = auth_headers

        update_data = {
            "username": "Updated User",
            "authorizations": {"role": "moderator"}
        }

        response = client.put(f"/api/users/{auth_user.id}", json=update_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "Updated User"

    def test_delete_user(self, client: TestClient, db_session, auth_headers):
        headers, _ = auth_headers

        # Create user to delete
        user = User(username="To Delete", auth_type="test", is_active=True)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        response = client.delete(f"/api/users/{user.id}", headers=headers)

        assert response.status_code == 200
        assert "deactivated successfully" in response.json()["message"]


class TestCourseCRUD:
    def test_create_course(self, client: TestClient, auth_headers):
        headers, user = auth_headers

        course_data = {
            "title": "Test Course",
            "description": "Test Description",
            "keyword": "test",
            "created_by": str(user.id)
        }

        response = client.post("/api/courses", json=course_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Course"
        assert data["created_by"] == str(user.id)

    def test_get_courses(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create test courses
        for i in range(2):
            course = Course(
                title=f"Course {i}",
                created_by=str(user.id),
                updated_by=str(user.id),
                is_active=True
            )
            db_session.add(course)
        db_session.commit()

        response = client.get("/api/courses")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

    def test_get_course_by_id(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        course = Course(
            title="Test Course",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        response = client.get(f"/api/courses/{course.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Course"

    def test_update_course(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        course = Course(
            title="Original Title",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        update_data = {
            "title": "Updated Title",
            "updated_by": str(user.id)
        }

        response = client.put(f"/api/courses/{course.id}", json=update_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"


class TestClassCRUD:
    def test_create_class(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create course first
        course = Course(
            title="Test Course",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        class_data = {
            "title": "Test Class",
            "lecturer_info": "Test Lecturer",
            "created_by": str(user.id)
        }

        response = client.post(f"/api/courses/{course.id}/classes", json=class_data, headers=headers)

        if response.status_code != 200:
            print(f"Error response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Class"
        assert data["course_id"] == str(course.id)

    def test_get_classes_by_course(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create course and classes
        course = Course(
            title="Test Course",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        for i in range(2):
            class_obj = Class(
                course_id=course.id,
                title=f"Class {i}",
                created_by=str(user.id),
                updated_by=str(user.id),
                is_active=True
            )
            db_session.add(class_obj)
        db_session.commit()

        response = client.get(f"/api/courses/{course.id}/classes")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2


class TestLectureCRUD:
    def test_create_lecture(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create course and class
        course = Course(
            title="Test Course",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        class_obj = Class(
            course_id=course.id,
            title="Test Class",
            created_by=str(user.id),
            updated_by=str(user.id),
            is_active=True
        )
        db_session.add(class_obj)
        db_session.commit()
        db_session.refresh(class_obj)

        lecture_data = {
            "title": "Test Lecture",
            "sequence": 1,
            "created_by": str(user.id)
        }

        response = client.post(f"/api/classes/{class_obj.id}/lectures", json=lecture_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Lecture"
        assert data["sequence"] == 1

    def test_get_lectures_by_class(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Setup course, class, and lectures
        course = Course(title="Test Course", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        class_obj = Class(course_id=course.id, title="Test Class", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        db_session.add(class_obj)
        db_session.commit()
        db_session.refresh(class_obj)

        for i in range(2):
            lecture = Lecture(
                class_id=class_obj.id,
                title=f"Lecture {i}",
                sequence=i+1,
                created_by=str(user.id),
                updated_by=str(user.id)
            )
            db_session.add(lecture)
        db_session.commit()

        response = client.get(f"/api/classes/{class_obj.id}/lectures")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2


class TestAttendanceCRUD:
    def test_create_attendance(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Setup course, class, and lecture
        course = Course(title="Test Course", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        class_obj = Class(course_id=course.id, title="Test Class", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        lecture = Lecture(class_id=class_obj.id, title="Test Lecture", sequence=1, created_by=str(user.id), updated_by=str(user.id))

        db_session.add_all([course, class_obj, lecture])
        db_session.commit()
        db_session.refresh(lecture)

        attendance_data = {
            "user_id": str(user.id),
            "status": "present",
            "created_by": str(user.id)
        }

        response = client.post(f"/api/lectures/{lecture.id}/attendances", json=attendance_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "present"
        assert data["user_id"] == str(user.id)


class TestCertificationCRUD:
    def test_create_certification(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create course
        course = Course(title="Test Course", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        certification_data = {
            "course_id": str(course.id),
            "user_id": str(user.id),
            "issued_at": "2024-01-01T00:00:00",
            "created_by": str(user.id)
        }

        response = client.post("/api/certifications", json=certification_data, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["course_id"] == str(course.id)
        assert data["user_id"] == str(user.id)

    def test_get_user_certifications(self, client: TestClient, db_session, auth_headers):
        headers, user = auth_headers

        # Create course and certification
        course = Course(title="Test Course", created_by=str(user.id), updated_by=str(user.id), is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)

        from datetime import datetime
        certification = Certification(
            course_id=course.id,
            user_id=user.id,
            issued_at=datetime.utcnow(),
            created_by=str(user.id),
            updated_by=str(user.id)
        )
        db_session.add(certification)
        db_session.commit()

        response = client.get(f"/api/users/{user.id}/certifications", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1