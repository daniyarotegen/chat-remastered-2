import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Poll, PollOption, PollResponse, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_uuid = uuid.UUID(self.scope['url_route']['kwargs']['room_uuid'])
        self.room_group_name = 'poll_%s' % self.room_uuid

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
        self.user = await self.get_user(text_data_json['user_id'])

        if text_data_json['type'] == 'create_poll':
            poll = await self.create_poll(text_data_json['question'], text_data_json['options'],
                                          text_data_json['allow_multiple_answers'])
            await self.send_poll(poll)

        elif text_data_json['type'] == 'vote':
            response = await self.vote(text_data_json['poll_id'], text_data_json['option_id'])
            await self.send_vote(response)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_poll(self, question, options, allow_multiple_answers):
        poll = Poll(question=question, allow_multiple_answers=allow_multiple_answers, chat_room=self.room,
                    created_by=self.user)
        poll.save()

        for option in options:
            PollOption(poll=poll, option_text=option).save()

        return poll

    async def send_poll(self, poll):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'poll_message',
                'message': {
                    'type': 'new_poll',
                    'poll_id': poll.id,
                    'question': poll.question,
                    'options': [option.option_text for option in poll.options.all()],
                    'allow_multiple_answers': poll.allow_multiple_answers
                },
            })

    @database_sync_to_async
    def vote(self, poll_id, option_id):
        poll = Poll.objects.get(id=poll_id)
        option = PollOption.objects.get(id=option_id)
        response = PollResponse(poll=poll, option=option, responded_by=self.user)
        response.save()

        return response

    async def send_vote(self, response):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'poll_message',
                'message': {
                    'type': 'new_vote',
                    'poll_id': response.poll.id,
                    'option_id': response.option.id,
                    'user_id': response.responded_by.id,
                },
            })

    async def poll_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))
