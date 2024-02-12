from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def chat(request):
    if request.user.is_authenticated:
        return render(request, "chats/chats.html")
    else:
        return HttpResponseRedirect(reverse("custom_auth:login"))
