from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    error_css_class = 'form--error'

    name = forms.CharField(
        label="Name",
        max_length=50,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Message",
        max_length=280,
        strip=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean(self):
        for field_name in self.errors:
            self[field_name].field.widget.attrs['class'] += ' errorfield'
        return super().clean()

    class Meta:
        fields = ('name', 'email', 'message')


class SignUpForm(forms.ModelForm):
    error_css_class = 'form--error'

    username = forms.CharField(
        label="Username",
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    first_name = forms.CharField(
        label="First name",
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        label="Last name",
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        if "password1" in cleaned_data and "password2" in cleaned_data:
            if cleaned_data["password1"] != cleaned_data["password2"]:
                self.add_error("password1", ValidationError("Passwords did not match."))
            elif len(cleaned_data["password1"]) < 8:
                self.add_error("password1", ValidationError("Password must be at least 8 characters long."))
        if "username" in cleaned_data and User.objects.filter(username=cleaned_data["username"]).exists():
            self.add_error("username", ValidationError("Chosen username already exists."))
        if "email" in cleaned_data and User.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", ValidationError("Chosen email already exists."))

        for field_name in self.errors:
            self[field_name].field.widget.attrs['class'] += ' errorfield'

        cleaned_data["is_active"] = False
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'is_active')
