from django.urls import path
from .views import Index, Room, StartChatView, GroupChatProfileView, EditGroupChatView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('start_chat/<str:username>/', StartChatView.as_view(), name='start-chat'),
    path('<uuid:room_uuid>/', Room.as_view(), name='room'),
    path('groupchat/<uuid:group_id>/', GroupChatProfileView.as_view(), name='group-profile'),
    path('groupchat/<uuid:pk>/edit/', EditGroupChatView.as_view(), name='edit-group-chat'),
]