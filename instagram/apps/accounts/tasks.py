""" Background tasks module for users """

# Django imports
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Pillow imports
from PIL import Image

# Instagram tasks
from instagram.tasks import celery
# Instagram models
from instagram.core.models import User
# Instagram utils
from instagram.utils.token import generate_user_token
from instagram.utils.mail import send_email_multi_alternatives


@celery.task(max_retries=4)
def send_verification_email(user_id: int) -> None:
    """ Celery task that helps to send an email verification """

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None

    account_verification_token = generate_user_token(
        user = user,
        exp_mins = 15,
        token_type = 'verification_email'
    )

    send_email_multi_alternatives(
        subject=_('Account verification'),
        template_name='emails/account_verification.html',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        context={
            'user': user,
            'token': account_verification_token
        }
    )


@celery.task
def resize_profile_pic():
    pass