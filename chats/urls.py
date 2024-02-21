from django.urls import path, re_path

from . import views

app_name = "chats"

urlpatterns = [
    path("", views.chat, name="chat"),
    re_path(r"(?P<room_name>[0-9a-zA-Z]{1,50})/$", views.room, name="room"),
]
