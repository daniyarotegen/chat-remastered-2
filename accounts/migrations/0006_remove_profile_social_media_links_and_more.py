# Generated by Django 4.2.1 on 2023-06-01 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_business_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='social_media_links',
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tiktok_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='vk_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='whatsapp_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]