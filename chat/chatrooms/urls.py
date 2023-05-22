from django.urls import path
from .views import Index, Room, StartChatView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('start_chat/<str:username>/', StartChatView.as_view(), name='start-chat'),
    path('<uuid:room_uuid>/', Room.as_view(), name='room'),
]