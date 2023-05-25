from django.urls import path
from .views import EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, EventDayView

urlpatterns = [
    path('event_list/', EventListView.as_view(), name='event_list'),
    path('event_list/<int:year>/<int:month>/', EventListView.as_view(), name='event_list_nav'),
    path('<int:year>/<int:month>/<int:day>/', EventDayView.as_view(), name='event_day'),
    path('<uuid:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('new/', EventCreateView.as_view(), name='event_create'),
    path('<uuid:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('<uuid:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]
