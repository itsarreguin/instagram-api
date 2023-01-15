""" Instagram clone mail utils """

# Python standard library
from typing import (
    Any,
    Dict,
    List
)

# Django imports
from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_email_multi_alternatives(
    subject: str = ...,
    template_name: str = ...,
    from_email: str = None,
    to: List[str] = None,
    context: Dict[str, Any] = None
) -> None:
    template = loader.render_to_string(
        template_name=template_name,
        context=context
    )

    msg = EmailMultiAlternatives(
        subject = subject,
        body = template,
        from_email = from_email,
        to = to
    )
    msg.attach_alternative(template, 'text/html')
    msg.send(fail_silently=False)