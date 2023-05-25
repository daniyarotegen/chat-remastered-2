from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventDayView,
    EventRegistrationView,
)

urlpatterns = [
    path('event_list/', EventListView.as_view(), name='event_list'),
    path('event_list/<int:year>/<int:month>/', EventListView.as_view(), name='event_list_nav'),
    path('<int:year>/<int:month>/<int:day>/', EventDayView.as_view(), name='event_day'),
    path('<uuid:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('new/', EventCreateView.as_view(), name='event_create'),
    path('<uuid:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<uuid:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('<uuid:pk>/register/', EventRegistrationView.as_view(), name='event_registration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
