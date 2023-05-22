import uuid
from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class ChatType(Enum):
    PRIVATE = "Private"
    GROUP = "Group"


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chat_type = models.CharField(
        max_length=7,
        choices=[(tag.name, tag.value) for tag in ChatType],
        default=ChatType.PRIVATE,
    )
    users = models.ManyToManyField(User, through='ChatRoomMembership')
    is_group = models.BooleanField(default=False)

    def is_group_chat(self):
        return self.is_group

    def get_user_list(self):
        return [user.username for user in self.users.all()]


class ChatRoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
