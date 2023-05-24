from django.views.generic.edit import FormView
from chatrooms.models import ChatRoom
from .forms import PollForm, PollOptionForm
from .models import PollOption


class CreatePollView(FormView):
    template_name = 'polls/create_poll.html'
    form_class = PollForm
    success_url = '/thanks/'

    def form_valid(self, form):
        poll = form.save(commit=False)
        poll.chat_room = ChatRoom.objects.get(id=self.kwargs['room_uuid'])
        poll.created_by = self.request.user
        poll.save()

        for option_text in self.request.POST.getlist('options'):
            PollOption.objects.create(poll=poll, option_text=option_text)

        return super().form_valid(form)

