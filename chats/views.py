from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from chat_app.settings import WS_CONN

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
        if room_name in RoomNameForm.ROOM_TYPE.keys():
            room_type = RoomNameForm.ROOM_TYPE[room_name]
            if request.user.type == room_type:
                return render(
                    request,
                    "chats/room.html",
                    {
                        "room_name": room_name,
                        "room_type": room_type,
                        "ws_conn": WS_CONN,
                    },
                )
            else:
                return render(
                    request,
                    "chats/invalid_type.html",
                    {"room_name": room_name, "room_type": room_type},
                )
        else:
            raise Http404("This room does not exist")
    else:
        return redirect("custom_auth:login")
