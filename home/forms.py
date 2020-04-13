from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class ContactForm(forms.Form):
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

    class Meta:
        fields = ('name', 'email', 'message')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
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
                self.add_error("password1", ValidationError("Passwords did not match"))
            elif len(cleaned_data["password1"]) < 8:
                self.add_error("password1", ValidationError("Password must be at least 8 characters long"))
        if "username" in cleaned_data and User.objects.filter(username=cleaned_data["username"]).exists():
            self.add_error("username", ValidationError("Chosen username already exists"))
        if "email" in cleaned_data and User.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", ValidationError("Chosen email already exists"))

        cleaned_data["is_active"] = False
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'is_active')
