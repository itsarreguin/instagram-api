""" Authentication tasks module """

# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Instagram tasks
from instagram.tasks import celery
# Instagram utils
from instagram.utils.token import generate_user_token
from instagram.utils.mail import send_email_multi_alternatives


@celery.task(max_retries=3)
def password_reset_email(user_id: int, path: str) -> None:
    """ Send password rest email to the requesting user """

    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return None

    reset_password_token = generate_user_token(
        user = user,
        exp_mins = 10,
        token_type = 'password_reset'
    )

    send_email_multi_alternatives(
        subject=_('Password rest instructions'),
        template_name='emails/password_reset.html',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        context={
            'user': user,
            'token': reset_password_token,
            'path': path
        }
    )