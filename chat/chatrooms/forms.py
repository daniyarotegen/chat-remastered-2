from django import forms
from django.contrib.auth.models import User


class GroupChatForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none())

