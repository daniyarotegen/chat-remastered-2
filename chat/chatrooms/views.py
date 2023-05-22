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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/profile.html')


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chatrooms/user_list.html', {'users': users})


class StartChatView(LoginRequiredMixin, View):
    def get(self, request, username):
        other_user = User.objects.get(username=username)
        if not other_user:
            return HttpResponse("User not found", status=404)

        rooms = ChatRoom.objects.filter(users__in=[request.user, other_user], is_group=False)
        room = None

        for potential_room in rooms:
            if potential_room.users.count() == 2 and set(potential_room.users.all()) == set([request.user, other_user]):
                room = potential_room
                break

        if room is None:
            room = ChatRoom.objects.create(name=f'Chat with {other_user.username}', is_group=False)
            room.users.add(request.user, other_user)

        return redirect(reverse('room', args=[str(room.id)]))


class ChatsView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = ChatRoom.objects.filter(users=request.user).distinct()
        chats_with_recipients = []
        for room in chatrooms:
            chat = room.chat_set.order_by('-timestamp').first()
            if chat:
                recipients = room.users.exclude(id=request.user.id)
                if room.is_group:
                    recipient_names = ', '.join([user.username for user in recipients.all()])
                else:
                    recipient_names = recipients.first().username
                chats_with_recipients.append({'chat': chat, 'recipient_names': recipient_names,
                                              'room_id': str(room.id)})

        chats_with_recipients.sort(key=lambda x: x['chat'].timestamp, reverse=True)
        return render(request, 'chatrooms/chats.html', {'chats_with_recipients': chats_with_recipients})




class Room(LoginRequiredMixin, View):
    def get(self, request, room_uuid):
        room = ChatRoom.objects.filter(id=room_uuid).first()
        if room is None:
            return HttpResponse("Room not found", status=404)

        chats = Chat.objects.filter(room=room).order_by('-timestamp')

        return render(request, 'chatrooms/room.html',
                      {'room_name': room.name, 'room_id': str(room.id), 'chats': chats, 'is_group_chat': room.is_group})


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
            if created:
                for user in users:
                    room.users.add(user)
            return redirect(reverse('room', args=[str(room.id)]))
        return render(request, 'chatrooms/create_group_chat.html', {'form': form})
