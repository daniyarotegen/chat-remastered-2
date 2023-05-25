from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Event
from .forms import EventForm
import calendar
import datetime
from calendar import monthrange
from datetime import datetime, timedelta
from django.utils import timezone


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        year = int(self.kwargs.get('year', today.year))
        month = int(self.kwargs.get('month', today.month))
        _, days_in_month = monthrange(year, month)
        prev_year = year - 1 if month == 1 else year
        prev_month = month - 1 if month != 1 else 12
        next_year = year + 1 if month == 12 else year
        next_month = month + 1 if month != 12 else 1
        start_date = timezone.make_aware(datetime(year, month, 1), timezone.utc)
        end_date = start_date + timedelta(days=days_in_month)
        start_date = max(start_date, timezone.make_aware(datetime.combine(today, datetime.min.time()), timezone.utc))
        events = Event.objects.filter(start_datetime__gte=start_date, start_datetime__lt=end_date).order_by(
            'start_datetime')
        month_calendar = calendar.monthcalendar(year, month)
        context['month'] = month_calendar
        context['days_in_month'] = days_in_month
        context['month_number'] = month
        context['month_name'] = calendar.month_name[month]
        context['year'] = year
        context['prev_month'] = prev_month
        context['prev_year'] = prev_year
        context['next_month'] = next_month
        context['next_year'] = next_year
        context['events'] = events
        return context


class EventDayView(ListView):
    model = Event
    template_name = 'events/event_day.html'
    context_object_name = 'events'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        return Event.objects.filter(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_list')


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

    def get_success_url(self):
        return reverse('event_list')


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer


class EventRegistrationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        attendee = request.user
        event.attendees.add(attendee)
        return redirect('event_detail', pk=pk)
