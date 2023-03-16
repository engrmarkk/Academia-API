from flask_jwt_extended import create_access_token
from .. import create_app
from ..extensions import db
from ..config import config_object
from ..models import Course
import unittest


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(configure=config_object['testcon'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_create_course(self):
        data = {
            "course_code": "CSC401",
            "course_title": "Advanced Programming",
            "course_unit": 2,
            "teacher": "mark",
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-2023-020200")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/create-course", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        # check if student was created
        courses = Course.query.all()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].id, 1)
        self.assertEqual(courses[0].course_unit, 2)
        self.assertEqual(courses[0].course_code, "CSC401")
