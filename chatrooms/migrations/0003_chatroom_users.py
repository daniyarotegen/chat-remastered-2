# Generated by Django 4.2.1 on 2023-05-22 07:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatrooms', '0002_chatroom_chat_type_chatroom_is_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(through='chatrooms.ChatRoomMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]