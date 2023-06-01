from django import forms
from django.contrib.auth import get_user_model

from .models import File

User = get_user_model()


class GroupChatForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none(),
                                           widget=forms.CheckboxSelectMultiple)
    avatar = forms.ImageField(required=False)


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
