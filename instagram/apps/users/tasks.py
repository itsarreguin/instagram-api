""" Users tasks module """

from datetime import timedelta

import jwt

# Django imports
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Instagram tasks
from instagram.tasks import celery
# Instagram models
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


@celery.task(max_retries=4)
def send_verification_email(user_id):
    """ Celery task that helps to send an email verification """
    user = User.objects.get(pk=user_id)
    verification_token = gen_verification_token(user=user)

    subject: str = 'Account verification'
    template = render_to_string(
        template_name='emails/account_verification.html',
        context={
            'token': verification_token,
            'user': user
        }
    )
    from_email: str = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives(subject, template, from_email, to=[user.email])
    msg.attach_alternative(template, 'text/html')
    msg.send(fail_silently=False)