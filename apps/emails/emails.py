from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


class Email(object):
    email = None

    def __init__(self, subject, ctx, to, template):
        html = render_to_string(template,ctx)
        self.email = EmailMultiAlternatives(
            subject=subject,
            body="This is a simple text email body.",
            from_email="SIPEP <sipepuacj@gmail.com>",
            to=to.split(',')
        )
        self.email.attach_alternative(html, "text/html")

    def send(self):
        self.email.send()