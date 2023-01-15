""" Authentication tasks module """

# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives

# Instagram tasks
from instagram.tasks import celery
# Instagram utils
from instagram.utils.token import generate_user_token


@celery.task(max_retries=3)
def password_reset_email(user_id):
    """"""
    user = get_user_model().objects.get(id=user_id)

    reset_password_token = generate_user_token(
        user = user,
        exp_mins = 10,
        token_type = 'password_reset'
    )

    subject = 'Password rest instructions'
    content = loader.render_to_string(
        template_name = 'emails/password_reset.html',
        context = {
            'user': user,
            'token': reset_password_token
        }
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(content, 'text/html')
    msg.send(fail_silently=False)