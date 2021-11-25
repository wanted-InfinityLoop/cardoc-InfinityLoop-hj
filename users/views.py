import json
import bcrypt

from django.views.generic import View
from django.http.response import JsonResponse
from django.core.exceptions import ValidationError

from users.models import User
from core.validator import validate_id, validate_pwd


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
