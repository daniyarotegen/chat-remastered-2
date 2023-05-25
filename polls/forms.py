from django import forms
from django.forms import formset_factory
from .models import Poll, PollOption


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'allow_multiple_answers']


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['option_text']


PollOptionFormSet = formset_factory(PollOptionForm, extra=1)
