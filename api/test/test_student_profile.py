import unittest
from .. import create_app, db
from ..models import Student
from ..config import config_object
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256


class TestStudentProfileEndpoint(unittest.TestCase):
    student = None
    app = None

    @classmethod
    def setUpClass(cls):
        """Initialize app and test variables"""
        cls.app = create_app(configure=config_object['testcon'])
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
            # Create a test student
            cls.student = Student(
                first_name="testuser",
                last_name="testuser",
                email="testuser@example.com")
            db.session.add(cls.student)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Teardown all initialized variables"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_student_profile(self):
        """Test that an authenticated student can retrieve their profile"""
        # Create an access token for the test student

        with self.app.app_context():
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
        with self.app.app_context():
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
