from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class LoginForm(forms.Form):
    """
    For for user login.

    This form contains fields for username and passwrod for user login.
    """

    username = forms.CharField(label="Username", max_length=40, required=True)
    password = forms.CharField(
        label="Password",
        max_length=40,
        required=True,
        widget=forms.PasswordInput,
    )


class RegisterForm(UserCreationForm):
    """
    Form for user registration.

    This form extends the UserCreationForm and includes fields for
    username, email, passowrd (twice for confirmation) and user type.
    """

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "type"]


class ChangeForm(UserChangeForm):
    """
    Form for changing user details.

    This form extends the UserChangeForm and includes fields for
    username, email, and user type.
    """

    class Meta:
        model = CustomUser
        fields = ["username", "email", "type"]


class ChangeTypeForm(UserChangeForm):
    """
    Form for changing user type.

    This form extends the UserChangeForm and contains only type field.
    """

    password = None

    class Meta:
        model = CustomUser
        fields = ["type"]
