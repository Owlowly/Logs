# Generated by Django 4.1.9 on 2023-12-26 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0010_alter_entry_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='slug',
        ),
    ]
