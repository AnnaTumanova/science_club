from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm
from wagtail.core.models import Page, PAGE_TEMPLATE_VAR

from django.conf import settings
from .forms import ContactForm, SignUpForm
from .tokens import account_activation_token


class HomePage(Page):
    form = ContactForm()

    def get_context(self, request, *args, **kwargs):
        self.form = ContactForm(request.POST or None)

        if request.method == 'POST' and self.form.is_valid():
            try:
                data = self.form.cleaned_data
                mail_subject = "Message from: " + data.get('name')
                message = render_to_string('mail/contact_message_mail.html', {
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'message': data.get('message')
                })
                email = EmailMessage(
                    mail_subject, message, to=[settings.DEFAULT_CONTACT_US_EMAIL]
                )
                email.send()
            except:
                self.form.add_error(None, "Error occurred during message sending")

        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request
        }


class SignUpPage(Page):
    form = SignUpForm()
    is_account_created = False
    confirmation_link = None

    def get_context(self, request, *args, **kwargs):
        self.form = SignUpForm(request.POST or None)

        if request.method == 'POST' and self.form.is_valid():
            try:
                user = self.form.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                message = render_to_string('mail/account_confirmation_mail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token
                })
                to_email = self.form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                self.is_account_created = True
            except:
                self.form.add_error(None, "Error occurred during user registration")

        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request
        }
