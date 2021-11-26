import re
import jwt
import bcrypt

from django.core.exceptions import ValidationError

from users.models import User


def validate_id(id):
    if User.objects.filter(id=id).exists():
        raise ValidationError(("ALREADY EXIST ID"), code="invalid")
    
    if len(id) < 4:
        raise ValidationError(("INVALID ID TYPE"), code="invalid")
    
    return id


def validate_pwd(pwd):
    pwd_check = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$").match(pwd)
    
    if not pwd_check:
        raise ValidationError(("INVALID PWD"), code="invalid")

    return pwd


def validate_user_id(id):
    if not User.objects.filter(id=id).exists():
        raise ValidationError(("INVALID INPUT"), code="invalid")
    
    return User.objects.get(id=id)


def validate_user_pwd(user, pwd):
    if not bcrypt.checkpw(pwd.encode('utf-8'), user.password.encode('utf-8')):
        raise ValidationError(("INVALID INPUT"), code="invalid")
    
    return True
