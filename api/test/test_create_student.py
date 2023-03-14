from flask_jwt_extended import create_access_token
from .. import create_app
from ..extensions import db
from ..config import config_object
from ..models import Student
import unittest


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object["testcon"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_student(self):
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
