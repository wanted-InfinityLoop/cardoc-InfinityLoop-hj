import json 

from django.test import TestCase, Client

from users.models import User


class CarTest(TestCase):

    def setUp(self):
        self.client = Client()

        User.objects.create(id="test1", password="qwerty1!")
        User.objects.create(id="test2", password="qwerty1!")

    def tearDown(self):
        User.objects.all().delete()

    def test_post_tire_success(self):
        signup_data = [
                        {
                        "id"    : "test1",
                        "trimId": 23000
                        },
                        {
                        "id"    : "test2",
                        "trimId": 7000
                        }
                      ]
        response = self.client.post("/car/tire", json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "USER TIRE SAVED"  : ['test1', 'test2'],
            "USER TIRE UNSAVED": []
            },
        )  

    def test_post_exceed_tire_count(self):
        signup_data = [
                        {
                        "id"    : "test1",
                        "trimId": 23000
                        },
                        {
                        "id"    : "test2",
                        "trimId": 7000
                        },
                        {
                        "id"    : "test3",
                        "trimId": 7000
                        },
                        {
                        "id"    : "test4",
                        "trimId": 7000
                        }
                        ,
                        {
                        "id"    : "test5",
                        "trimId": 7000
                        },
                        {
                        "id"    : "test6",
                        "trimId": 7000
                        }
                      ]
        response=self.client.post("/car/tire", json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "THE MAXIMUM NUMBER OF TIRES STORED IS 5"})        

    def test_post_tire_invalid_user(self):
        signup_data = [
                        {
                        "id"    : "test1",
                        "trimId": 23000
                        },
                        {
                        "id"    : "test3",
                        "trimId": 7000
                        }
                      ]
        response=self.client.post('/car/tire',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "USER TIRE SAVED"  : ["test1"],
            "USER TIRE UNSAVED": ["test3"]
            },
        ) 
        
    def test_post_tire_key_error(self):
        signup_data = [
                        {
                        "ids"    : "test1",
                        "trimId": 23000
                        },
                        {
                        "id"    : "test2",
                        "trimId": 7000
                        }
                      ]
        response=self.client.post('/car/tire',json.dumps(signup_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "KEY ERROR"})        
