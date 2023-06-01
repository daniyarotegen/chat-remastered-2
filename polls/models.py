from django.db import models
from chatrooms.models import ChatRoom


class Poll(models.Model):
    question = models.CharField(max_length=500)
    allow_multiple_answers = models.BooleanField(default=False)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_by = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.option_text


class PollResponse(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    responded_by = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("poll", "responded_by", "option"),)
