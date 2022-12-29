""" Instagram clone email utils """

import jwt

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from instagram.core.models import User


def gen_verification_token(user: User):
    exp_date = timezone.now() + timedelta(minutes=15)

    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'verification_email'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token