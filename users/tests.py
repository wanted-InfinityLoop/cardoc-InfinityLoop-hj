import json 

from django.test import TestCase, Client

from users.models import User


class SignUpTest(TestCase):

    def setUp(self):
        self.client = Client()

        User.objects.create(id="test2", password="qwerty2@")

    def tearDown(self):
        User.objects.all().delete()

    def test_post_signup_success(self):
        signup_data = {"id": "test1", "password": "qwerty1!"}
        response = self.client.post('/user/signup', json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_post_signup_already_exist_id(self):
        signup_data = {"id": "test2", "password": "qwerty1!"}
        response=self.client.post('/user/signup',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "ALREADY EXIST ID"})        

    def test_post_signup_invalid_id_type(self):
        signup_data = {"id": "tes", "password": "qwerty1!"}
        response=self.client.post('/user/signup',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID ID TYPE"})        

    def test_post_signup_invalid_password(self):
        signup_data = {"id": "test1", "password": "qwerty"}
        response=self.client.post('/user/signup',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID PWD"})        
