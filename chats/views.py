from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RoomNameForm


def chat(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = RoomNameForm(request.POST)
            if form.is_valid():
                return redirect(
                    to="chats:room", room_name=form.cleaned_data["room_name"]
                )
            else:
                messages.error(request, f"Invalid room name")
                return render(
                    request,
                    "chats/index.html",
                    {
                        "form": form,
                    },
                )
        else:
            form = RoomNameForm()
            return render(
                request,
                "chats/index.html",
                {
                    "form": form,
                },
            )
    else:
        return redirect("custom_auth:login")


def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, "chats/room.html", {"room_name": room_name})
    else:
        return redirect("custom_auth:login")
