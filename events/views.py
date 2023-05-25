from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from .forms import EventForm
from django.urls import reverse
import calendar
import datetime
from calendar import monthrange


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        year = int(self.kwargs.get('year', today.year))
        month = int(self.kwargs.get('month', today.month))
        _, days_in_month = monthrange(year, month)
        prev_year = year - 1 if month == 1 else year
        prev_month = month - 1 if month != 1 else 12
        _, days_in_prev_month = monthrange(prev_year, prev_month)
        next_year = year + 1 if month == 12 else year
        next_month = month + 1 if month != 12 else 1
        _, days_in_next_month = monthrange(next_year, next_month)
        month_calendar = calendar.monthcalendar(year, month)
        for i, day in enumerate(month_calendar[0]):
            if day == 0:
                month_calendar[0][i] = days_in_prev_month - len([d for d in month_calendar[0] if d == 0]) + i + 1
        next_month_day = 1
        for i, day in enumerate(month_calendar[-1]):
            if day == 0:
                month_calendar[-1][i] = next_month_day
                next_month_day += 1
        context['month'] = month_calendar
        context['days_in_month'] = days_in_month
        context['month_number'] = month
        context['month_name'] = calendar.month_name[month]
        context['year'] = year
        context['prev_month'] = prev_month
        context['prev_year'] = prev_year
        context['next_month'] = next_month
        context['next_year'] = next_year
        return context


class EventDayView(ListView):
    model = Event
    template_name = 'events/event_day.html'
    context_object_name = 'events'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        return Event.objects.filter(start_date__year=year, start_date__month=month, start_date__day=day)


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
