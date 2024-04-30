# Generated by Django 4.1.9 on 2023-11-19 15:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning_logs', '0007_topic_users_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='topic',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='topic_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='topic',
            index=models.Index(fields=['-total_likes'], name='learning_lo_total_l_8ecf65_idx'),
        ),
    ]
