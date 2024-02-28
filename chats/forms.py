from django import forms
from django.core.validators import RegexValidator

from custom_auth.models import CustomUser

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class RoomNameForm(forms.Form):
    """
    Form for chat room selection.

    This form contains one field with chat room name (only alphanumeric).
    """

    ROOM_TYPE = {
        "Room1": CustomUser.T1,
        "Room2": CustomUser.T1,
        "Room3": CustomUser.T2,
        "Room4": CustomUser.T2,
    }

    CHOICES = [(r, f"{r} (only for {t})") for r, t in ROOM_TYPE.items()]
    room_name = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

    """room_name = forms.CharField(
        label="room_name",
        max_length=50,
        required=True,
        validators=[alphanumeric],
    )"""
