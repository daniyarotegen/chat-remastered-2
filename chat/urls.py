"""
URL configuration for chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import ProfileView, EditProfileView, UserListView, UserProfileView
from chatrooms.views import ChatsView, CreateGroupChatView, calendar_view, FileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("users/", UserListView.as_view(), name="user-list"),
    path('chats/', ChatsView.as_view(), name='chats'),
    path('chat/', include('chatrooms.urls')),
    path('events/', include('events.urls')),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('create_group_chat/', CreateGroupChatView.as_view(), name='create_group_chat'),
    path('polls/', include('polls.urls')),
    path('calendar/', calendar_view, name='calendar'),
    path('upload/<uuid:room_uuid>/', FileUploadView.as_view(), name='file-upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
