from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=40, required=True)
    password = forms.CharField(
        label="Password",
        max_length=40,
        required=True,
        widget=forms.PasswordInput,
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
