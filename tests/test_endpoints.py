import unittest
from flask import jsonify
from api.views.auth import app
from api.models.dbcontroller import DbController


class EndpointsTestCase(unittest.TestCase):
    """
    Tests our API endpoints, run using pytest.
    """
    def setUp(self):
        self.client = app.test_client()
        self.db = DbController().get_users()

    def test_can_display_message(self):
        """Tests whether endpoint displays welcome message"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_can_signup(self):
        test_signup = {"name":"wali","password":"@br@h@m1234","role":"admin"}
        response = self.client.post(/v2/auth/signup, json = test_signup)
        self.assertEqual(response.status_code,201)
        result = DbController().get_element_by_id(1,user_table)

    def test_can_isolate_errors(self):
        response = self.client.post(/v2/auth/signup, json = {"name":"",
        "password":"@br@h@m1234","role":"admin"})
        self.assertEqual(response.status_code,400)
        response2 = self.client.post(/v2/auth/signup, json = {"name":"wali",
        "password":"@br","role":"admin"})
        self.assertEqual(response2.status_code,400)
        response = self.client.post(/v2/auth/signup, json = {"name":"wali",
        "password":"@br@h@m1234","role":"admins"})
        self.assertEqual(response.status_code,400)
