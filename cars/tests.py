import jwt
import json 
import bcrypt

from django.test import TestCase, Client

from cars.models import Car, FrontTire, RearTire, Spec
from users.models import User
from my_settings  import MY_SECRET_KEY, ALGORITHM

class CarTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.car = Car.objects.create(name="오피러스", brand="기아", year_type=2004)
        
        self.front_tire = FrontTire.objects.create(
            name        ="오피러스 전 타이어", 
            width       =225, 
            aspect_ratio=60, 
            wheel_size  =16
            )
        
        self.rear_tire = RearTire.objects.create(
            name        ="오피러스 후 타이어", 
            width       =225, 
            aspect_ratio=60, 
            wheel_size  =16
            )
        
        Spec.objects.create(car=self.car, front_tire=self.front_tire, rear_tire=self.rear_tire)

        self.user1 = User.objects.create(
            id      ="test1",
            password=bcrypt.hashpw("qwerty1!".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), 
            car     =self.car
            )
        
        self.user2 = User.objects.create(id="test2", password="qwerty1!")
    
        self.user1_token = jwt.encode(
        {"user_id": self.user1.id}, MY_SECRET_KEY, ALGORITHM
        )

        self.user2_token = jwt.encode(
        {"user_id": self.user2.id}, MY_SECRET_KEY, ALGORITHM
        )

    def tearDown(self):
        User.objects.all().delete()
        Spec.objects.all().delete()
        RearTire.objects.all().delete()
        FrontTire.objects.all().delete()
        Spec.objects.all().delete()

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
                        "ids"   : "test1",
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

    def test_get_tire_info_success(self):
        header = {"HTTP_Authorization": self.user1_token}
        response=self.client.get('/car/tire?id=test1', **header, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                        'test1 TIRE INFORMATION': [{
                            'aspect_ratio': 60,
                            'name'        : '오피러스 전 타이어',
                            'wheel_size'  : 16,
                            'width'       : 225
                            },
                            {
                            'aspect_ratio': 60,
                            'name'        : '오피러스 후 타이어',
                            'wheel_size'  : 16,
                            'width'       : 225
                            }
                        ]
                    }
                )        

    def test_get_tire_info_wrong_user(self):
        header = {"HTTP_Authorization": self.user1_token}
        response=self.client.get('/car/tire?id=test2', **header, content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message" : "WRONG USER"}) 

    def test_get_tire_info_not_found(self):
        header = {"HTTP_Authorization": self.user2_token}
        response=self.client.get("/car/tire?id=test2", **header, content_type="application/json")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message" : "NOT FOUND TIRE INFO"}) 
