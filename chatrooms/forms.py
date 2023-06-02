from django import forms
from django.contrib.auth import get_user_model
from .models import File, ChatRoom

User = get_user_model()


class UserModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class GroupChatForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    users = UserModelChoiceField(queryset=User.objects.none(),
                                 widget=forms.CheckboxSelectMultiple)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'users', 'avatar']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
