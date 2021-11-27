import jwt
import re
import requests

from django.http import JsonResponse

from users.models import User
from my_settings import ALGORITHM, MY_SECRET_KEY


def login_check(func):
    def wrapper(self, request, *arg, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, MY_SECRET_KEY, ALGORITHM)
            user_id      = User.objects.get(id = payload['user_id'])
            request.user = user_id
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": 'INVALID_USER'}, status=404)

        return func(self, request, *arg, **kwargs)

    return wrapper


def get_car_info(data):
    trim_id    = data["trimId"]
    car_info   = requests.get(f"https://dev.mycar.cardoc.co.kr/v1/trim/{trim_id}").json()
    front_tire = re.split("[P/R]",car_info.get("spec")["driving"]["frontTire"]["value"].replace(" ", ""))
    rear_tire  = re.split("[P/R]", car_info.get("spec")["driving"]["rearTire"]["value"].replace(" ", ""))
    info_dic = {
        "trim_id"   : trim_id,
        "car_brand" : car_info.get("brandName", None),
        "year_type" : car_info.get("yearType", None),
        "car_name"  : car_info.get("submodelGroupName", None),
        "front_tire": list(filter(bool, front_tire)),
        "rear_tire" : list(filter(bool, rear_tire))
    }

    return info_dic


def create_tire(Tire, car_name, info, location):
    WIDTH        = 0
    ASPECT_RATIO = 1
    WHEEL_SIZE   = 2

    tire = Tire.objects.create(
        name        =f"{car_name} {location} 타이어",
        width       =info[WIDTH],
        aspect_ratio=info[ASPECT_RATIO],
        wheel_size  =info[WHEEL_SIZE]
        )

    return tire

 