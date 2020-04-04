from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractForm
from wagtail.core.models import Page, PAGE_TEMPLATE_VAR


class HomePage(Page):
    pass


class SignUpForm(forms.Form):
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

    def clean(self):
        cleaned_data = self.cleaned_data

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error("password1", ValidationError("Passwords did not match"))

        return cleaned_data


class SignUpPage(Page):
    form = SignUpForm()

    def get_context(self, request, *args, **kwargs):
        self.form = SignUpForm(request.POST or None)

        if request.method == 'POST' and self.form.is_valid():
            pass

        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request
        }
