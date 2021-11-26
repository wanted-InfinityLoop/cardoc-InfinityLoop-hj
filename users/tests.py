import jwt
import json 
import bcrypt

from django.test import TestCase, Client

from users.models import User
from my_settings  import MY_SECRET_KEY, ALGORITHM


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
        self.assertEqual(response.json(), {"message" : "SUCCESS"})  

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

    def test_post_signup_key_error(self):
        signup_data = {"ids": "test1", "password": "qwerty1@"}
        response=self.client.post('/user/signin',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "KEY ERROR"})  


class SignInTest(TestCase):

    def setUp(self):
        self.client = Client()

        user1 = User.objects.create(id="test1", password=bcrypt.hashpw("qwerty1!".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))

        self.access_token1 = jwt.encode({"user_id": user1.id}, MY_SECRET_KEY, ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()

    def test_post_signin_success(self):
        signin_data = {"id": "test1", "password": "qwerty1!"}
        response = self.client.post("/user/signin", json.dumps(signin_data), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message" : "SUCCESS", "token": self.access_token1})  

    def test_post_signin_invalid_id(self):
        signup_data = {"id": "test2", "password": "qwerty1!"}
        response=self.client.post("/user/signin", json.dumps(signup_data), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID INPUT"})  

    def test_post_signin_invalid_pwd(self):
        signup_data = {"id": "test1", "password": "qwerty@@"}
        response=self.client.post("/user/signin", json.dumps(signup_data), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "INVALID INPUT"}) 

    def test_post_signin_key_error(self):
        signup_data = {"ids": "test1", "password": "qwerty@@"}
        response=self.client.post("/user/signin", json.dumps(signup_data), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "KEY ERROR"})         
