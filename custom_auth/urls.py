from django.urls import path

from . import views

app_name = "custom_auth"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("settings", views.settings_view, name="settings"),
    path("change_password", views.change_password, name="change_password"),
]
