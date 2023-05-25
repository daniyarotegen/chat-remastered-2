import uuid
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_datetime = models.DateTimeField()
    venue = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, through='EventAttendee')
    image = models.ImageField(upload_to='demo/', null=True, blank=True)

    def __str__(self):
        return self.title


class EventAttendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
