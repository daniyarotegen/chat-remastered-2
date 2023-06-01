from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar', 'first_name', 'last_name', 'business_sector', 'company', 'expertise', 'resources',
                  'achievements', 'goals', 'requests', 'city', 'date_of_birth', 'hobbies', 'education',
                  'interesting_facts', 'marital_status', 'phone_number', 'website', 'social_media_links']


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
