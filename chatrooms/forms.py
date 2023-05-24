from django import forms
from django.contrib.auth.models import User
from .models import File


class GroupChatForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none())


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
