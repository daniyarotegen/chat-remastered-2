# Generated by Django 4.2.1 on 2023-06-01 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_city_alter_profile_marital_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='expertise',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
