from django.urls import path
from .views import CreatePollView, PollVoteView

urlpatterns = [
    path('create/<uuid:room_uuid>', CreatePollView.as_view(), name='create_poll'),
    path('<int:pk>/vote/', PollVoteView.as_view(), name='vote_on_poll'),
]