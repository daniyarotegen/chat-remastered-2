from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    BUSINESS_SECTORS = (
        ('agriculture', 'Agriculture'),
        ('construction', 'Construction'),
        ('manufacturing', 'Manufacturing'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
        ('transportation', 'Transportation'),
        ('information', 'Information'),
        ('finance', 'Finance and Insurance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education Services')
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    business_sector = models.CharField(choices=BUSINESS_SECTORS, max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    expertise = models.CharField(max_length=100, blank=True, null=True)
    resources = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    requests = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    interesting_facts = models.TextField(blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)
