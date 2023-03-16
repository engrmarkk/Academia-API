import unittest
from .. import create_app, db
from ..models import Student
from ..config import config_object
from flask_jwt_extended import create_access_token


class TestStudentAdminEndpoint(unittest.TestCase):
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
            # cls.student = Student(
            #     first_name="testuser",
            #     last_name="testuser",
            #     email="testuser@example.com")
            # db.session.add(cls.student)
            # db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Teardown all initialized variables"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_student(self):
        with self.app.app_context():

            data = {
                "first_name": "john",
                "last_name": "joe",
                "email": "joe@example.com"
            }

            # create JWT token for authorization
            token = create_access_token(identity="ADMIN-2023-020200")

            # set headers with JWT token
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = self.client.post("/create-student", json=data, headers=headers)

            self.assertEqual(response.status_code, 201)

            # check if student was created
            students = Student.query.all()
            self.assertEqual(len(students), 1)
            self.assertEqual(students[0].id, 1)
            self.assertEqual(students[0].first_name, "john")
            self.assertEqual(students[0].last_name, "joe")

    def test_get_students(self):
        with self.app.app_context():
            # create JWT token for authorization
            token = create_access_token(identity="ADMIN-2023-020200")

            # set headers with JWT token
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = self.client.get("/students", headers=headers)
            self.assertEqual(response.status_code, 200)
            students = Student.query.all()
            self.assertEqual(len(students), 1)
            self.assertEqual(students[0].registered_courses, [])

    def test_update_student_data(self):
        with self.app.app_context():

            student = Student.query.filter_by(email="joe@example.com").first()
            stud_id = student.stud_id

            token = create_access_token(identity="ADMIN-2023-020200")

            # set headers with JWT token
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = self.client.put(f"/student/{stud_id}",
                                       headers=headers,
                                       json={
                                        "first_name": "chris",
                                        "last_name": "",
                                        "email": ""
                                        })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(student.first_name, 'chris')
            self.assertEqual(student.email, 'joe@example.com')
