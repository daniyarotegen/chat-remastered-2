from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GroupChatForm
from .models import ChatRoom, Chat
from django.contrib.auth.models import User


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/index.html')


class StartChatView(LoginRequiredMixin, View):
    def get(self, request, username):
        other_user = User.objects.get(username=username)
        if not other_user:
            return HttpResponse("User not found", status=404)
        room_name = '_'.join(sorted([str(request.user.id), str(other_user.id)]))
        room, created = ChatRoom.objects.get_or_create(
            name=room_name,
            defaults={'is_group': False}
        )
        room.users.add(request.user)
        room.users.add(other_user)
        return redirect(reverse('room', args=[room_name]))


class ChatsView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = ChatRoom.objects.filter(users=request.user).distinct()
        chats_with_recipients = []
        for room in chatrooms:
            chat = room.chat_set.order_by('-timestamp').first()
            recipients = room.users.exclude(id=request.user.id)
            if room.is_group:
                recipient_names = ', '.join([user.username for user in recipients.all()])
            else:
                recipient_names = recipients.first().username
            chats_with_recipients.append({'chat': chat, 'recipient_names': recipient_names, 'room_name': room.name})
        return render(request, 'chatrooms/chats.html', {'chats_with_recipients': chats_with_recipients})



class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        room = ChatRoom.objects.filter(name=room_name).first()
        if room is None:
            return HttpResponse("Room not found", status=404)

        chats = Chat.objects.filter(room=room).order_by('-timestamp')

        return render(request, 'chatrooms/room.html',
                      {'room_name': room_name, 'chats': chats, 'is_group_chat': room.is_group_chat()})


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chatrooms/user_list.html', {'users': users})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/profile.html')


class CreateGroupChatView(LoginRequiredMixin, View):
    def get(self, request):
        form = GroupChatForm()
        form.fields['users'].queryset = User.objects.exclude(id=request.user.id)
        return render(request, 'chatrooms/create_group_chat.html', {'form': form})

    def post(self, request):
        form = GroupChatForm(request.POST)
        form.fields['users'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            users = form.cleaned_data['users']
            users = list(users) + [request.user]
            name = form.cleaned_data['name']
            description = form.cleaned_data.get('description', '')
            room, created = ChatRoom.objects.get_or_create(
                name=name,
                defaults={'is_group': True, 'description': description}
            )
            for user in users:
                room.users.add(user)
            return redirect(reverse('room', args=[name]))
        return render(request, 'chatrooms/create_group_chat.html', {'form': form})
