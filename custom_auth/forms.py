from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


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
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "type"]


class ChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "type"]
