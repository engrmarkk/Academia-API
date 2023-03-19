import unittest
from .. import create_app, db
from ..models import Student
from ..config import config_object
from flask_jwt_extended import create_access_token


class TestStudentAdminEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app(configure=config_object['testcon'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()
        student = Student(
            first_name="testuser",
            last_name="testuser",
            email="joe@example.com",
            stud_id="ACA-2023-020200"
        )
        db.session.add(student)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_create_student(self):

        data = {
            "first_name": "john",
            "last_name": "joe",
            "email": "mark@example.com"
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
        self.assertEqual(len(students), 2)
        self.assertEqual(students[1].id, 2)
        self.assertEqual(students[1].first_name, "john")
        self.assertEqual(students[1].last_name, "joe")
        self.assertTrue(students[1].stud_id.startswith("ACA"))

    def test_get_students(self):
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

    def test_get_each_student(self):
        student = Student.query.filter_by(email="joe@example.com").first()
        stud_id = student.stud_id

        token = create_access_token(identity="ADMIN-2023-020200")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get(f"/student/{stud_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], 'testuser')

    def test_delete_student(self):
        student = Student.query.filter_by(email="joe@example.com").first()
        stud_id = student.stud_id
        token = create_access_token(identity="ADMIN-2023-020200")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.delete(f"/student/{stud_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

        student = Student.query.filter_by(email="mark@example.com").first()
        self.assertEqual(student, None)
