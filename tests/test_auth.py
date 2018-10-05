import unittest
from flask import json
from api.models.dbcontroller import DbController
import unittest
from api import app

class EndpointsTestCase(unittest.TestCase):
    """
    Tests our API endpoints, run using pytest.
    """
    def setUp(self):
        test_db = DbController()
        test_db.create_tables()
        self.client = app.test_client()
        self.test_order = {"order":"matooke"}
        self.test_order2 = {"order":"rice"}
        self.test_order3 = {"order":"chips"}
        self.test_status1 = {"completed_status":"yes"}
        self.admin={"name":"qwrrudc","password":"!23dsgd","role":"admin"}

    def tearDown(self):
        test_db = DbController()
        test_db.drop_tables()    

    def test_register_valid_details(self):
        """ Tests creating a new user with valid details """
        test_user = {
            'name': 'walimiiike',
            'password': 'password123',
            'role': 'user'
        }
        response = self.client.post('/auth/signup',
                                    data=json.dumps(test_user),
                                    content_type='application/json')
        self.assertIn('You have successfully signed up.',
                      str(response.data))
        self.assertEqual(response.status_code, 201) 
        

    def test_can_not_register_similar_names(self):       
        test_user = {
            'name': 'walimiiike',
            'password': 'password123',
            'role': 'user'
        }
        response = self.client.post('/auth/signup', data=json.dumps(test_user),
                                    content_type='application/json')                      
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/auth/signup', data=json.dumps(test_user),
                                    content_type='application/json') 
        self.assertIn('User already exists', str(response.data))


    def test_login_valid_credentials(self):
        test_user = {
            'name': 'walimiiike',
            'password': 'password123',
            'role': 'user'
        }
        response = self.client.post('/auth/signup',
                                    data=json.dumps(test_user),
                                    content_type='application/json')
        self.assertIn('You have successfully signed up.',
                      str(response.data))
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/auth/login',
                                    data=json.dumps(test_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)   

    def test_register_with_blank_inputs(self):
        """ Tests creating a new user with blank """
        inv_char = {
            'name': '',
            'username': ' ',
            'password': ''
        }
        response = self.client.post('/auth/signup',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_non_json_input(self):
        """ Tests register with non valid JSON input """
        response = self.client.post('/auth/signup',
                                    data='some non json data',
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_characters(self):
        """ Test login with invalid characters """
        inv_char = {
            'username': '#$%',
            'password': '@#$%'
        }
        response = self.client.post('/auth/login',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_with_blank_inputs(self):
        """ Tests creating a new user with blank """
        inv_char = {

            'username': ' ',
            'password': ''
        }
        response = self.client.post('/auth/login',
                                    data=json.dumps(inv_char),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_password(self):
        """ Tests login with wrong password  """
        user = {
            'name': 'right user',
            'username': 'rightuser',
            'password': 'rightpassword'
        }
        self.client.post('/auth/register',
                         data=json.dumps(user),
                         content_type='application/json')
        user_login = {
            'username': 'rightuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/auth/login',
                                    data=json.dumps(user_login),
                                    content_type='application/json')

        self.assertIn('Missing username parameter', str(response.data))
        self.assertEqual(response.status_code, 400)                     

        