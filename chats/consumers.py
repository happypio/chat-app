import json
from datetime import datetime, timedelta, timezone

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .forms import RoomNameForm


class ChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer for handling chat functionality.
    """

    def connect(self):
        """
        Connects a user to the chat room if authenticated and verifies room access permissions.
        """
        if not self.scope["user"].is_authenticated:
            self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # check if room name is in allowed rooms
        if self.room_name not in RoomNameForm.ROOM_TYPE.keys():
            self.close()
            return

        # check if type is suitable
        if self.scope["user"].type != RoomNameForm.ROOM_TYPE[self.room_name]:
            self.close()
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        info = f"User {self.scope['user'].username} has joined the chat"
        # Send info_message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "info_chat_message", "info": info},
        )

    def get_log_time(self):
        """
        Get the current time in UTC format.

        Returns:
            str: Current time in "HH:MM:SS" format.
        """
        now = datetime.now(timezone.utc) + timedelta(hours=1)
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def disconnect(self, close_code):
        """
        Handles disconnection from the chat room.
        """

        info = f"User {self.scope['user'].username} has left the chat"
        # Send info_message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "info_chat_message", "info": info},
        )

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        """
        Receives a message from WebSocket and forwards it to the chat room.

        Args:
            text_data (str): The received message data.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.scope["user"].username,
            },
        )

    # Receive info message from group
    def info_chat_message(self, event):
        """
        Sends an information message to the WebSocket.

        Args:
            event (dict): The event containing the information message.
        """
        info = event["info"]
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "info": info,
                    "log_time": self.get_log_time(),
                }
            )
        )

    # Receive message from room group
    def chat_message(self, event):
        """
        Sends a chat message to the WebSocket.

        Args:
            event (dict): The event containing the chat message.
        """

        message = event["message"]
        user = event["user"]
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "user": user,
                    "message": message,
                    "log_time": self.get_log_time(),
                }
            )
        )
