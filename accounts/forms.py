from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['business_sector', 'company', 'expertise', 'resources', 'achievements', 'goals', 'requests',
                  'city', 'date_of_birth', 'hobbies', 'education', 'interesting_facts', 'marital_status',
                  'phone_number', 'website', 'social_media_links']
