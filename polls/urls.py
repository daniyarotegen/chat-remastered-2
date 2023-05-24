from django.urls import path
from .views import CreatePollView

urlpatterns = [
    path('create/<uuid:room_uuid>', CreatePollView.as_view(), name='create_poll'),
]