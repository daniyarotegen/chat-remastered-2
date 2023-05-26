from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from chatrooms.models import ChatRoom, Chat
from .forms import PollForm, PollOptionFormSet, PollOptionForm
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import PollResponse, Poll, PollOption
from django.forms import inlineformset_factory

PollOptionFormSet = inlineformset_factory(
    Poll, PollOption, form=PollOptionForm, extra=1, can_delete=False
)


class CreatePollView(FormView):
    template_name = 'polls/create_poll.html'
    form_class = PollForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PollOptionFormSet(self.request.POST, instance=Poll())
        else:
            context['formset'] = PollOptionFormSet(instance=Poll())
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
                print("Option text: ", option.option_text)
                option.save()

            chat = Chat.objects.create(
                user=self.request.user,
                room=chat_room,
                content=f"Poll created: {poll.question}. Options are: {', '.join([option.option_text for option in poll.options.all()])}",
                poll=poll
            )
            self.success_url = reverse_lazy('room', kwargs={'room_uuid': self.kwargs['room_uuid']})
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PollVoteView(SingleObjectMixin, View):
    model = Poll
    template_name = 'polls/vote_on_poll.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.options.all())
        return render(request, self.template_name, context={'poll': self.object})

    def post(self, request, *args, **kwargs):
        poll = self.get_object()
        option_id = request.POST.get('option')
        option = poll.options.get(id=option_id)
        PollResponse.objects.create(poll=poll, option=option, responded_by=request.user)
        return redirect('room', room_uuid=poll.chat_room.id)
