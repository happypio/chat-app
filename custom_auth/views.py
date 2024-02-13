from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


def redirect_if_authenticated(request, to_redirect, to_render, args=None):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(to_redirect))
    else:
        return render(
            request,
            to_render,
            args,
        )


def login_view(request):
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
                return HttpResponseRedirect(reverse("chats:chat"))
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


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return HttpResponseRedirect(reverse("chats:chat"))
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


def logout_view(request):
    logout(request)
    messages.success(request, f"You have been logged out.")
    return HttpResponseRedirect(reverse("custom_auth:login"))
