import jwt

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
