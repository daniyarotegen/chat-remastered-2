import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_uuid = uuid.UUID(self.scope['url_route']['kwargs']['room_uuid'])
        self.room_group_name = 'chat_%s' % self.room_uuid

        self.room = await self.get_room(self.room_uuid)

        if self.room is None:
            print(f"No room found with uuid {self.room_uuid}")
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_room(self, room_uuid):
        try:
            room = ChatRoom.objects.get(id=room_uuid)
            return room
        except ChatRoom.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.user_id = self.scope['user'].id

        room = await database_sync_to_async(ChatRoom.objects.get)(id=self.room_uuid)

        chat = Chat(
            content=message,
            user=self.scope['user'],
            room=room
        )

        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': self.user_id
            })

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id
        }))
