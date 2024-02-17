from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import ChangeTypeForm, LoginForm, RegisterForm


def settings_view(request: HttpRequest) -> HttpResponse:
    """
    View for handling user settings.

    This view allows authenticated users to change their account settings.
    If user isn't authenticated it redirects him to login view.

    Args:
        request (HttpRequest): current request
    Returns:
        HttpResponse: Rendered template with settings form
    """
    if request.user.is_authenticated:
        pass_form = PasswordChangeForm(request.user)

        if request.method == "POST":
            sett_form = ChangeTypeForm(request.POST, instance=request.user)
            if sett_form.is_valid():
                sett_form.save()
                messages.success(request, "Your type has been updated!")
                return redirect(to="custom_auth:settings")
            else:
                messages.error(request, f"Invalid form")
        else:
            sett_form = ChangeTypeForm(instance=request.user)

        return render(
            request,
            "custom_auth/settings.html",
            {
                "sett_form": sett_form,
                "pass_form": pass_form,
            },
        )
    else:
        return redirect(to="custom_auth:login")


def change_password(request: HttpRequest) -> HttpResponse:
    """
    View for handling password change request.

    This view allows only authenticated users to change their passwords.

    Args:
        request (HttpRequest): current request
    Returns:
        HttpResponse: Rendered template with settings form
    """
    if request.user.is_authenticated:
        sett_form = ChangeTypeForm(instance=request.user)

        if request.method == "POST":
            pass_form = PasswordChangeForm(request.user, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Your password was successfully updated!"
                )
                return redirect(to="custom_auth:settings")
            else:
                messages.error(request, "Failed to update password")
        else:
            pass_form = PasswordChangeForm(request.user)

        return render(
            request,
            "custom_auth/settings.html",
            {
                "sett_form": sett_form,
                "pass_form": pass_form,
            },
        )
    else:
        return redirect(to="custom_auth:login")


def redirect_if_authenticated(
    request: HttpRequest, to_redirect: str, to_render: str, args: dict = None
) -> HttpResponse:
    """
    Redirects to specified url if user is not authenticated.
    Else renders specified tempalte.

    Args:
        request (HttpRequest): current request
        to_redirect (str): name of an app view
        to_render (str): path to html file with template
        args (dict, optional): a dictionary to add to the template context
    Returns:
        HttpResponse: Rendered template with settings form or redirect to specified url

    """
    if request.user.is_authenticated:
        return redirect(to=to_redirect)
    else:
        return render(
            request,
            to_render,
            args,
        )


def login_view(request: HttpRequest) -> HttpResponse:
    """
    View for handling user login.

    This view allows authenticated users to log in to the application

    Args:
        request (HttpRequest): current request
    Returns:
        HttpResponse: Rendered template with settings form
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(
                    request, f"Hi {username.title()}, welcome back!"
                )
                login(request, user)
                return redirect(to="chats:chat")
        messages.error(request, f"Invalid username or password")
        return render(
            request,
            "custom_auth/login.html",
            {"form": form},
        )

    else:
        form = LoginForm()
        return redirect_if_authenticated(
            request,
            "chats:chat",
            "custom_auth/login.html",
            args={"form": form},
        )


def register_view(request: HttpRequest) -> HttpResponse:
    """
    View for handling user registration requests.

    This view allows users to register a new account.

    Args:
        request (HttpRequest): current request
    Returns:
        HttpResponse: Rendered template with settings form
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect(to="chats:chat")
        else:
            return render(
                request,
                "custom_auth/register.html",
                {"form": form},
            )
    else:
        form = RegisterForm()
        return redirect_if_authenticated(
            request,
            "chats:chat",
            "custom_auth/register.html",
            args={"form": form},
        )


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    View for handling user logout.

    This view logs out the currently authenticated user.

    Args:
        request (HttpRequest): current request
    Returns:
        HttpResponse: Rendered template with settings form
    """
    logout(request)
    messages.success(request, f"You have been logged out.")
    return redirect(to="custom_auth:login")
