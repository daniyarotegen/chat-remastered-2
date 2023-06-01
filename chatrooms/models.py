import uuid
from django.db import models
from enum import Enum


class ChatType(Enum):
    PRIVATE = "Private"
    GROUP = "Group"


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    poll = models.ForeignKey('polls.Poll', on_delete=models.SET_NULL, null=True, blank=True)


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chat_type = models.CharField(
        max_length=7,
        choices=[(tag.name, tag.value) for tag in ChatType],
        default=ChatType.PRIVATE,
    )
    users = models.ManyToManyField('accounts.Profile', through='ChatRoomMembership')
    avatar = models.ImageField(upload_to='groupchats/', null=True, blank=True)
    is_group = models.BooleanField(default=False)

    def is_group_chat(self):
        return self.is_group

    def get_user_list(self):
        return [user.username for user in self.users.all()]


class ChatRoomMembership(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
