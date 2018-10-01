import unittest
from flask import json
from api.views.auth import app


class EndpointsTestCase(unittest.TestCase):
    """
    Tests our API endpoints, run using pytest.
    """
    def setUp(self):
        self.client = app.test_client()

    def test_can_display_message(self):
        """Tests whether endpoint displays welcome message"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)