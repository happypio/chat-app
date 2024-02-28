from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase

from chats.consumers import ChatConsumer
from custom_auth.models import CustomUser


class ChatConsumerTestCase(TransactionTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            type="Type 1",
        )
        self.second_user = get_user_model().objects.create_user(
            username="testuser_2",
            email="test2@example.com",
            password="testpassword",
            type="Type 1",
        )
        self.anonymous_user = AnonymousUser()

    async def test_message_sending_by_user(self):
        room = "Room1"
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )
        communicator.scope["url_route"] = {"kwargs": {"room_name": room}}
        communicator.scope["user"] = self.user
        connected, subprotocol = await communicator.connect()

        self.assertTrue(connected)

        message_data = {
            "type": "chat_message",
            "message": "Test message",
        }
        await communicator.send_json_to(message_data)

        response = await communicator.receive_json_from()
        self.assertEqual(response["message"], "Test message")

        await communicator.disconnect()

    async def test_message_sending_by_anonymous_user(self):
        room = "Room1"
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )
        communicator.scope["url_route"] = {"kwargs": {"room_name": room}}
        communicator.scope["user"] = self.anonymous_user
        connected, subprotocol = await communicator.connect()

        self.assertFalse(connected)

    async def test_message_receiving_by_second_user_in_same_room(self):
        room = "Room1"
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )
        communicator_2 = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )

        communicator.scope["url_route"] = {"kwargs": {"room_name": room}}
        communicator.scope["user"] = self.user
        connected, subprotocol = await communicator.connect()

        communicator_2.scope["url_route"] = {"kwargs": {"room_name": room}}
        communicator_2.scope["user"] = self.second_user
        connected_2, subprotocol = await communicator_2.connect()

        self.assertTrue(connected_2)
        self.assertTrue(connected)

        message_data = {
            "type": "chat_message",
            "message": "Test message",
        }
        await communicator.send_json_to(message_data)

        response = await communicator_2.receive_json_from()
        self.assertEqual(response["message"], "Test message")

        await communicator.disconnect()
        await communicator_2.disconnect()

    async def test_message_receiving_by_second_user_in_different_room(self):
        room = "Room1"
        different_room = "Room2"
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )
        communicator_2 = WebsocketCommunicator(
            ChatConsumer.as_asgi(), f"/ws/{room}/"
        )

        communicator.scope["url_route"] = {"kwargs": {"room_name": room}}
        communicator.scope["user"] = self.user
        connected, subprotocol = await communicator.connect()

        communicator_2.scope["url_route"] = {
            "kwargs": {"room_name": different_room}
        }
        communicator_2.scope["user"] = self.second_user
        connected_2, subprotocol = await communicator_2.connect()

        self.assertTrue(connected_2)
        self.assertTrue(connected)

        message_data = {
            "type": "chat_message",
            "message": "Test message",
        }
        await communicator.send_json_to(message_data)
        res = await communicator_2.receive_nothing()

        self.assertTrue(res)

        await communicator.disconnect()
        await communicator_2.disconnect()

        async def test_message_sending_by_user_with_wrong_type(self):
            room = "Room3"  # it has type 2 (user has type 1)
            communicator = WebsocketCommunicator(
                ChatConsumer.as_asgi(), f"/ws/{room}/"
            )
            communicator.scope["url_route"] = {"kwargs": {"room_name": room}}
            communicator.scope["user"] = self.user
            connected, subprotocol = await communicator.connect()

            self.assertFalse(connected)
