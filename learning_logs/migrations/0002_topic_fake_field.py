# Generated by Django 4.1.9 on 2023-11-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='fake_field',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
