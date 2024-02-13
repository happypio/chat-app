from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("chats:chat"))
        else:
            return render(
                request,
                "custom_auth/login.html",
                {"error_message": "Invalid login"},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("chats:chat"))
        else:
            return render(
                request,
                "custom_auth/login.html",
            )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("custom_auth:login"))
