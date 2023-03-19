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
        course = Course(
                course_code="PYT301",
                course_title="Advanced Python",
                course_unit=3,
                teacher="gideon"
        )
        db.session.add(course)
        db.session.commit()

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
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[1].id, 2)
        self.assertEqual(courses[1].course_unit, 2)
        self.assertEqual(courses[1].course_code, "CSC401")

    def test_available_course(self):
        response = self.client.get("/available-courses")
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        data = {
            "course_unit": 3,
            "teacher": "abraham"
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-2023-020200")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.put("/course/PYT301", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

        course = Course.query.filter_by(course_code="PYT301").first()
        self.assertEqual(course.course_unit, 3)
        self.assertEqual(course.teacher, "abraham")
        self.assertEqual(course.course_code, "PYT301")
        self.assertNotEqual(course.course_unit, 2)
        self.assertNotEqual(course.teacher, "gideon")

    def test_delete_course(self):
        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-2023-020200")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.delete("/course/PYT301", headers=headers)
        self.assertEqual(response.status_code, 200)

        course = Course.query.all()
        self.assertEqual(len(course), 0)
        self.assertEqual(course, [])
