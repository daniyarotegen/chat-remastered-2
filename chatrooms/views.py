from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView
from .forms import GroupChatForm, FileForm
from .models import ChatRoom, Chat
from django.contrib.auth import get_user_model

User = get_user_model()


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/index.html')


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
        print(f"Chatrooms are {chatrooms}")
        chats_with_recipients = []
        for room in chatrooms:
            chat = room.chat_set.order_by('-timestamp').first()
            if room.is_group:
                chat_name = room.name
                avatar_url = room.avatar.url if room.avatar else None
                if chat:
                    chats_with_recipients.append({'chat': chat, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})
                else:
                    chats_with_recipients.append({'chat': None, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})
            else:
                if chat:
                    recipient = room.users.exclude(id=request.user.id).first()
                    chat_name = recipient.first_name + " " + recipient.last_name
                    avatar_url = recipient.avatar.url if recipient.avatar else None
                    chats_with_recipients.append({'chat': chat, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})

        chats_with_recipients.sort(key=lambda x: x['chat'].timestamp if x['chat'] else timezone.now(), reverse=True)
        return render(request, 'chatrooms/chats.html', {'chats_with_recipients': chats_with_recipients})


class Room(LoginRequiredMixin, View):
    def get(self, request, room_uuid):
        room = ChatRoom.objects.filter(id=room_uuid).first()
        if room is None:
            return HttpResponse("Room not found", status=404)

        chats = Chat.objects.filter(room=room).order_by('-timestamp')
        form = FileForm()

        return render(request, 'chatrooms/room.html',
                      {'room_name': room.name, 'room_id': str(room.id), 'chats': chats,
                       'is_group_chat': room.is_group, 'form': form, 'room': room})


class GroupChatProfileView(LoginRequiredMixin, TemplateView):
    template_name = "chatrooms/group_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = kwargs.get('group_id')
        groupchat = get_object_or_404(ChatRoom, id=group_id)
        context['groupchat'] = groupchat
        return context


class CreateGroupChatView(LoginRequiredMixin, View):
    def get(self, request):
        form = GroupChatForm()
        form.fields['users'].queryset = User.objects.exclude(id=request.user.id)
        return render(request, 'chatrooms/create_group_chat.html', {'form': form})

    def post(self, request):
        form = GroupChatForm(request.POST, request.FILES)
        form.fields['users'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            users = form.cleaned_data['users']
            users = list(users) + [request.user]
            name = form.cleaned_data['name']
            description = form.cleaned_data.get('description', '')
            avatar = form.cleaned_data.get('avatar', None)
            room, created = ChatRoom.objects.get_or_create(
                name=name,
                defaults={'is_group': True, 'description': description, 'avatar': avatar, 'creator': request.user}
            )
            if created:
                for user in users:
                    room.users.add(user)
            return redirect(reverse('room', args=[str(room.id)]))
        return render(request, 'chatrooms/create_group_chat.html', {'form': form})


class EditGroupChatView(LoginRequiredMixin, UpdateView):
    model = ChatRoom
    template_name = 'chatrooms/edit_group_chat.html'
    form_class = GroupChatForm

    def get_object(self, queryset=None):
        groupchat = super().get_object()
        if not groupchat.creator == self.request.user:
            raise Http404()
        return groupchat

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['users'].queryset = User.objects.all()
        form.fields['users'].initial = self.object.users.all()
        return form

    def form_valid(self, form):
        groupchat = form.save(commit=False)
        if groupchat.creator != self.request.user:
            return HttpResponseForbidden()

        users = form.cleaned_data['users']
        if not any(user.id == self.request.user.id for user in users):
            users = list(users) + [self.request.user]
        print(f"Users are {users}")
        groupchat.users.set(users)
        groupchat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('group-profile', args=[str(self.object.id)])


def calendar_view(request):
    return render(request, 'chatrooms/calendar.html')


@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(LoginRequiredMixin, View):
    def post(self, request, room_uuid):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.chat_room = ChatRoom.objects.get(id=room_uuid)
            new_file.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{room_uuid}',
                {
                    'type': 'file.upload',
                    'file_url': new_file.file.url,
                    'user_id': request.user.id,
                }
            )
            return JsonResponse({'file_url': new_file.file.url})
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
