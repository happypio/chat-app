from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model for the application.

    It extends AbstractUser and adds type field to categorize users
    into different types.
    """

    T1 = "Type 1"
    T2 = "Type 2"
    TYPE_CHOICES = (
        (T1, "type 1"),
        (T2, "type 2"),
    )
    type = models.CharField(
        max_length=6,
        choices=TYPE_CHOICES,
        help_text=("Type of account determines access to chat rooms"),
    )
