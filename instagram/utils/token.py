""" Instagram clone token utils """

# JSON Web Token
import jwt

# Python standard library
from datetime import timedelta

# Django imports
from django.conf import settings
from django.utils import timezone

# Instagram models
from instagram.core.models import User


def generate_user_token(user: User, exp_mins: int = None, token_type: str = None) -> str:
    exp_date = timezone.now() + timedelta(minutes=exp_mins)

    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': token_type
    }
    token = jwt.encode(payload, key=settings.SECRET_KEY, algorithm='HS256')

    return token