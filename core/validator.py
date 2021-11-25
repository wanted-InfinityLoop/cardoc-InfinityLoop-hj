import re

from django.core.exceptions import ValidationError

from users.models import User


def validate_id(id):
    if User.objects.filter(id=id).exists():
        raise ValidationError(("ALREADY EXIST ID"), code = "invalid")
    
    if len(id) < 4:
        raise ValidationError(("INVALID ID TYPE"), code="invalid")
    
    return id


def validate_pwd(pwd):
    pwd_check = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$").match(pwd)
    
    if not pwd_check:
        raise ValidationError(("INVALID PWD"), code = "invalid")

    return pwd

