from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    diff = now - value

    minutes = diff.total_seconds() // 60
    hours = diff.total_seconds() // 3600
    days = diff.total_seconds() // 86400

    if diff <= timedelta(minutes=1):
        return '1 minute ago'
    elif diff <= timedelta(hours=1):
        return f'{int(minutes)} minutes ago'
    elif diff <= timedelta(hours=2):
        return '1 hour ago'
    elif diff <= timedelta(days=1):
        return f'{int(hours)} hours ago'
    elif diff <= timedelta(days=2):
        return '1 day ago'
    else:
        return f'{int(days)} days ago'
