# import unittest
# from ..extensions import db
# from ..config import config_object
# from .. import create_app
# from ..models import Admin
#
#
# class UserTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(config_object["testcon"])
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         self.client = self.app.test_client()
#         db.create_all()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
#         self.app = None
#         self.client = None
#
#     def test_user_registration(self):
#         # test for user registration
#         data = {
#             "first_name": "john",
#             "last_name": "doe",
#             "email": "johndoe@yahoo.com",
#             "password": "password"
#         }
#         response = self.client.post("/register", json=data)
#         admin = Admin.query.filter_by(email=data["email"]).first()
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(admin.first_name, data["first_name"])
#         self.assertEqual(admin.last_name, data["last_name"])
#         self.assertEqual(admin.email, data["email"])
