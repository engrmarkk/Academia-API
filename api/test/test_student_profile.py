import unittest
from .. import create_app, db
from ..models import Student
from ..config import config_object
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256


class TestStudentProfileEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_object["testcon"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        # Create a test student
        student = Student(
            first_name="testuser",
            last_name="testuser",
            email="testuser@example.com",
            stud_id="ACA-2023-020200")
        db.session.add(student)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_get_student_profile(self):
        """Test that an authenticated student can retrieve their profile"""
        # Create an access token for the test student

        student = Student.query.filter_by(email="testuser@example.com").first()
        current_user = student.stud_id
        access_token = create_access_token(identity=current_user)
        # Send a GET request to the /student-profile endpoint with the access token
        response = self.client.get("/student-profile",
                                   headers={"Authorization": f"Bearer {access_token}"})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_patch_student_password(self):
        """Test that an authenticated student can update their password"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="testuser@example.com").first()
        current_user = student.stud_id
        access_token = create_access_token(identity=current_user)

        # Send a PATCH request to the /student-profile endpoint with the access token and new password data
        password_data = {"new_password": "newpassword",
                         "confirm_password": "newpassword"}
        response = self.client.patch("/student-profile",
                                     headers={"Authorization": f"Bearer {access_token}"},
                                     json=password_data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertTrue(pbkdf2_sha256.verify("newpassword", student.password))

    def test_register_course(self):
        """Test that an authenticated student can register a course"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="testuser@example.com").first()
        current_user = student.stud_id

        data = {
            "course_code": "BCH101"
        }

        access_token = create_access_token(identity=current_user)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = self.client.post("/register-course", json=data, headers=headers)
        # this is to ascertain that the course did not exist
        self.assertEqual(response.status_code, 404)

    def test_fetch_stud_id(self):
        """Test that an authenticated student can fetch their student id"""

        response = self.client.get("/get-student-id/testuser@example.com")

        student = Student.query.filter_by(email="testuser@example.com").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.stud_id, "ACA-2023-020200")
