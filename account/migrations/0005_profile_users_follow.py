# Generated by Django 4.1.9 on 2023-11-13 13:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_remove_profile_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='users_follow',
            field=models.ManyToManyField(blank=True, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
    ]