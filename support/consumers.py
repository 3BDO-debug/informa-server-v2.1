import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "informa.settings")
django.setup()


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . import models, serializers
from accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        await self.channel_layer.group_add(self.conversation_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.conversation_id, self.channel_name)

    async def broadcast_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        conversation_id = event["conversation_id"]

        # Only create the message in the database if this message
        # originated from this WebSocket client
        if self.channel_name == event["sender_channel_name"]:
            conversation = await sync_to_async(
                models.SupportConversation.objects.get, thread_sensitive=True
            )(conversation_name=conversation_id)
            sender = await sync_to_async(User.objects.get, thread_sensitive=True)(
                id=int(sender_id)
            )

            message_exists = await sync_to_async(
                models.SupportConversationMessage.objects.filter(
                    conversation=conversation, sender=sender, message=message
                ).exists,
                thread_sensitive=True,
            )()  # Now exists is called

            if not message_exists:
                message_obj = await sync_to_async(
                    models.SupportConversationMessage.objects.create,
                    thread_sensitive=True,
                )(conversation=conversation, sender=sender, message=message)

                message_obj_serializer = (
                    serializers.SupportConversationMessageSerializer(
                        message_obj, many=False
                    ).data
                )

                await self.channel_layer.group_send(
                    self.conversation_id,
                    {
                        "type": "broadcast_message",
                        "message": message_obj_serializer,
                    },
                )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        sender_id = text_data_json["senderId"]
        message = text_data_json["message"]
        conversation_id = text_data_json["conversationId"]

        # Send message to the group for this conversation
        await self.channel_layer.group_send(
            self.conversation_id,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
                "conversation_id": conversation_id,
                "sender_channel_name": self.channel_name,  # Add this line
            },
        )
