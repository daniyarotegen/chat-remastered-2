from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Profile


class UserAdmin(DjangoUserAdmin):
    # Include all extra fields here.
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Custom fields", {
            'fields': (
                'business_sector',
                'company',
                'expertise',
                'resources',
                'achievements',
                'goals',
                'requests',
                'city',
                'date_of_birth',
                'hobbies',
                'education',
                'interesting_facts',
                'marital_status',
                'phone_number',
                'website',
                'social_media_links',
            ),
        }),
    )

admin.site.register(Profile, UserAdmin)
