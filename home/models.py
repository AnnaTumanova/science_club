from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm
from wagtail.core.models import Page, PAGE_TEMPLATE_VAR

from .tokens import account_activation_token


class HomePage(Page):
    pass


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data["password1"] != cleaned_data["password2"]:
            self.add_error("password1", ValidationError("Passwords did not match"))
        elif len(cleaned_data["password1"]) < 8:
            self.add_error("password1", ValidationError("Password must be at least 8 characters long"))
        if User.objects.filter(username=cleaned_data["username"]).exists():
            self.add_error("username", ValidationError("Chosen username already exists"))
        if User.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", ValidationError("Chosen email already exists"))

        cleaned_data['is_active'] = False
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'is_active')


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

                message = render_to_string('account_confirmation_mail.html', {
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
