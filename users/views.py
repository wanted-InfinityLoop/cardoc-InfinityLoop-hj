import jwt
import json
import bcrypt

from django.views.generic   import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models   import User
from core.validator import validate_id, validate_pwd, validate_user_id, validate_user_pwd

from my_settings import MY_SECRET_KEY, ALGORITHM


class SignupView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            id         = validate_id(data["id"])
            password   = validate_pwd(data["password"])
            
            hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(id=id, password=hashed_pwd)

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=400)

        except KeyError:
            return JsonResponse({'message': "KEY ERROR"}, status=400)


class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user_id  = validate_user_id(data["id"])
            password = validate_user_pwd(user_id, data["password"])
            
            if password:
                token = jwt.encode({'user_id':user_id.id}, MY_SECRET_KEY, ALGORITHM).decode('utf-8')
            
            return JsonResponse({"message": "SUCCESS", "token": token}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=400)

        except KeyError:
            return JsonResponse({'message': "KEY ERROR"}, status=400)
