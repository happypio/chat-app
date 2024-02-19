from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .forms import ChangeForm, ChangeTypeForm, LoginForm, RegisterForm
from .models import CustomUser
from .views import (
    change_password,
    login_view,
    logout_view,
    redirect_if_authenticated,
    register_view,
    settings_view,
)


class SettingsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_auth_user_setting_view(self):
        request = self.factory.get(reverse("custom_auth:settings"))
        request.user = self.user
        response = settings_view(request)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_unauth_user_settings_view(self):
        request = self.factory.get(reverse("custom_auth:settings"))
        request.user = AnonymousUser()
        response = settings_view(request)

        # Check if the response redirects to the login page
        self.assertRedirects(
            response,
            reverse("custom_auth:login"),
            status_code=302,
            fetch_redirect_response=False,
        )


class ChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_unauth_user_password_view(self):
        request = self.factory.get(reverse("custom_auth:change_password"))
        request.user = AnonymousUser()
        response = change_password(request)

        # Check if the response redirects to the login page
        self.assertRedirects(
            response,
            reverse("custom_auth:login"),
            status_code=302,
            fetch_redirect_response=False,
        )

    def test_auth_user_password_view(self):
        request = self.factory.get(reverse("custom_auth:change_password"))
        request.user = self.user
        response = change_password(request)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_password_change_by_auth_user(self):
        data = {
            "old_password": "testpassword1",
            "new_password1": "newtestpassword",
            "new_password2": "newtestpassword",
        }

        user = CustomUser.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("custom_auth:change_password"), data
        )

        # Redirects after successful password change
        self.assertRedirects(
            response,
            reverse("custom_auth:settings"),
            status_code=302,
        )

        user.refresh_from_db()  # Refresh the user object from the database
        self.assertTrue(
            user.check_password("newtestpassword")
        )  # Check if the password has been updated

    def test_wrong_password_change_by_auth_user(self):
        data = {
            "old_password": "wrong_testpassword1",
            "new_password1": "newtestpassword",
            "new_password2": "newtestpassword",
        }

        user = CustomUser.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("custom_auth:change_password"), data
        )

        self.assertEqual(
            response.status_code, 200
        )  # Form should be re-rendered with errors
        self.assertFormError(
            response.context["pass_form"],
            "old_password",
            "Your old password was entered incorrectly. Please enter it again.",
        )


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_login_view_GET(self):
        response = self.client.get(reverse("custom_auth:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "custom_auth/login.html")

    def test_login_view_POST_valid_data(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = self.client.post(reverse("custom_auth:login"), data)

        self.assertRedirects(
            response,
            reverse("chats:chat"),
            status_code=302,
        )

    def test_login_view_POST_invalid_data(self):
        data = {
            "username": "testuser",
            "password": "wrongtestpassword",
        }

        response = self.client.post(reverse("custom_auth:login"), data)

        self.assertEqual(response.status_code, 200)

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Invalid username or password")


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_register_view_GET(self):
        response = self.client.get(reverse("custom_auth:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "custom_auth/register.html")

    def test_register_view_POST_valid_data(self):
        data = {
            "username": "newtestuser",
            "email": "newtestuser@example.com",
            "password1": "123testing",
            "password2": "123testing",
            "type": "Type 1",
        }

        response = self.client.post(reverse("custom_auth:register"), data)
        self.assertRedirects(response, reverse("chats:chat"), status_code=302)

    def test_register_view_POST_invalid_data(self):
        data = {
            "username": "newtestuser",
            "email": "newtestuser@example.com",
            "password1": "testpassword",
            "password2": "wrongtestpassword",
            "type": "Type 1",
        }

        response = self.client.post(reverse("custom_auth:register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "password2",
            "The two password fields didn’t match.",
        )
        # self.assertContains(response, "The two password fields didn’t match.")


class LogoutViewTestCase(TestCase):
    def test_logout_view(self):
        user = CustomUser.objects.create_user(
            username="testuser1", password="testpassword1"
        )
        self.client.force_login(user)
        response = self.client.post(reverse("custom_auth:logout"))
        self.assertRedirects(
            response,
            reverse("custom_auth:login"),
            status_code=302,
        )


class LoginFormTestCase(TestCase):
    def test_valid_login_form(self):
        form_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        form_data = {
            "username": "",
            "password": "",
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterFormTestCase(TestCase):
    def test_valid_register_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "type": "Type 1",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_register_form(self):
        form_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "type": "Type 1",
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class ChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com"
        )

    def test_valid_change_form(self):
        form_data = {
            "username": "newtestuser",
            "email": "newtest@example.com",
            "type": "Type 2",
        }
        form = ChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_change_form(self):
        form_data = {
            "username": "",
            "email": "newtest@example.com",
            "type": "Type 2",
        }
        form = ChangeForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())


class ChangeTypeFormTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser", email="test@example.com"
        )

    def test_valid_change_type_form(self):
        form_data = {
            "type": "Type 2",
        }
        form = ChangeTypeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_change_type_form(self):
        form_data = {
            "type": "",
        }
        form = ChangeTypeForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
