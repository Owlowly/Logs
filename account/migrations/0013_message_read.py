# Generated by Django 4.1.9 on 2023-11-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
