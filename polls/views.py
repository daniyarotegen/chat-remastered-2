from django.views.generic.edit import FormView
from chatrooms.models import ChatRoom, Chat
from .forms import PollForm, PollOptionFormSet
from django.urls import reverse_lazy


class CreatePollView(FormView):
    template_name = 'polls/create_poll.html'
    form_class = PollForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PollOptionFormSet(self.request.POST)
        else:
            context['formset'] = PollOptionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            poll = form.save(commit=False)
            chat_room = ChatRoom.objects.get(id=self.kwargs['room_uuid'])
            poll.chat_room = chat_room
            poll.created_by = self.request.user
            poll.save()

            for form in formset:
                option = form.save(commit=False)
                option.poll = poll
                option.save()
        else:
            return self.form_invalid(form)

        chat = Chat.objects.create(
            user=self.request.user,
            room=chat_room,
            content=f"Poll created: {poll.question}"
        )
        self.success_url = reverse_lazy('room', kwargs={'room_uuid': self.kwargs['room_uuid']})
        return super().form_valid(form)
