from django import forms
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class RoomNameForm(forms.Form):
    """
    Form for chat room selection.

    This form contains one field with chat room name (only alphanumeric).
    """

    room_name = forms.CharField(
        label="room_name",
        max_length=50,
        required=True,
        validators=[alphanumeric],
    )
