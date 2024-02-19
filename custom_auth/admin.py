from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ChangeForm, RegisterForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for managing CustomUser instances.

    This class extends UserAdmin class and provides functionality
    to modify the type field of CustomUser.
    """

    model = CustomUser

    add_form = RegisterForm
    form = ChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ["type"]},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {"fields": ["type"]},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
